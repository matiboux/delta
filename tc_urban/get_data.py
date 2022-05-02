import pandas as pd

# get Indicators.csv: https://www.kaggle.com/datasets/kaggle/world-development-indicators?select=Indicators.csv
# get countries_continents_codes_flags_url.csv : https://www.kaggle.com/datasets/andreshg/countries-iso-codes-continent-flags-url?resource=download&select=countries_continents_codes_flags_url.csv

indicators_df = pd.read_csv("data/Indicators.csv")
countries_df = pd.read_csv("data/countries_continents_codes_flags_url.csv")

# Clean the countries dataframe
countries_df = countries_df[['country', 'alpha-3', 'region']]
countries_df.rename(columns = {'country': 'CountryName', 'alpha-3': 'CountryCode', 'region': 'RegionName'}, inplace = True)

# Clean the indicators dataframe

# Keep only the good indicators for us :
#   - CO2 emission : EN.ATM.CO2E.KT
#   - Total population : SP.POP.TOTL
#   - Rural population : SP.RUR.TOTL
#   - Urban population : SP.URB.TOTL
indicators_df = indicators_df[(indicators_df.IndicatorCode == "SP.POP.TOTL") |
    (indicators_df.IndicatorCode == "SP.RUR.TOTL") |
    (indicators_df.IndicatorCode == "SP.URB.TOTL") |
    (indicators_df.IndicatorCode == "EN.ATM.CO2E.KT")]

# With a five years step
indicators_df = indicators_df[indicators_df.Year % 5 == 0]

# Get a clean dataframe
indicators_df['CO2 emissions (kt)'] = indicators_df.apply(lambda row: (row.Value, 0)[row.IndicatorCode != "EN.ATM.CO2E.KT"], axis = 1)
indicators_df['Total population'] = indicators_df.apply(lambda row: (row.Value, 0)[row.IndicatorCode != "SP.POP.TOTL"], axis = 1)
indicators_df['Rural population'] = indicators_df.apply(lambda row: (row.Value, 0)[row.IndicatorCode != "SP.RUR.TOTL"], axis = 1)
indicators_df['Urban population'] = indicators_df.apply(lambda row: (row.Value, 0)[row.IndicatorCode != "SP.URB.TOTL"], axis = 1)

indicators_df = indicators_df.drop(['IndicatorName', 'IndicatorCode', 'Value'], axis = 1)
indicators_df = indicators_df.groupby(['Year', 'CountryCode', 'CountryName'], as_index=False).sum()

# Remove line where there is no CO2 information
indicators_df = indicators_df[indicators_df['CO2 emissions (kt)'] != 0]

# Main dataframe
df = pd.merge(indicators_df, countries_df, on = ["CountryCode", "CountryName"])
RegionName_Column = df.pop("RegionName")
df.insert(3, 'RegionName', RegionName_Column)

df.to_pickle('data/countriesData.pkl')