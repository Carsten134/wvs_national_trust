from utils.wpfi import clean_wpfi_wave, merge_wave_wpfi
from utils.feature_extraction import mma, attach_regressors, attach_timeseries_regressors
from utils.row_selection import get_row_selection_cross_sectional
from utils.data_loader import get_data
from utils.config import COUNTRIES_ISO, REGRESSORS

def run_preprocessing():
  
  # read in the data
  print("reading in the data...")
  cs, ts, wpf = get_data()

  # row selection
  print("running row selection...")
  cross_sectional_row_cond = get_row_selection_cross_sectional(cs)
  cs = cs.loc[cross_sectional_row_cond, :]
  
  # merge wpfi with cross sectional data
  print("merging wpfi with cross sectional data...")
  pivoted_wpfi = clean_wpfi_wave(wpf)
  processed_cs = merge_wave_wpfi(cs, pivoted_wpfi)

  # attach regressors to processed_cs
  print("running feature extraction...")
  processed_cs = attach_regressors(processed_cs)

  # attach trust index for time series data
  print("processing time series...")
  ts = attach_timeseries_regressors(ts)
  

  # save as csv
  print("finished, now saving processed data...")
  processed_cs[[*REGRESSORS,
                "wpfi",
                *[f"country_{i}" for i in COUNTRIES_ISO],
                "national_distrust_index",
                # additionally save all questions for later use
                *processed_cs.columns[processed_cs.columns.str.match(r"Q\d+")]]].to_csv("./data/wvs/wave7.csv", index=False)
  
  ts[["national_distrust_index", "wave"]].to_csv("./data/wvs/time_series.csv", index=False)


if __name__ == "__main__":
    run_preprocessing()