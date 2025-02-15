import streamlit as st
import pandas as pd
import re
import datetime

# --- 1. Définition des colonnes cibles et leurs validateurs ---
# Définition des catégories et leurs colonnes
COLUMN_CATEGORIES = {
    "Document de référence": [
        'numeroBsd',
        'idSecondaire',
        'statutBordereauCode',
        'dateCreationBordereau',
        'dateModifBordereau'
    ],
    "Émetteur": [
        'nomSiteEmetteur',
        'siretEmetteur',
        'adresseEmetteur',
        'codePostalEmetteur',
        'communeEmetteur',
        'paysEmetteur',
        'prenomContactEmetteur',
        'nomContactEmetteur',
        'telephoneContactEmetteur',
        'emailContactEmetteur',
        'nomPointCollecte',
        'adresseCollecte',
        'codePostalCollecte',
        'communeCollecte',
        'infosCollecte'
    ],
    "Déchets": [
        'codeCed',
        'descDechet',
        'mentionAdr',
        'codeONU',
        'consistance',
        'pop'
    ],
    "Contenants": [
        'typeContenant',
        'descContenant',
        'nbContenants',
        'quantiteCollecteTransporteur',
        'quantiteEstimeeReelleTransporteur',
        'volumeUnitaire',
        'uniteMesureVolume'
    ],
    "Transporteur": [
        'nomTransporteur',
        'siretTransporteur',
        'adresseTransporteur',
        'codePostalTransporteur',
        'communeTransporteur',
        'paysTransporteur',
        'prenomContactTransporteur',
        'nomContactTransporteur',
        'telephoneContactTransporteur',
        'emailTransporteur',
        'recepisseTransporteur',
        'departementTransporteur',
        'limiteValiditeTransporteur',
        'immatriculationTransporteur',
        'modeTransportTransporteur',
        'dateCollecteTransporteur'
    ],
    "Installation de destination": [
        'nomInstallationDestination',
        'siretInstallationDestination',
        'adresseInstallationDestination',
        'codePostalInstallationDestination',
        'communeInstallationDestination',
        'paysInstallationDestination',
        'prenomContactInstallationDestination',
        'nomContactInstallationDestination',
        'telephoneContactInstallationDestination',
        'emailContactInstallationDestination',
        'numeroCap',
        'codeTraitementPrevuInstallationDestination',
        'dateReceptionInstallationDestination',
        'quantiteReceptionneeNetInstallationDestination',
        'quantiteEstimeeReelleReceptionInstallationDestination',
        'quantiteRefuseeInstallationDestination',
        'codeTraitementRealiseInstallationDestination',
        'qualificationTraitementInstallationDestination',
        'dateTraitementInstallationDestination',
        'ruptureTracabiliteInstallationDestination',
        'ruptureTracabiliteInstallationIntermediaire',
        'ruptureTracabiliteInstallationDestination2'
    ],
    "Éco-organisme": [
        'nomEcoOrganisme',
        'siretEcoOrganisme'
    ]
}

# Créer TARGET_COLUMNS à partir des catégories
TARGET_COLUMNS = []
for category_columns in COLUMN_CATEGORIES.values():
    TARGET_COLUMNS.extend(category_columns)

# --- 2. Fonctions de validation pour chaque type de colonne ---
def validate_siret(value):
    """Valide un numéro SIRET"""
    if pd.isna(value):
        return True
    value = str(value).strip()
    value = ''.join(filter(str.isdigit, value))
    return len(value) == 14

def format_siret(value):
    """Formate un SIRET en string de 14 chiffres"""
    if pd.isna(value):
        return ''
    value = str(value).strip()
    value = ''.join(filter(str.isdigit, value))
    return value if len(value) == 14 else ''

def validate_number(value):
    """Valide si la valeur peut être convertie en nombre"""
    if pd.isna(value):
        return True
    try:
        if isinstance(value, (int, float)):
            return True
        value_str = str(value).strip().replace(' ', '').replace(',', '.')
        float(value_str)
        return True
    except ValueError:
        return False

