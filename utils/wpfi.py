import pandas as pd

def clean_wpfi_wave(wpf: pd.DataFrame) -> pd.DataFrame:
  countries = ['AUS','CAN','DEU','NLD','USA']
  wpf = wpf[wpf['Economy ISO3'].isin(countries)]
  # Use rank instead of index because it is the same measurement over time
  # # Index changed around 2013 to be calculated completely differently
  wpf = wpf[wpf['Indicator ID'] != 'RWB.PFI.RANK']
  wpf = pd.concat([wpf.iloc[:, :2], wpf.iloc[:, -7:]], axis=1)
  main_columns = wpf.iloc[:, :2]  # First two column
  year_columns = wpf.iloc[:, -7:]  # Last seven columns
  # pivot the last seven columns into rows so that we can merge into broader d
  pivoted_df = pd.melt(
      wpf, 
      id_vars=main_columns.columns,  # Columns to keep (e.g., the first two columns)
      value_vars=year_columns.columns,  # Columns to pivot (e.g., the last seven columns)
      var_name='Year',  # Name of the new column that will hold column names
      value_name='wpfi_rank'  # Name of the new column that will hold the values
  )
  return pivoted_df

def merge_wave_wpfi(df: pd.DataFrame, pivoted_df: pd.DataFrame) -> pd.DataFrame:
  # Filter for Countries in "Western Europe" as defined by the European Union (https://eur-lex.europa.eu/browse/eurovoc.html?params=72,7206,913#arrow_913)
  countries = ['AUS','CAN','DEU','NLD','USA']
  # Belgium, Ireland, Liechtenstein, Luxembourg, and Monaco do not have data in wave 7
  df = df[df['B_COUNTRY_ALPHA'].isin(countries)]
  # Perform the left join on 'ISO' and 'Year'
  merged_df = pd.merge(
      df, 
      pivoted_df, 
      how='left', 
      left_on=['B_COUNTRY_ALPHA', 'A_YEAR'], 
      right_on=['Economy ISO3', 'Year']
  )
  return merged_df