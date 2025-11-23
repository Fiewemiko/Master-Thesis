import pandas as pd


# Wczytaj wszystkie trzy pliki CSV
df_2023 = pd.read_csv('csv ze stron/money_pl_2023.csv')
df_2022 = pd.read_csv('csv ze stron/money_pl_2022.csv')
df_2021 = pd.read_csv('csv ze stron/money_pl_2021.csv')

# Połącz wszystkie dataframe'y
df_combined = pd.concat([df_2023, df_2022, df_2021], ignore_index=True)

# Usuń duplikaty jeśli istnieją (na podstawie URL)
df_combined = df_combined.drop_duplicates(subset=['url'], keep='first')

# Sortuj po dacie (od najnowszych)
df_combined['google_detected_date'] = pd.to_datetime(df_combined['google_detected_date'])
df_combined = df_combined.sort_values('google_detected_date', ascending=False)

# Zapisz połączony plik
df_combined.to_csv('csv ze stron/money_pl_combined.csv', index=False)

print(f"Połączono pliki. Łączna liczba rekordów: {len(df_combined)}")
print(f"Po usunięciu duplikatów: {len(df_combined)}")