def format_number(value):
    """Formate un nombre en string avec virgule pour les décimaux"""
    if pd.isna(value):
        return ''
    try:
        if isinstance(value, (int, float)):
            return f"{value}".replace('.', ',')
        value_str = str(value).strip().replace(' ', '')
        if ',' in value_str:
            value_str = value_str.replace(',', '.')
        number = float(value_str)
        return f"{number}".replace('.', ',')
    except ValueError:
        return ''

def validate_date(value):
    """Valide si la valeur peut être convertie en date"""
    if pd.isna(value):
        return True
    try:
        if isinstance(value, (pd.Timestamp, datetime.datetime)):
            return True
        pd.to_datetime(str(value))
        return True
    except:
        return False

def format_date(value):
    """Formate une date en dd/mm/yyyy"""
    if pd.isna(value):
        return ''
    try:
        if isinstance(value, (pd.Timestamp, datetime.datetime)):
            return value.strftime('%d/%m/%Y')
        date = pd.to_datetime(str(value))
        return date.strftime('%d/%m/%Y')
    except:
        return ''

def validate_string(value):
    """Valide que la valeur est bien une chaîne de caractères"""
    if pd.isna(value):  # Accepte les valeurs vides
        return True
    return isinstance(str(value), str)

def validate_email(value):
    """Valide une adresse email"""
    if not value:
        return True
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value))

def validate_phone(value):
    """Valide un numéro de téléphone"""
    if not value:
        return True
    value = str(value).replace(' ', '')
    return bool(re.match(r'^(\+33|0)[1-9][0-9]{8}$', value))

def validate_postal_code(value):
    """Valide un code postal français"""
    if not value:
        return True
    return bool(re.match(r'^[0-9]{5}$', str(value)))

def validate_quantity(value):
    """Valide une quantité"""
    if not value:
        return True
    try:
        float(str(value).replace(',', '.'))
        return True
    except:
        return False

