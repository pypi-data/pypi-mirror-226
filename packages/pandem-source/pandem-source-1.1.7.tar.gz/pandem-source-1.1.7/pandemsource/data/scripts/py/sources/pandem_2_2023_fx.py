import numpy as np
import pandas as pd
from datetime import date, timedelta
import random

INIT_DATE = date(2023, 10, 1)
max_indicators = ["people in hospital", "people in icu", "population"]
sum_indicators = ["cases", "hospitalisations", "deaths", "vaccination", "icu admissions"]
beds_capacity = ["number_of_icu_beds", "number_of_ward_beds"]
calc_indicators = ["number_of_beds", "people_in_ward"]

ward_capacity = {"DE":83000, "NL":17500}
icu_capacity = {"DE":2200, "NL":455}

country_pop = {"ES":47332614,"MT":514564,"BE":11522440,"CY":888005,"FR":67320216,"IT":59641488,"NL":17407585,"RO":19328838,"EE":1328976,"PL":37958138,"DE":83166711,"SE":10327589,"SI":2095861,"SK":5457873,"HU":9769526,"BG":6951482,"FI":5525292,"AT":8901064,"IE":4964440,"PT":10295909,"DK":5822763,"HR":4058165,"CZ":10693939,"LU":626108,"LV":1907675,"LT":2794090,"EL":10718565}

nuts_pop = {
  "DE":{"DE93":1710914,"DE11":4143418,"DE92":2149805,"DE80":1609675,"DEA1":5202321,"DEB3":2057952,"DE50":682986,"DE60":1841179,"DE23":1109269,"DEC0":990509,"DEA4":2055310,"DE13":2264469,"DEE0":2208321,"DE71":3998724,"DEB1":1495885,"DE24":1067482,"DE73":1219823,"DE40":2511917,"DEA3":2623619,"DE25":1770401,"DE27":1887754,"DE22":1238528,"DE94":2525333,"DE72":1047262,"DE14":1856517,"DE26":1317124,"DE91":1596396,"DEF0":2896712,"DED5":1043293,"DEB2":531007,"DE21":4686163,"DED4":1436445,"DE12":2805129,"DED2":1598199,"DEA2":4468904,"DEA5":3582497,"DEG0":2143145},
  "NL":{"NL42":1117201,"NL11":586009,"NL21":1081266,"NL23":423021,"NL33":3636552,"NL34":383488,"NL31":1354834,"NL32":2764017,"NL41":2401202,"NL12":649957,"NL22":2085952,"NL13":493682}
}

def df_transform(df: pd.DataFrame) -> pd.DataFrame:
    seed = 'pandem-2'
    # managing optional format
    if "model_val" not in df:
      df["model_val"] = df["synthetic_val"]
    
    print("..........Transforming data for thr 2023 FX")
    print("..............Adding two months of zero rows")
    df = add_previous_days(df, 60)
    print("..............Adding country level rows for other EU countries and EU level")
    df = add_other_countries(df, nuts_pop, country_pop, 20)
    print("..............Split  by NUTS-2")
    # implemeting split by nuts

    nuts_weights = {}
    for c in nuts_pop:
      nuts_weights[c] = {n:nuts_pop[c][n]/sum(nuts_pop[c].values()) for n in nuts_pop[c]}
    cuts = {
      11:["DE94", "NL22"],
      13:["E93", "DE50", "DE92", "DEA4", "DEA3", "NL41", "NL42", "NL33", "NL31", "NL23", "NL21"]
    }
    df = split_by_nuts(df,nuts_pop, nuts_weights, cuts, seed)

    # Generate the data for all ages
    print("..............Adding All ages")
    df = pd.concat([df.groupby(["Time", "country", "indicator"]).aggregate({"synthetic_val":"sum", "population":"sum"}).reset_index(), df], ignore_index = True)
    df["Age"] = ["ALL" if pd.isna(age) else age for age in df["Age"]]
    print("..............Normalize format")
    normalize_column_names(df)
    normalize_dates(df)
    print("..............Unpivot dataframe")
    df = split_interest_columns(df)
    print("..............Adding to weekly")
    df = daily_to_weekly(df)
    df["age"] = [age if age != "ALL" else None for age in df["age"]]
    print("..............Adding bed capacity")
    add_bed_capacity(df, nuts_weights, seed) 
    print("..............Adding calculated measures")
    add_calculated(df) 
    df['line_number'] = range(1, len(df)+1)
    return df


