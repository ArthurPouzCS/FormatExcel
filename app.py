import streamlit as st
import pandas as pd
import re
import datetime
import json

# --- 1. Définition des colonnes cibles et leurs validateurs ---
# Définition des catégories et leurs colonnes
COLUMN_CATEGORIES = {
    "InfosBSD1": [
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
        'nomInstallationDestination',
        'siretInstallationDestination',
        'adresseInstallationDestination',
        'codePostalInstallationDestination',
        'communeInstallationDestination',
        'numeroCap',
        'codeTraitementPrevuInstallationDestination'
    ],
    "InfosBSD2": [
        'nomTransporteur',
        'siretTransporteur',
        'adresseTransporteur',
        'codePostalTransporteur',
        'communeTransporteur',
        'recepisseTransporteur',
        'dateCollecteTransporteur',
        'codeCed',
        'descDechet',
        'codeONU',
        'consistance',
        'quantiteCollecteTransporteur'
    ],
    "InfosBSD3": [
        'mentionAdr',
        'pop',
        'isDangerous'
    ],
    "InfosNonTrackdechets": [
        'descContenant',
        'typeContenant',
        'volumeUnitaire',
        'uniteMesureVolume'
    ],
    "InfosFinancieres": [
        'coutsPreparationHT',
        'coutsTransportHT',
        'coutsTraitementHT',
        'coutGlobal',
        'rachatTotalHT',
        'equivalentCoutsContenantsHT',
        'coutsMiseDispo',
        'coutsMaintenance',
        'coutsContenantAutres',
        'autresCoutsHT',
        'coutsNonExpliques',
        'coutsPenalites',
        'coutsDeclassement',
        'coutsTGAP',
        'montantTotalHT'
    ]
}

# Colonnes obligatoires
REQUIRED_COLUMNS = [
    'siretEmetteur',
    'codeTraitementPrevuInstallationDestination',
    'dateCollecteTransporteur',
    'codeCed',
    'quantiteCollecteTransporteur'
]

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
st.title("📝 Mapping et Validation d'Excels")

