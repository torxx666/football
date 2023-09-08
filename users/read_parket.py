import pandas as pd

# Spécifiez le chemin vers le fichier Parquet
# chemin_fichier_parquet = 'https://s3.amazonaws.com/aui-lab-data-engineer-resources/tweets/clubs-tweets.parquet'
chemin_fichier_parquet = 'clubs-tweets.parquet'

# Utilisez pandas pour lire le fichier Parquet depuis l'URL S3 public
df = pd.read_parquet(chemin_fichier_parquet)

# Affichez le contenu du DataFrame
print(df)
