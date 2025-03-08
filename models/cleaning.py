import sys
import pandas as pd
import numpy as np
import re

# Read the CSV file from stdin
dataset = pd.read_csv(sys.stdin)

# Missing values handling
missing_values = dataset.isnull().sum()

for col in dataset.columns:
    if dataset[col].isnull().sum() > 0:
        if dataset[col].dtype == 'O':
            dataset[col].fillna("Inconnu", inplace=True)
        else:
            dataset[col].fillna(dataset[col].median(), inplace=True)

# Duplicate rows handling
num_duplicates = dataset.duplicated().sum()
if num_duplicates > 0:
    sys.stderr.write(f"{num_duplicates} doublon(s) détecté(s) dans le dataset.\n")
    dataset.drop_duplicates(inplace=True)

# Détection des incohérences
incoherence_achats = dataset[(dataset['NombreAchats'] == 0) & (dataset['MontantTotalAchats'] > 0)]
incoherence_panier = dataset[(dataset['MontantTotalAchats'] == 0) & (dataset['PanierMoyen'] > 0)]
remboursements_invalides = dataset[dataset['MontantTotalRemboursé'] > dataset['MontantTotalAchats']]

sys.stderr.write(f"📌 Nombre de pages incohérentes (NombreAchats = 0 & MontantTotalAchats > 0) : {len(incoherence_achats)}\n")
sys.stderr.write(f"📌 Nombre de pages incohérentes (MontantTotalAchats = 0 & PanierMoyen > 0) : {len(incoherence_panier)}\n")
sys.stderr.write(f"📌 Nombre d'enregistrements où le MontantTotalRemboursé > MontantTotalAchats : {len(remboursements_invalides)}\n")

# Correction des incohérences
dataset.loc[(dataset['NombreAchats'] == 0) & (dataset['MontantTotalAchats'] > 0), 'NombreAchats'] = dataset['NombreAchats'].median()
dataset.loc[(dataset['PanierMoyen'] == 0) & (dataset['MontantTotalAchats'] > 0), 'MontantTotalAchats'] = dataset['MontantTotalAchats'].median()
dataset.loc[(dataset['MontantTotalAchats'] == 0) & (dataset['PanierMoyen'] > 0), 'PanierMoyen'] = 0

# Suppression des enregistrements invalides
dataset = dataset[dataset['MontantTotalRemboursé'] <= dataset['MontantTotalAchats']]


def standardise_date(date):
    """Convertir plusieurs formats de date en yyyy-mm-dd"""
    date = str(date).strip()

    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):  # yyyy-mm-dd
        return date
    elif re.match(r"^\d{2}/\d{2}/\d{4}$", date):  # mm/dd/yyyy
        match = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", date)
        return f"{match.group(3)}-{match.group(1)}-{match.group(2)}"
    elif re.match(r"^(\d{2})/(\d{2})$", date):  # mm/dd (année inconnue)
        match = re.match(r"^(\d{2})/(\d{2})$", date)
        return f"20{match.group(2)}-{match.group(1)}-01"  # On assume le 1er jour du mois
    elif re.match(r"^\d{2}-\d{2}-\d{4}$", date):  # dd-mm-yyyy
        match = re.match(r"^(\d{2})-(\d{2})-(\d{4})$", date)
        return f"{match.group(3)}-{match.group(2)}-{match.group(1)}"
    elif re.match(r"^\d{2}-\d{2}-\d{2}$", date):  # dd-mm-yy
        match = re.match(r"^(\d{2})-(\d{2})-(\d{2})$", date)
        return f"20{match.group(3)}-{match.group(2)}-{match.group(1)}"

    return date  # Si aucun format reconnu, on garde la valeur originale

# Standardisation des colonnes numériques (arrondi à 2 décimales)
columns_to_round = ['MontantTotalAchats', 'SoldeCompte', 'PanierMoyen', 'MontantTotalRemboursé']
for col in columns_to_round:
    if col in dataset.columns:
        dataset[col] = dataset[col].apply(lambda x: round(x, 2) if pd.notna(x) else x)

sys.stderr.write("Standardisation des valeurs numériques effectuée.\n")

# Standardisation des colonnes textuelles (`Pays`, `Ville`)
standardize_name_columns = ['Pays', 'Ville']
for col in standardize_name_columns:
    if col in dataset.columns:
        dataset[col] = dataset[col].str.title()  # Convertir en format standard (Ex: "france" → "France")

sys.stderr.write("Standardisation des noms de pays et villes effectuée.\n")

# Standardisation des dates (`DateNaissance`, `DernierAchat`, `DateExpirationCarte`)
standardize_date_columns = ['DateNaissance', 'DernierAchat', 'DateExpirationCarte']
for col in standardize_date_columns:
    if col in dataset.columns:
        dataset[col] = dataset[col].astype(str).apply(standardise_date)

sys.stderr.write("Standardisation des dates effectuée.\n")

# Standardisation des types des colonnes datetime
date_columns = ['DateNaissance', 'DernierAchat', 'DateExpirationCarte']
for col in date_columns:
    if col in dataset.columns:
        dataset[col] = pd.to_datetime(dataset[col], errors='coerce')  # Convertir en datetime64[ns], valeurs erronées mises à NaT

sys.stderr.write("Standardisation des dates effectuée.\n")

# Conversion des colonnes numériques (float et int)
numeric_columns = ['MontantTotalAchats', 'SoldeCompte', 'PanierMoyen', 'MontantTotalRemboursé', 'NombreAchats']
for col in numeric_columns:
    if col in dataset.columns:
        dataset[col] = pd.to_numeric(dataset[col], errors='coerce')  # Convertir en float ou int, erreurs mises à NaN

sys.stderr.write("Standardisation des nombres effectuée.\n")

# Conversion des colonnes texte
text_columns = ['ClientID', 'Nom', 'Prénom', 'Email', 'Adresse', 'Pays', 'Ville', 'ProduitPréféré']
for col in text_columns:
    if col in dataset.columns:
        dataset[col] = dataset[col].astype(str).fillna("Inconnu")  # Convertir en string

sys.stderr.write("Standardisation des colonnes texte effectuée.\n")

# Export the cleaned data to stdout
dataset.to_csv(sys.stdout, index=False)