def normalize_column_names(df: pd.DataFrame):
    df.columns = map(str.lower, df.columns)
    df.rename(columns={"time": "date"}, inplace=True)


def normalize_dates(df: pd.DataFrame):
    df["date"] = [do_normalize_dates(date) for date in df["date"]]


def do_normalize_dates(days_since_init_date: str) -> str:
    return str(INIT_DATE + timedelta(days=days_since_init_date))


def split_interest_columns(df: pd.DataFrame) -> pd.DataFrame:
    indicators = [*max_indicators, *sum_indicators]
    df["indicator"] = [str.lower(indicator) for indicator in df["indicator"]]
    for ind in indicators:
      if ind != "population":
        df[ind.replace(" ", "_")] = get_interest_column(df, ind)
    # Combine rows with same date but different indicators
    df = (df.groupby(by=["date", "age", "country"])
      .aggregate({**{ind.replace(" ","_"):"sum" for ind in sum_indicators}, **{ind.replace(" ","_"):"max" for ind in max_indicators}})
      .reset_index()
    )
    return df

def get_interest_column(df, indicator) -> pd.Series:
    return df.apply(lambda row: do_split_interest_columns(row, indicator, "synthetic_val"), axis=1)

def do_split_interest_columns(row: pd.Series, indicator_name: str, base_col: str):
    return row[base_col] if row["indicator"] == indicator_name else np.nan

def daily_to_weekly(daily_data: pd.DataFrame) -> pd.DataFrame:
    daily_data['date'] = pd.to_datetime(daily_data['date'])
    daily_data = daily_data.set_index('date')
    weekly_data = (daily_data.groupby(['country', 'age', pd.Grouper(freq='W-MON')])
      .agg({**{ind.replace(" ","_"):"sum" for ind in sum_indicators}, **{ind.replace(" ","_"):"max" for ind in max_indicators}})
      .reset_index()
    )
    daily_data['period_type'] = 'date'
    daily_data.reset_index(inplace=True)
    weekly_data['period_type'] = 'isoweek'
    return pd.concat([weekly_data, daily_data], ignore_index=True)

def add_bed_capacity(df, nuts_weights, seed = None):
    icu_cap_nuts = {
      **icu_capacity,
      **{nut:weight for country in icu_capacity for nut, weight in weighted_distribution(icu_capacity[country], nuts_weights[country], seed).items() }
    }
    ward_cap_nuts = {
      **ward_capacity,
      **{nut:weight  for country in ward_capacity for nut, weight in weighted_distribution(ward_capacity[country], nuts_weights[country], seed).items()}
    }

    df["number_of_icu_beds"] = df.apply(lambda r: icu_cap_nuts.get(r["country"]) if pd.isna(r["age"]) else None, axis = 1)
    df["number_of_ward_beds"] = df.apply(lambda r: ward_cap_nuts.get(r["country"]) if pd.isna(r["age"]) else None, axis = 1)
    return df


def add_calculated(df):
    df["number_of_beds"] = df["number_of_icu_beds"] + df["number_of_ward_beds"]
    df["people_in_ward"] = df["people_in_hospital"] - df["people_in_icu"]
    return df

def add_previous_days(df, days):
  ref_time = 1
  rows = [] 
  for index, row in df.iterrows():
    if row['Time'] == ref_time:
      for d in range(-days, 0):
        rows.append({
          'Time':row['Time']+d,
          'Age':row['Age'],
          'model_val':row['model_val'],
          'synthetic_val':row['synthetic_val'],
          'indicator':row['indicator'],
          'country':row['country'],
          'population':row['population']
        })
  return pd.concat([pd.DataFrame(rows), df], ignore_index = True)