# Importer plusieurs fichiers Excel
uploaded_files = st.file_uploader("📂 Importer un ou plusieurs fichiers Excel", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    # Initialiser les dictionnaires de mapping dans la session state
    if 'column_mappings' not in st.session_state:
        st.session_state.column_mappings = {}
    if 'selectors' not in st.session_state:
        st.session_state.selectors = {}
    if 'dfs' not in st.session_state:
        st.session_state.dfs = {}
    if 'mapped_dfs' not in st.session_state:
        st.session_state.mapped_dfs = {}

    # Créer un onglet pour chaque fichier
    tabs = st.tabs([f"Fichier {i+1}" for i in range(len(uploaded_files))])

    for i, (tab, uploaded_file) in enumerate(zip(tabs, uploaded_files)):
        with tab:
            st.subheader(f"📄 Fichier {i+1}: {uploaded_file.name}")
            
            # Charger le fichier si pas déjà fait
            if i not in st.session_state.dfs:
                st.session_state.dfs[i] = pd.read_excel(uploaded_file)
                st.write("✅ Fichier chargé avec succès !")

            # Afficher les colonnes originales
            st.subheader("📌 Colonnes originales du fichier :")
            original_columns = st.session_state.dfs[i].columns.tolist()
            st.write(original_columns)

            # Interface de mapping des colonnes par catégorie
            st.subheader("🔄 Mapping des colonnes")
            
            # Générer le prompt pour ChatGPT
            # Filtrer les colonnes Unnamed
            filtered_columns = [col for col in original_columns if not str(col).startswith('Unnamed:')]
            prompt = f"""Fais le mapping entre les colonnes de ces deux fichiers Excel de déchets.

Colonnes cibles à mapper :
{', '.join(TARGET_COLUMNS)}

Colonnes sources disponibles :
{', '.join(filtered_columns)}

Colonnes obligatoires :
{', '.join(REQUIRED_COLUMNS)}

Renvoie un JSON sous cette forme :
[
  {{ "nom_colonne_cible": "nom_colonne_source" }},
  {{ "siretEmetteur": "SIRET Emetteur" }},
  {{ "codeCed": "Code CED" }}
]"""

            # Afficher le prompt
            st.markdown("### 🤖 Assistant de mapping automatique")
            st.markdown("1️⃣ Copiez ce prompt et envoyez-le à ChatGPT :")
            st.code(prompt, language="text")
            
            # Zone de texte pour la réponse de ChatGPT
            st.markdown("2️⃣ Collez la réponse de ChatGPT ici :")
            chatgpt_response = st.text_area("Réponse JSON de ChatGPT", height=200, key=f"chatgpt_{i}")
            
            # Bouton pour appliquer le mapping automatique
            if st.button("🔄 Appliquer le mapping automatique", key=f"auto_map_{i}"):
                try:
                    # Parser la réponse JSON
                    mapping_data = json.loads(chatgpt_response)
                    
                    # Vérifier le format
                    if not isinstance(mapping_data, list):
                        st.error("❌ Format JSON invalide. La réponse doit être un tableau.")
                        st.stop()
                    
                    # Appliquer le mapping
                    st.session_state.column_mappings[i] = {}
                    for mapping in mapping_data:
                        for target_col, source_col in mapping.items():
                            if source_col in original_columns:
                                st.session_state.column_mappings[i][source_col] = target_col
                                # Mettre à jour les sélecteurs
                                is_required = target_col in REQUIRED_COLUMNS
                                display_name = f"{target_col} {'*' if is_required else ''}"
                                st.session_state.selectors[f"{i}_{source_col}"] = display_name
                    
                    st.success("✅ Mapping automatique appliqué avec succès !")
                    
                    # Afficher le résumé du mapping automatique
                    mapped_summary = pd.DataFrame(
                        [{"Colonne source": k, "Colonne cible": v} for k, v in st.session_state.column_mappings[i].items()]
                    )
                    st.markdown("### 📊 Résumé du mapping automatique")
                    st.dataframe(mapped_summary)
                    
                    # Forcer le rechargement de la page
                    st.experimental_rerun()
                    
                except json.JSONDecodeError:
                    st.error("❌ Format JSON invalide. Vérifiez la réponse de ChatGPT.")
                    st.stop()
                except Exception as e:
                    st.error(f"❌ Une erreur s'est produite : {str(e)}")
                    st.stop()

            st.markdown("### 📝 Mapping manuel")
            # Créer la liste des colonnes cibles avec leurs catégories
            target_columns_with_category = []
            for category, columns in COLUMN_CATEGORIES.items():
                for col in columns:
                    is_required = col in REQUIRED_COLUMNS
                    display_name = f"{col} {'*' if is_required else ''}"
                    target_columns_with_category.append(display_name)

            # Créer un layout en 4 colonnes
            col1, col2, col3, col4 = st.columns(4)
            columns = [col1, col2, col3, col4]
            
            # Diviser les colonnes originales en quatre groupes
            items_per_column = -(-len(original_columns) // 4)  # Arrondi supérieur
            
            # Distribuer les colonnes dans les colonnes de l'interface
            for j, column in enumerate(columns):
                start_idx = j * items_per_column
                end_idx = min((j + 1) * items_per_column, len(original_columns))
                
                with column:
                    for source_col in original_columns[start_idx:end_idx]:
                        # Obtenir des exemples de valeurs pour cette colonne
                        examples = st.session_state.dfs[i][source_col].dropna().head(2).tolist()
                        examples_str = f"<div style='color: gray; font-size: 0.8em; margin-top: -6px;'>{', '.join(str(ex) for ex in examples)}</div>" if examples else ""
                        
                        # Utiliser la valeur du sélecteur stockée dans la session state
                        options = [''] + target_columns_with_category
                        current_value = st.session_state.selectors.get(f"{i}_{source_col}", '')
                        try:
                            default_index = options.index(current_value) if current_value in options else 0
                        except ValueError:
                            default_index = 0
                        
                        # Afficher le label en gras et les exemples en gris dans un conteneur compact
                        st.markdown(f"""
                            <div style='margin-bottom: -10px; border-top : 1px solid #ccc; padding-top: 10px;'>
                                <div style='font-weight: bold;'>{source_col}</div>
                                {examples_str if examples else ''}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        selected_target = st.selectbox(
                            "",  # Label vide car on l'affiche au-dessus
                            options,  # Options (colonnes cibles)
                            key=f"select_{i}_{source_col}",
                            index=default_index  # Utiliser l'index pour la valeur par défaut
                        )
                        if selected_target:
                            # Enlever l'astérisque si présent pour le mapping
                            target_col = selected_target.split(' *')[0]
                            if i not in st.session_state.column_mappings:
                                st.session_state.column_mappings[i] = {}
                            st.session_state.column_mappings[i][source_col] = target_col
                            # Mettre à jour le sélecteur dans la session state
                            st.session_state.selectors[f"{i}_{source_col}"] = selected_target

            # Bouton pour valider le mapping de ce fichier
            if st.button("✨ Valider le mapping", key=f"validate_{i}"):
                # Vérifier les champs obligatoires
                missing_required = []
                for required_col in REQUIRED_COLUMNS:
                    if required_col not in st.session_state.column_mappings[i].values():
                        missing_required.append(required_col)
                
                if missing_required:
                    st.warning(f"⚠️ Les champs suivants sont obligatoires mais n'ont pas été mappés : {', '.join(missing_required)}")
                    st.info("Vous pouvez continuer le mapping, mais ces champs seront manquants dans le fichier final.")

                # Créer un DataFrame vide avec toutes les colonnes cibles
                df_mapped = pd.DataFrame(columns=TARGET_COLUMNS)
                
                # Remplir les colonnes mappées avec formatage
                for source_col, target_col in st.session_state.column_mappings[i].items():
                    if target_col in ['siretEmetteur', 'siretInstallationDestination', 'siretTransporteur']:
                        df_mapped[target_col] = st.session_state.dfs[i][source_col].apply(format_siret)
                    elif target_col in ['dateCollecteTransporteur']:
                        df_mapped[target_col] = st.session_state.dfs[i][source_col].apply(format_date)
                    elif target_col in ['quantiteCollecteTransporteur']:
                        df_mapped[target_col] = st.session_state.dfs[i][source_col].apply(format_number)
                    elif target_col == 'mentionAdr':
                        df_mapped[target_col] = st.session_state.dfs[i][source_col].fillna('').astype(str)
                        df_mapped['isSubjectToADR'] = df_mapped[target_col] == 'ADR'
                    elif target_col == 'pop':
                        df_mapped[target_col] = st.session_state.dfs[i][source_col].fillna('').astype(str)
                        df_mapped['pop'] = df_mapped[target_col] == 'O'
                    elif target_col == 'codeCed':
                        df_mapped[target_col] = st.session_state.dfs[i][source_col].fillna('').astype(str)
                        df_mapped['isDangerous'] = df_mapped[target_col].str.contains('*', regex=False)
                    else:
                        df_mapped[target_col] = st.session_state.dfs[i][source_col].fillna('').astype(str)
                
                # Stocker le DataFrame mappé
                st.session_state.mapped_dfs[i] = df_mapped
                st.success(f"✅ Mapping validé pour le fichier {i+1} !")
                
                # Afficher l'aperçu des données mappées
                st.subheader("📌 Aperçu des données après mapping :")
                # Filtrer le DataFrame pour ne garder que les colonnes mappées
                mapped_columns = set(st.session_state.column_mappings[i].values())
                df_mapped_preview = df_mapped[list(mapped_columns)]
                st.write(df_mapped_preview.head())

                # Validation des données
                st.subheader("🔍 Validation des données")
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
                    elif 'email' in target_col.lower():
                        is_valid = df_mapped[target_col].apply(validate_email)
                    elif 'telephone' in target_col.lower():
                        is_valid = df_mapped[target_col].apply(validate_phone)
                    elif 'codePostal' in target_col:
                        is_valid = df_mapped[target_col].apply(validate_postal_code)
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

    # Si tous les fichiers ont été mappés, afficher le bouton de concaténation
    if len(st.session_state.mapped_dfs) == len(uploaded_files):
        st.markdown("### 🔄 Concaténation des fichiers")
        if st.button("✨ Concaténer les fichiers mappés"):
            # Concaténer tous les DataFrames mappés
            final_df = pd.concat(st.session_state.mapped_dfs.values(), ignore_index=True)
            
            # Afficher un aperçu du fichier final
            st.subheader("📌 Aperçu du fichier final :")
            st.write(final_df.head())
            
            # Afficher les statistiques
            st.subheader("📊 Statistiques du fichier final :")
            st.write(f"Nombre total de lignes : {len(final_df)}")
            st.write(f"Nombre de colonnes : {len(final_df.columns)}")
            
            # Export du fichier final
            st.subheader("📥 Télécharger le fichier final")
            final_df.to_excel("output_final.xlsx", index=False)
            with open("output_final.xlsx", "rb") as file:
                st.download_button(
                    "📥 Télécharger le fichier Excel final",
                    file,
                    "output_final.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
