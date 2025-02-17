import pandas as pd

def get_row_selection_cross_sectional(cs: pd.DataFrame) -> pd.Series:
  valid_immigration_status = (cs["Q263"] > 0) & (cs["Q264"] > 0) & (cs["Q265"] > 0)
  valid_age = cs["Q262"] > 0
  valid_gender = cs["Q260"] > 0
  valid_happiness = cs['Q46'] > 0
  valid_income = cs["Q288"] > 0 
  valid_pol_ref = cs["Q240"] > 0

  cross_sectional_row_cond = valid_immigration_status & valid_happiness & valid_age & valid_income & valid_pol_ref & valid_gender

  return cross_sectional_row_cond