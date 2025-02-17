import pandas as pd

from utils.config import TIME_SERIES_TRUST_ENC, COUNTRIES_ISO

def get_data():
  # read in cross sectional with the configured western developed countries only
  cs = pd.read_csv("data/wvs/WVS_Cross_National.csv").query("B_COUNTRY_ALPHA in @COUNTRIES_ISO")
  
  # read in time series only german and only trust enc and wave and all the needed features
  ts = pd.read_csv("data/wvs/WVS_Time_Series.csv").query("COUNTRY_ALPHA == 'DEU'")[[*TIME_SERIES_TRUST_ENC, "S002VS", "COUNTRY_ALPHA"]]
  
  wpf = pd.read_excel('data/additional/RWB-PFI.xlsx')

  return cs, ts, wpf