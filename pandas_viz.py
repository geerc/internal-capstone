import pandas as pd

df_mens = pd.read_csv("data/MTeams.csv")

df_cities = pd.read_csv("data/Cities.csv")


print(df_mens)
print(df_cities)
df_cities.head()

df_cities.describe()

df_cities.drop_duplicates()
df_cities.dropna()

string_columns = df_cities.select_dtypes(include=['object']).columns
df_cities[string_columns] = df_cities[string_columns].apply(lambda x: x.str.strip())