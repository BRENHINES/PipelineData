import sys
import pandas as pd
import numpy as np
import hashlib

# Lire le fichier CSV depuis l'entrée standard
dataset = pd.read_csv(sys.stdin)

# Anonymisation des données sensibles
def anonymize_name(name):
    """Anonymiser un nom ou prénom avec MD5"""
    return hashlib.md5(name.encode()).hexdigest() if pd.notna(name) else name

def anonymize_email(email):
    """Anonymiser une adresse email en masquant le nom d'utilisateur"""
    if pd.notna(email) and "@" in email:
        username = email.split('@')[0]
        hashed_username = hashlib.md5(username.encode()).hexdigest()
        return f"{hashed_username}@masked.com"
    return "masked@masked.com"

def pseudonymize_credit_card(card_number):
    """Pseudonymiser un numéro de carte bancaire en gardant les 4 derniers chiffres"""
    if pd.notna(card_number) and len(card_number) >= 4:
        return f"**** **** **** {card_number[-4:]}"
    return "**** **** **** ****"

"""
def pseudonymize_credit_card_expiration(expiration_date):
    ""Pseudonymiser la date d'expiration d'une carte bancaire en gardant les 2 derniers chiffres""
    if pd.notna(expiration_date) and len(expiration_date) >= 2:
        return expiration_date[-2:]
    return "**"
"""

def pseudonymize_postal_code(postal_code):
    """Pseudonymiser un code postal en gardant les 2 premiers chiffres et masquant le reste"""
    if pd.notna(postal_code) and len(postal_code) >= 2:
        return postal_code[:2] + "***"
    return "*****"

dataset['Nom'] = dataset['Nom'].apply(anonymize_name)
dataset['Prénom'] = dataset['Prénom'].apply(anonymize_name)
dataset['Email'] = dataset['Email'].astype(str).apply(anonymize_email)
dataset['Adresse'] = "masked"
dataset['Téléphone'] = "masked"

# Pseudonymisation des identifiants
dataset['NuméroCarteCrédit'] = dataset['NuméroCarteCrédit'].astype(str).apply(pseudonymize_credit_card)
dataset['DateExpirationCarte'] = dataset['DateExpirationCarte'].astype(str).apply(pseudonymize_credit_card_expiration)
dataset['CodePostal'] = dataset['CodePostal'].astype(str).apply(pseudonymize_postal_code)

# Aggregation des données d'age
bins = [0, 18, 25, 35, 45, 55, 65, 100]  # Intervalles d'âge
labels = ["0-18", "19-25", "26-35", "36-45", "46-55", "56-65", "65+"]  # Labels correspondants

dataset['CatégorieÂge'] = pd.cut(dataset['Âge'], bins=bins, labels=labels, right=True)  # Catégorisation des âges

# Suppression des colonnes inutiles
columns_to_delete = ['CodePostal', 'Nom', 'Prénom', 'Email', 'Adresse','Téléphone', 'DateNaissance', 'NuméroCarteCrédit', 'DateExpirationCarte', 'SoldeCompte']
dataset.drop(columns=[col for col in columns_to_delete if col in dataset.columns], inplace=True, errors='ignore')

# Suppression des enregistrements incohérents
if 'MontantTotalRemboursé' in dataset.columns and 'MontantTotalAchats' in dataset.columns:
    initial_count = len(dataset)
    dataset = dataset[dataset['MontantTotalRemboursé'] <= dataset['MontantTotalAchats']]
    removed_count = initial_count - len(dataset)

# 3️⃣ Création de nouvelles colonnes pour la visualisation
dataset['TauxRemboursement'] = np.where(dataset['MontantTotalAchats'] == 0,0,(dataset['MontantTotalRemboursé'] / dataset['MontantTotalAchats']) * 100)
dataset['MontantTotalDepensé'] = dataset['MontantTotalAchats'] - dataset['MontantTotalRemboursé']
dataset['AchatsSup5'] = dataset['NombreAchats'].apply(lambda x: 'True' if x > 5 else 'False')

bins = [0, 100, 500, 1000, 5000, float("inf")]
labels = ["Petit Acheteur", "Acheteur Régulier", "Bon Client", "Gros Acheteur", "VIP"]

dataset['CatégorieClient'] = pd.cut(dataset['MontantTotalAchats'].fillna(0), bins=bins, labels=labels, right=False)

# Exporter les données transformées vers stdout
dataset.to_csv(sys.stdout, index=False)
