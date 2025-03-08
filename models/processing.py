import sys
import pandas as pd
import hashlib

# Lire le fichier CSV depuis l'entrée standard
df = pd.read_csv(sys.stdin)

# 1️⃣ Anonymisation des données sensibles
def anonymize(text):
    return hashlib.sha256(text.encode()).hexdigest()[:10] if pd.notna(text) else text

df['Nom'] = df['Nom'].apply(anonymize)
df['Prénom'] = df['Prénom'].apply(anonymize)
df['Email'] = df['Email'].apply(lambda x: "user" + str(hash(x) % 10000) + "@exemple.com" if pd.notna(x) else x)
df['Adresse'] = df['Adresse'].apply(anonymize)

# 2️⃣ Pseudonymisation des identifiants
df['ClientID'] = df['ClientID'].apply(lambda x: hashlib.md5(x.encode()).hexdigest())

# 3️⃣ Création de nouvelles colonnes pour la visualisation
df['MontantTotalDépensé'] = df['MontantTotalAchats'] - df['MontantTotalRemboursé']
df['ClientFidèle'] = df['NombreAchats'].apply(lambda x: 'Oui' if x > 5 else 'Non')

# Exporter les données transformées vers stdout
df.to_csv(sys.stdout, index=False)
