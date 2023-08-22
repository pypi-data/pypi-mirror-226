from . import acquisition
from . import util
import tweepy
import threading
import time
import json
import gzip
from datetime import datetime
import os
import glob
from math import inf
import re
import logging
import time

l = logging.getLogger("pandem.twitter")

class AcquisitionTwitter(acquisition.Acquisition):
    def __init__(self, name, orchestrator_ref, settings): 
        super().__init__(name = name, orchestrator_ref = orchestrator_ref, settings = settings, channel = "twitter")

    def on_start(self):
        super().on_start()
        self._storage_proxy = self._orchestrator_proxy.get_actor("storage").get().proxy()
        # Getting twitter credentials
        self._api_key=util.get_or_set_secret("twitter-api-key") 
        self._api_key_secret=util.get_or_set_secret("twitter-api-key-secret") 
        self._access_token=util.get_or_set_secret("twitter-access-token") 
        self._access_token_secret=util.get_or_set_secret("twitter-access-token-secret") 
        self._replay_dir = util.pandem_path("files", "twitter", "v1.1", "replay")
        self._filter_dir = util.pandem_path("files", "twitter", "v1.1", "tweets")
        self._filter_arc_dir = util.pandem_path("files", "twitter", "v1.1", "archived")
        if not os.path.exists(self._filter_dir):
          os.makedirs(name = self._filter_dir)
        if not os.path.exists(self._filter_arc_dir):
          os.makedirs(name = self._filter_arc_dir)
        # storing the api to do hydrate tweet
        auth = tweepy.OAuth2AppHandler(
          consumer_key = self._api_key, 
          consumer_secret = self._api_key_secret 
        )

        self._api = tweepy.API(auth, wait_on_rate_limit = True)

    def add_datasource(self, dls, force_acquire, ignore_last_exec = True):
      if len(self.current_sources) > 0:
        raise ValueError("Twitter aqquisition support only a single DLS, others will be ignored")
      if "acquisition" in dls and "channel" in dls["acquisition"] and "topics" in dls["acquisition"]["channel"]:
        self._topics  = dls["acquisition"]["channel"]["topics"].keys()
        self._maingroup  = dls["acquisition"]["channel"]["main_group"]
        self._phrases = []
        self._included_regex = {}
        self._topic_groups = {}
        for topic in self._topics:
          self._included_regex[topic] = ""
          if "phrases" in dls["acquisition"]["channel"]["topics"][topic]:
            phrases = dls["acquisition"]["channel"]["topics"][topic]["phrases"]
            in_maingroup = dls["acquisition"]["channel"]["topics"][topic]["group"] == self._maingroup
            self._included_regex[topic] = "|".join(map(lambda v: re.escape(v.lower()), phrases))  
            for kw in phrases:
              if not kw in self._phrases and in_maingroup:
                if len(kw.encode("utf-8")) > 60:
                  raise ValueError(f"Twitter filter endpoint cannot contain phrases bigger than 60 bytes and {kw} has {len(kw.encode('utf-8'))}")
                self._phrases.append(kw)
          else:
            raise ValueError("Twitter DLS topics needs to have a phrases property with a list of phrases to use")
          if "group" in dls["acquisition"]["channel"]["topics"][topic]:
            self._topic_groups[topic] =  dls["acquisition"]["channel"]["topics"][topic]["group"]
      else: 
        raise ValueError("If a Twitter DLS is found it should contain a (possible empty) list of topics under ['acquisition']['channel']")
      
      if "acquisition" in dls and "channel" in dls["acquisition"] and "languages" in dls["acquisition"]["channel"]:
        self._languages = dls["acquisition"]["channel"]["languages"]
      else:
        self._languages = None

      if "acquisition" in dls and "channel" in dls["acquisition"] and "excluded_phrases" in dls["acquisition"]["channel"]:
        self._excluded_regex =  "|".join(map(lambda v: re.escape(v.lower()), dls["acquisition"]["channel"]["excluded_phrases"]))
      else:
        self._excluded_regex = None

      if "acquisition" in dls and "channel" in dls["acquisition"] and "include_retweets" in dls["acquisition"]["channel"]:
        self._include_retweets = bool(dls["acquisition"]["channel"]["include_retweets"])
      else:
        self._include_retweets = False
      
      # launching the tweet collection
      self.tweet_filter = self.TwitterFilter(
        track = self._phrases,
        included_regex = self._included_regex,
        excluded_regex = self._excluded_regex,
        include_retweets = self._include_retweets,
        topic_groups = self._topic_groups,
        languages = self._languages,
        filter_dir = self._filter_dir,
        consumer_key = self._api_key, 
        consumer_secret = self._api_key_secret, 
        access_token = self._access_token, 
        access_token_secret = self._access_token_secret
      )
      self.create_new_gz()
      threading.Thread(target=self.tweet_filter.run).start()


      super().add_datasource(dls, force_acquire, ignore_last_exec)

    def hydrate_tweet_ids(self, ids):
      i = 0
      j = 0
      ret = {}
      while i < len(ids):
        # setting a minumum of 0.5 secs between requests
        start = time.time()
        success = False
        tries = 0
        while not success:
          try:
            res = self._api.lookup_statuses(ids[i:i+100], include_entities = False, trim_user = True)
            success = True
          except Exception as e:
            tries = tries + 1
            if tries <= 10 :
              l.debug(f"Tweet request failed with error {e} \nretryng on {tries*tries} seconds")
              time.sleep(tries * tries)
            else:
              l.error("Too many retries failed")
              raise(e)
            
        ret.update({t.id_str:{"id":t.id_str, "text":t.text, "created_at":t.created_at.isoformat(), "lang":t.lang} for t in res})
        if j % 5 == 0 and j > 0:
          l.debug(f"{i} tweets rehydrated from {len(ids)}")
        i = i + 100
        j = j + 1
        # spleepling if less than 0.5 secs has happened
        pending = time.time() - start
        if pending < 0.5:
          time.sleep(pending)

      l.debug(f"{i} tweets rehydrated from {len(ids)}")
      return ret

    def create_new_gz(self):
       lfile = f"{datetime.now().strftime('%Y.%m.%d.%H.%M.%S')}.json.gz"
       path = util.pandem_path("files", "twitter", "v1.1", "tweets", lfile)
       l.info(f"Creating new file {lfile} for storing new tweets")
       open(path, 'a').close()
       return lfile
    
    def new_files(self, dls, last_hash):
        # testing if we need to replay files
        replay = False
        if os.path.exists(self._replay_dir):
          files_to_replay = glob.glob(f"{self._replay_dir}/**/*.json.gz", recursive = True)
          if len(files_to_replay) > 0:
            # testing if pipeline is not full if so the file will not be sent
            twitter_steps = self._storage_proxy.read_db('job', lambda j:j.status == 'in progress' and j.source == 'twitter').get()["step"]
            saturated = len(twitter_steps) > len(twitter_steps.unique())
            if saturated:
              return {"hash":last_hash, "files":[]}  
            else:
              to_archive = files_to_replay[0]
              to_arc = os.path.split(to_archive)[1]
              l.debug(f"replaying twitter file {to_arc}")
              arc = os.path.join(self._filter_arc_dir, to_arc[0:10])
              os.makedirs(arc, exist_ok = True)
              dest = os.path.join(arc, to_arc)
              os.rename(to_archive, dest)
              current_hash = to_arc
              return {"hash":to_archive, "files":[dest]}  


        existing_files = list(filter(lambda f: f.endswith(".json.gz"), os.listdir(self._filter_dir)))
        # files to archive which are those with a name alphabetically lesser or equal than the current hash
        if last_hash is not None and last_hash !=  "":
          to_archive = list(filter(lambda v: v <=last_hash, existing_files))
        else: 
          to_archive = []
       
        # deleting files already processed
        for to_arc in to_archive:
          arc = os.path.join(self._filter_arc_dir, to_arc[0:10])
          os.makedirs(arc, exist_ok = True)
          os.rename(os.path.join(self._filter_dir, to_arc), os.path.join(arc, to_arc))
          l.debug(f"old file {to_arc} has been archived")

        # files to pipeline are thise with a name alphabetically bigger than the current hash
        files_to_pipeline = list(filter(lambda v: v > last_hash and os.path.getsize(os.path.join(self._filter_dir, v)) > 0, existing_files))
        files_to_pipeline.sort(reverse = False) 
        if len(files_to_pipeline) > 0:
          current_hash = files_to_pipeline[-1]
        else : 
          current_hash = ""
        # adding full path
        files_to_pipeline = list([os.path.join(self._filter_dir, f) for f in files_to_pipeline])
        # creating the new file and waiting until a first write is done to be sure than the previous files are not updated anymore
        new_name = self.create_new_gz()
        new_file = os.path.join(self._filter_dir, new_name)
        new_size = os.path.getsize(new_file)
        while new_size == 0:
          l.debug("Waiting 1 second to see if the new tweet file is being filled")
          time.sleep(1)
          new_size = os.path.getsize(new_file)
        l.debug("New tweet file contais data. Sending previous files to pipeline")
          
        return {"hash":current_hash, "files":files_to_pipeline}  

    class TwitterFilter(tweepy.Stream):
      def __init__(self, track, included_regex, excluded_regex, include_retweets, topic_groups, languages, filter_dir,
            consumer_key, consumer_secret, access_token, access_token_secret, *args, chunk_size=512, max_retries=inf, proxy=None, verify=True
          ): 
        self._track = track
        self._included_regex = included_regex
        self._excluded_regex = excluded_regex
        self._include_retweets = include_retweets
        self._topic_groups = topic_groups
        self._languages = languages
        self._filter_dir = filter_dir
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret, *args, chunk_size=chunk_size, daemon=False, max_retries=max_retries, proxy=proxy, verify=verify)

      def run(self):
        try:
          while(True) :
            l.debug("Launching twitter track")
            l.debug(f"tracking: {self._track}")
            l.debug(f"languages{self._languages}")
            l.debug(f"included regex {self._included_regex}")
            l.debug(f"excluded regex {self._excluded_regex}")
            l.debug(f"topic groups {self._topic_groups}")
            l.debug(f"include retweets {self._include_retweets}")
            self.filter(follow=None, track=self._track, locations=None, filter_level=None, languages=self._languages, stall_warnings=False)
            l.warning("Tweet filter failed, trying again in 1 minute")
            time.sleep(60)
        except Exception as e: 
          l.error(str(e))
      
      def on_status(self, status):
        if hasattr(status, "retweeted_status"):
          if not self._include_retweets:
            text = None
          elif hasattr(status.retweeted_status, "extended_tweet") and "full_text" in status.retweeted_status.extended_tweet:
            text = status.retweeted_status.extended_tweet["full_text"]
          else: 
            text = status.retweeted_status.text
        elif hasattr(status, "extended_tweet") and "full_text" in status.extended_tweet:
          text = status.extended_tweet["full_text"]
        else: 
          text = status.text
        if text is not None:
          file_name = self.get_gz_file()
          file_path = os.path.join(self._filter_dir, file_name)
          reporting_date = str(datetime.strptime(file_name, '%Y.%m.%d.%H.%M.%S.json.gz'))
          res = {
            "id":status.id_str,
            "created_at":str(status.created_at),
            "lang":status.lang,
            "text":text,
            "reporting_time": reporting_date,
            "article_count": 1
          }
          
          for t in self.matching_topics(text):
            if t in self._topic_groups:
              col_name = f"topic_{self._topic_groups[t]}"
            else:
              col_name = "topic"
            if col_name in res:
              res[col_name].append(t)
            else:
              res[col_name] = [t]

          with gzip.GzipFile(file_path, 'a') as fout:
            fout.write(f"{json.dumps(res)}\n".encode('utf-8')) 

      def get_gz_file(self):
        files = list(filter(lambda f: f.endswith(".json.gz"), os.listdir(self._filter_dir)))
        if len(files)==0:
          raise ValueError("Could not find any file to save the tweets")
        else:
          files.sort(reverse=True)
          return files[0]
     
      def matching_topics(self, text):
        return list(filter(
          lambda topic: re.search(self._included_regex[topic], text.lower()) is not None and re.search(self._excluded_regex, text.lower()) is None,
          self._included_regex.keys()
        ))


    # methods for dataset post process