# Dictionnaire associant chaque colonne à sa fonction de validation
VALIDATION_FUNCTIONS = {
    # Validation des SIRET
    'siretEmetteur': validate_siret,
    'siretInstallationDestination': validate_siret,
    'siretTransporteur': validate_siret,
    'siretNegotiant': validate_siret,
    'siretCourtier': validate_siret,
    'siretEcoOrganisme': validate_siret,
    
    # Validation des quantités
    'quantiteCollecteTransporteur': validate_number,
    'quantiteReceptionneeNetInstallationDestination': validate_number,
    'quantiteRefuseeInstallationDestination': validate_number,
    'nbContenants': validate_number,
    'volumeUnitaire': validate_number,
    
    # Validation de la date de collecte (dd/mm/yyyy)
    'dateCollecteTransporteur': validate_date,
    
    # Toutes les autres colonnes doivent être des strings
    'numeroBsd': validate_string,
    'idSecondaire': validate_string,
    'statutBordereauCode': validate_string,
    'nomPointCollecte': validate_string,
    'adresseCollecte': validate_string,
    'codePostalCollecte': validate_string,
    'communeCollecte': validate_string,
    'infosCollecte': validate_string,
    'nomSiteEmetteur': validate_string,
    'adresseEmetteur': validate_string,
    'codePostalEmetteur': validate_string,
    'communeEmetteur': validate_string,
    'paysEmetteur': validate_string,
    'prenomContactEmetteur': validate_string,
    'nomContactEmetteur': validate_string,
    'telephoneContactEmetteur': validate_string,
    'emailContactEmetteur': validate_string,
    'prenomContactInstallationDestination': validate_string,
    'nomContactInstallationDestination': validate_string,
    'telephoneContactInstallationDestination': validate_string,
    'emailContactInstallationDestination': validate_string,
    'numeroCap': validate_string,
    'codeTraitementPrevuInstallationDestination': validate_string,
    'dateReceptionInstallationDestination': validate_string,
    'quantiteEstimeeReelleReceptionInstallationDestination': validate_string,
    'codeTraitementRealiseInstallationDestination': validate_string,
    'qualificationTraitementInstallationDestination': validate_string,
    'dateTraitementInstallationDestination': validate_string,
    'ruptureTracabiliteInstallationDestination': validate_string,
    'ruptureTracabiliteInstallationIntermediaire': validate_string,
    'ruptureTracabiliteInstallationDestination2': validate_string,
    'nomTransporteur': validate_string,
    'adresseTransporteur': validate_string,
    'codePostalTransporteur': validate_string,
    'communeTransporteur': validate_string,
    'paysTransporteur': validate_string,
    'prenomContactTransporteur': validate_string,
    'nomContactTransporteur': validate_string,
    'telephoneContactTransporteur': validate_string,
    'emailTransporteur': validate_string,
    'recepisseTransporteur': validate_string,
    'departementTransporteur': validate_string,
    'limiteValiditeTransporteur': validate_string,
    'immatriculationTransporteur': validate_string,
    'modeTransportTransporteur': validate_string,
    'codeCed': validate_string,
    'descDechet': validate_string,
    'mentionAdr': validate_string,
    'codeONU': validate_string,
    'typeContenant': validate_string,
    'descContenant': validate_string,
    'quantiteEstimeeReelleTransporteur': validate_string,
    'consistance': validate_string,
    'pop': validate_string,
    'uniteMesureVolume': validate_string,
    'parcelleCommuneEmetteur': validate_string,
    'parcelleCodePostalEmetteur': validate_string,
    'parcellePrefixSectionNumeroEmetteur': validate_string,
    'parcelleGPSEmetteur': validate_string,
    'refLaboEmetteur': validate_string,
    'idTerrainEmetteur': validate_string,
    'fichesTechniques': validate_string,
    'nomNegotiant': validate_string,
    'adresseNegotiant': validate_string,
    'codePostalNegotiant': validate_string,
    'communeNegotiant': validate_string,
    'paysNegotiant': validate_string,
    'prenomContactNegotiant': validate_string,
    'nomContactNegotiant': validate_string,
    'telephoneNegotiant': validate_string,
    'emailNegotiant': validate_string,
    'recipisseNegotiant': validate_string,
    'departementNegotiant': validate_string,
    'validiteNegotiant': validate_string,
    'nomCourtier': validate_string,
    'adresseCourtier': validate_string,
    'codePostalCourtier': validate_string,
    'communeCourtier': validate_string,
    'paysCourtier': validate_string,
    'prenomContactCourtier': validate_string,
    'nomContactCourtier': validate_string,
    'telephoneContactCourtier': validate_string,
    'emailCourtier': validate_string,
    'recipisseCourtier': validate_string,
    'departementCourtier': validate_string,
    'validiteCourtier': validate_string,
    #'nomEcoOrganisme': validate_string,
    'dateCreationBordereau': validate_string,
    'dateModifBordereau': validate_string
}

# Ajouter automatiquement la validation string pour toutes les colonnes non listées
for col in TARGET_COLUMNS:
    if col not in VALIDATION_FUNCTIONS:
        VALIDATION_FUNCTIONS[col] = validate_string

# --- 3. Interface utilisateur Streamlit ---
st.title("📝 Mapping et Validation d'un Excel")

# Importer un fichier Excel
uploaded_file = st.file_uploader("📂 Importer un fichier Excel", type=["xlsx"])