def add_other_countries(df, nuts_pop, country_pop, start_day):
  ref_pop = {c:sum(v.values()) for c, v in nuts_pop.items()}
  ref_countries = {c:{cc:pop for cc,pop in country_pop.items() if cc not in nuts_pop and  c == [*sorted([(ccc, abs(ref_pop[ccc] - pop)) for ccc in nuts_pop], key = lambda p:p[1])][0][0]} for c in nuts_pop}
  rows = []
  all_code = "EU"
  for index, row in df.iterrows():
    if row['country'] in ref_countries:
      cref = row['country']
      for c, cpop in ref_countries[cref].items():
          rows.append({
            'Time':row['Time'],
            'Age':row['Age'],
            'model_val':row['model_val'],
            'synthetic_val':int(row['synthetic_val']*cpop/ref_pop[cref]) if row['Time'] >= start_day else 0,
            'indicator':row['indicator'],
            'country':c,
            'population':int(row['population']*cpop/ref_pop[cref])
          })
  # Joining with other countries
  df =  pd.concat([df, pd.DataFrame(rows)], ignore_index = True)
  # Calculating all countries dataframe 
  alldf = df[df.country.isin(country_pop)].groupby(["Time", "Age", "indicator"]).agg({"model_val":"sum", "synthetic_val":"sum", "population":"sum"}).reset_index()
  alldf["country"] = all_code
  # joining with all 
  return pd.concat([df, alldf], ignore_index = True)


def split_by_nuts(df, nuts_pop, nuts_weights, cuts, seed = None):
  rows = [] 
  for index, row in df.iterrows():
    for c in nuts_pop:
      if row['country'] == c:
         cut = [i for i in cuts.keys() if row['Time'] <= i] if cuts is not None else []
         if len(cut) > 0:
           ic = min(cut)
           weights = {c:{n:(0 if n not in cuts[ic] else w/sum(ww for cc, ww in nuts.items() if cc in cuts[ic])) for n,w in nuts.items()} for c, nuts in nuts_weights.items()}
         else:
           weights = nuts_weights

         redis = weighted_distribution(row['synthetic_val'], weights[c], seed)
         for nut, pop in nuts_pop[c].items():
           rows.append({
             'Time':row['Time'],
             'Age':row['Age'],
             'model_val':row['model_val'],
             'synthetic_val':redis[nut],
             'indicator':row['indicator'],
             'country':nut,
             'population':pop
           })
  return pd.concat([df, pd.DataFrame(rows)], ignore_index = True)


def weighted_distribution(value, weights, seed = None):
  if seed is not None:
    random.seed(seed)
  limit = 10000
  parts = []
  while value / limit > 0:
    parts.append(value % limit)
    value = int(value / limit)
  res = {c:0 for c in weights}
  for i in range(0, len(parts)):
    redist = _weighted_distribution(parts[i], weights, sample = i == 0)
    for c, v in redist.items():
      res[c] = res[c] + pow(limit, i) * v
  return res

def _weighted_distribution(value, weights, sample = True):
  chunk = 5000
  wcodes = [*weights.keys()]
  ixs = [*range(0, len(wcodes))]
  if sample:
    iw = [weights[wcodes[i]] for i in ixs]
    res = [0 for c in ixs]
    while value > 0:
      to_dist = min(chunk, value)
      sampled = random.choices(ixs, weights = iw, k = to_dist)
      for i in sampled:
        res[i] = res[i] + 1
      value = value - to_dist
  else:
    res = [int(value * weights[c]) for c in wcodes]
    diff = value - sum(res)
    for i in range(0, diff):
      res[i%len(res)] = res[i%len(res)] + 1
  return {wcodes[i]:res[i] for i in ixs}

