import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from utils.config import WAVE_YEAR, TIME_SERIES_TRUST_ENC

def mma(df: pd.DataFrame, columns: list[str], country_col = "B_COUNTRY") -> pd.Series:
  """
  This function does a three step aggregation on columns
  
  1. Median imputation 
  2. MinMax scaling
  3. Rowwise averaging

  CAUTION: THIS FUNCTION HAS SIDE-EFFECTS
  """
  # 1. imputing with median --------------------------------------------
  # create a median dict with all the relevant values
  median_dict = {}
  countries = df[country_col].unique()

  for ct in countries:
      median_dict[ct] = {}

  for q in columns:
      for ct in countries:
          median_dict[ct][q] = df.loc[(df[q] > 0) & (df[country_col] == ct), q].median()
  
  # now populate the dataframe with the median values
  for q in columns:
      df[q] = df.loc[:, [q, country_col]].apply(lambda row: median_dict[row[country_col]][q] if row[q] <= 0 else row[q], axis=1)
    
  # 2. Minmax scaling --------------------------------------------
  scaler = MinMaxScaler()
  scaler.fit(df.loc[:, columns])
  df.loc[:, columns] = scaler.transform(df.loc[:, columns])

  # 3. Creating trust indeces by rowwise mean --------------------------------------------
  return df.loc[:, columns].mean(axis=1)


def attach_dummies(df: pd.DataFrame, col: str, prefix: str) -> pd.DataFrame:
  """
  Inplace appending of dummy variables onto the dataframe

  Basically just a wrapper to make the whole command more readable.
  """
  return pd.concat([df, pd.get_dummies(df[col], dtype=int, prefix=prefix)], axis=1)

def attach_regressors(cs:pd.DataFrame) -> None:
  """
  Attaches regressors to cross sectional data

  Is an inplace function with intended side-effects.
  """
  # Reverse the scale for hardships questions
  hardships_questions = [f"Q{i}" for i in range(51, 56)]
  for hq in hardships_questions:
      cs[hq] = cs[hq].where(cs[hq] <= 0, 4 + 1 - cs[hq])

  cs["national_distrust_index"] = mma(cs, [f"Q{i}" for i in range(64, 82)])

  cs["group_corruption"] = mma(cs, [f"Q{i}" for i in range(113, 117)])
  cs["migration_positive"] = mma(cs, ["Q122","Q123","Q125","Q127"])
  cs["migration_negative"] = mma(cs, ["Q124","Q126","Q128","Q129"])
  cs["security_neighborhood"] = mma(cs, [f"Q{i}" for i in range(132, 139)])
  cs["security_financial"] = mma(cs, ["Q142", "Q143"])
  cs["security_war"] = mma(cs, [f"Q{i}" for i in range(146, 149)])
  cs["hardships_questions"] = mma(cs, hardships_questions)

  cs["is_immigrant"] = (cs.Q263 == 2).astype(int)
  cs["mother_immigrant"] = (cs.Q264 == 2).astype(int)
  cs["father_immigrant"] = (cs.Q265 == 2).astype(int)
  
  for q, pre in zip(["Q240", "Q46", "B_COUNTRY_ALPHA"], ["pol_value", "happ_", "country"]):
    cs = pd.concat([cs, pd.get_dummies(cs[q], dtype=int, prefix=pre)], axis=1)
    
  cs["above_avg_inc"] = (cs.Q288 > cs.Q288.mean()).astype(int)
  cs["wpfi"] = cs.wpfi_rank / 100
  cs.rename(columns={"Q262": "age"}, inplace=True)
  cs["gender"] = (cs.Q260 == 1).astype(int)
  cs.rename(columns={"A_YEAR": "year"}, inplace=True)
  cs["year^2"] = cs.year**2
  cs["age_std"] = (cs.age - cs.age.mean())/ cs.age.std()
  cs["age_std^2"] = cs.age_std**2 

  return cs

def attach_timeseries_regressors(ts: pd.DataFrame) -> None:
  ts["national_distrust_index"] = mma(ts, TIME_SERIES_TRUST_ENC, "COUNTRY_ALPHA")
  ts.rename(columns={"S002VS": "wave"}, inplace=True)
  return ts