if uploaded_file:
    # Charger le fichier
    df = pd.read_excel(uploaded_file)
    st.write("✅ Fichier chargé avec succès !")

    # Afficher les colonnes originales
    st.subheader("📌 Colonnes originales du fichier :")
    original_columns = df.columns.tolist()
    st.write(original_columns)

    # Initialiser le dictionnaire de mapping
    column_mapping = {}

    # Interface de mapping des colonnes par catégorie
    st.subheader("🔄 Mapping des colonnes")
    
    for category, columns in COLUMN_CATEGORIES.items():
        st.markdown(f"### {category}")
        for target_col in columns:
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{target_col}**")
            
            with col2:
                selected_col = st.selectbox(
                    "",
                    [''] + original_columns,
                    key=f"select_{target_col}",
                    label_visibility="collapsed"
                )
                if selected_col:
                    column_mapping[selected_col] = target_col
            
            # Afficher des exemples si une colonne est sélectionnée
            with col3:
                if selected_col:
                    examples = df[selected_col].dropna().sample(n=min(2, len(df))).tolist()
                    st.write("📝 Exemples:", examples)

    if st.button("✨ Appliquer le mapping et valider"):
        # Créer un DataFrame vide avec toutes les colonnes cibles
        df_mapped = pd.DataFrame(columns=TARGET_COLUMNS)
        
        # Remplir les colonnes mappées avec formatage
        for source_col, target_col in column_mapping.items():
            if target_col in ['siretEmetteur', 'siretInstallationDestination', 'siretTransporteur', 
                             'siretNegotiant', 'siretCourtier', 'siretEcoOrganisme']:
                df_mapped[target_col] = df[source_col].apply(format_siret)
            elif target_col in ['dateCollecteTransporteur', 'dateCreationBordereau', 'dateModifBordereau',
                               'dateReceptionInstallationDestination', 'dateTraitementInstallationDestination',
                               'limiteValiditeTransporteur', 'validiteNegotiant', 'validiteCourtier']:
                df_mapped[target_col] = df[source_col].apply(format_date)
            elif target_col in ['quantiteCollecteTransporteur', 'quantiteReceptionneeNetInstallationDestination',
                               'quantiteRefuseeInstallationDestination', 'nbContenants', 'volumeUnitaire']:
                df_mapped[target_col] = df[source_col].apply(format_number)
            else:
                df_mapped[target_col] = df[source_col].fillna('').astype(str)
        
        # Récupérer les colonnes mappées
        mapped_columns = set(column_mapping.values())
        
        # Afficher le résumé du mapping
        st.info(f"📊 {len(mapped_columns)} colonnes mappées sur {len(TARGET_COLUMNS)} colonnes disponibles")
        
        # Validation des données
        validation_summary = []
        format_errors = {}
        
        for target_col in df_mapped.columns:
            # Ne valider que les colonnes qui ont été mappées
            if target_col not in mapped_columns:
                continue
                
            if target_col in ['siretEmetteur', 'siretInstallationDestination', 'siretTransporteur']:
                is_valid = df_mapped[target_col].apply(validate_siret)
            elif 'date' in target_col.lower():
                is_valid = df_mapped[target_col].apply(validate_date)
            elif any(word in target_col.lower() for word in ['quantite', 'volume', 'nb']):
                is_valid = df_mapped[target_col].apply(validate_number)
            else:
                is_valid = df_mapped[target_col].notna()

            nb_total = len(df_mapped[target_col])
            nb_valides = is_valid.sum()
            nb_invalides = nb_total - nb_valides
            nb_vides = df_mapped[target_col].isna().sum()

            validation_summary.append({
                "Colonne": target_col,
                "Total": nb_total,
                "Valides": nb_valides,
                "Invalides": nb_invalides,
                "Vides": nb_vides,
                "Taux de validité": f"{(nb_valides/nb_total)*100:.1f}%"
            })

            if nb_invalides > 0:
                format_errors[target_col] = df_mapped[~is_valid][target_col].tolist()
        
        # Affichage du tableau récapitulatif des validations
        if validation_summary:
            st.write("📊 Tableau récapitulatif des validations :")
            st.table(pd.DataFrame(validation_summary))
        
        # Affichage des erreurs détaillées
        if format_errors:
            st.error("❌ Détail des erreurs de format :")
            for col, values in format_errors.items():
                with st.expander(f"🔴 {col} - {len(values)} erreurs"):
                    st.write("Valeurs incorrectes :")
                    st.write(values)
                    if col in df_mapped.columns:
                        st.write("Exemples de valeurs valides :")
                        valid_examples = df_mapped[~df_mapped[col].isna()][col].head()
                        st.write(valid_examples.tolist())
        else:
            st.success("✅ Aucune erreur de format détectée !")

        # Affichage de l'aperçu des données mappées
        st.subheader("📌 Aperçu des données après mapping :")
        st.write(df_mapped.head())

        # Export du fichier modifié
        st.subheader("📥 Télécharger le fichier corrigé")
        df_mapped.to_excel("output.xlsx", index=False)
        with open("output.xlsx", "rb") as file:
            st.download_button(
                "📥 Télécharger le fichier Excel",
                file,
                "output.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
