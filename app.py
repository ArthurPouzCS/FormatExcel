import streamlit as st
import pandas as pd
import re
import datetime
import json
import os

# Configuration de la page en mode wide
st.set_page_config(layout="wide")

# Désactiver le cache
st.set_option('deprecation.showPyplotGlobalUse', False)
st.cache_data.clear()

# Charger les codes CED de référence
def load_ced_codes():
    """Charge les codes CED de référence depuis le fichier codes_ced.txt"""
    ced_codes = set()
    try:
        # Utiliser le chemin parent pour trouver le fichier
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ced_file_path = os.path.join(parent_dir, "codes_ced.txt")
        
        with open(ced_file_path, "r", encoding="utf-8") as f:
            for line in f:
                # Nettoyer la ligne et ajouter au set
                code = line.strip()
                if code:  # Ignorer les lignes vides
                    ced_codes.add(code)
    except Exception as e:
        st.error(f"Erreur lors du chargement des codes CED : {str(e)}")
    return ced_codes

def format_ced_code(code):
    """Formate un code CED en utilisant la référence"""
    if pd.isna(code):
        return ""
    
    # Convertir en string et nettoyer
    code = str(code).strip()
    # Enlever tous les espaces et astérisques
    clean_code = code.replace(" ", "").replace("*", "")
    
    # Chercher le code correspondant dans la référence
    for ref_code in CED_CODES:
        if ref_code.replace(" ", "").replace("*", "") == clean_code:
            return ref_code
    
    return code  # Retourner le code original si pas de correspondance trouvée

# Charger les codes CED au démarrage
CED_CODES = load_ced_codes()

# --- 1. Définition des colonnes cibles et leurs validateurs ---
# Définition des catégories et leurs colonnes
COLUMN_CATEGORIES = {
    "InfosBSD1": [
        'nomSiteEmetteur',
        'siretEmetteur',
        'adresseEmetteur',
        'emailContactEmetteur',
        'nomPointCollecte',
        'adresseCollecte',
        'nomInstallationDestination',
        'siretInstallationDestination',
        'adresseInstallationDestination',
        'numeroCap',
        'codeTraitementPrevuInstallationDestination'
    ],
    "InfosBSD2": [
        'nomTransporteur',
        'siretTransporteur',
        'adresseTransporteur',
        'recepisseTransporteur',
        'dateCollecteTransporteur',
        'codeCed',
        'descDechet',
        'codeONU',
        'consistance',
        'quantiteCollecteTransporteur'
    ],
    "InfosBSD3": [
        'pop',
    ],
    "InfosNonTrackdechets": [
        'descContenant',
        'volumeUnitaire',
        'uniteMesureVolume'
    ],
    "InfosFinancieres": [
        'coutsPreparationHT',
        'coutsTransportHT',
        'coutsTraitementHT',
        'coutGlobal',
        'rachatTotalHT',
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
    # Convertir en string et nettoyer
    value = str(value).strip()
    # Garder uniquement les chiffres
    value = ''.join(filter(str.isdigit, value))
    # Vérifier la longueur
    return len(value) == 14

def format_siret(value):
    """Formate un SIRET en string de 14 chiffres en préservant les zéros"""
    if pd.isna(value):
        return ''
    # Convertir en string et nettoyer
    value = str(value).strip()
    # Garder uniquement les chiffres
    value = ''.join(filter(str.isdigit, value))
    # Vérifier la longueur
    if len(value) == 14:
        return value
    return ''

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
                # Lire le fichier Excel en forçant le format texte pour toutes les colonnes
                st.session_state.dfs[i] = pd.read_excel(
                    uploaded_file,
                    dtype=str  # Force toutes les colonnes en format texte
                )
                st.write("✅ Fichier chargé avec succès !")

            # Afficher les colonnes originales
            st.subheader("📌 Colonnes originales du fichier :")
            original_columns = st.session_state.dfs[i].columns.tolist()
            st.write(original_columns)

            # Interface de mapping des colonnes par catégorie
            st.subheader("🔄 Mapping des colonnes")
            
            # Générer le prompt pour ChatGPT
            original_columns = st.session_state.dfs[i].columns.tolist()
            prompt = f"""Fais le mapping entre les colonnes de ces deux fichiers Excel de déchets. Attention n'essaie pas de tout mapper, seulement les colonnes qui ont un sens.

Colonnes cibles à mapper :
{', '.join(TARGET_COLUMNS)}

Synonymes importants à considérer :
- codeCed : peut aussi être nommé "nomenclature dechet", "code déchet", "code nomenclature"
- quantiteCollecteTransporteur : peut aussi être nommé "quantité de déchet en tonne", "quantité en t", "quantité en kg", "tonnage", "poids"
- descDechet : peut aussi être nommé "désignation", "nom du déchet", "description déchet", "type de déchet"
- codeTraitementPrevuInstallationDestination : peut aussi être nommé "code D/R", "code traitement", "code valorisation", "type de traitement"
- nomInstallationDestination : peut aussi être nommé "entreposage", "destination", "site de traitement", "installation de traitement", "centre de traitement"

Colonnes sources disponibles :
{', '.join(original_columns)}

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
                    st.rerun()
                    
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
                        else:
                            # Si aucune valeur n'est sélectionnée, supprimer le mapping
                            if i in st.session_state.column_mappings and source_col in st.session_state.column_mappings[i]:
                                del st.session_state.column_mappings[i][source_col]
                            # Mettre à jour le sélecteur dans la session state
                            st.session_state.selectors[f"{i}_{source_col}"] = ""

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
                    # Copier les données brutes sans formatage
                    df_mapped[target_col] = st.session_state.dfs[i][source_col]
                    
                    # Formatage spécial pour le code CED
                    if target_col == 'codeCed':
                        df_mapped[target_col] = df_mapped[target_col].apply(format_ced_code)
                    
                    # Remplacer les NaN selon le type de colonne
                    if target_col in ['quantiteCollecteTransporteur', 'volumeUnitaire']:
                        # Pour les quantités, remplacer NaN par "0"
                        df_mapped[target_col] = df_mapped[target_col].fillna("0")
                    elif target_col in ['coutsPreparationHT', 'coutsTransportHT', 'coutsTraitementHT', 'coutGlobal', 
                                     'rachatTotalHT', 'equivalentCoutsContenantsHT', 'coutsMiseDispo', 
                                     'coutsMaintenance', 'coutsContenantAutres', 'autresCoutsHT', 
                                     'coutsNonExpliques', 'coutsPenalites', 'coutsDeclassement', 
                                     'coutsTGAP', 'montantTotalHT']:
                        # Pour les coûts, remplacer NaN par "0"
                        df_mapped[target_col] = df_mapped[target_col].fillna("0")
                    else:
                        # Pour toutes les autres colonnes, remplacer NaN par une chaîne vide
                        df_mapped[target_col] = df_mapped[target_col].fillna("")
                
                # Stocker le DataFrame mappé
                st.session_state.mapped_dfs[i] = df_mapped
                st.success(f"✅ Mapping validé pour le fichier {i+1} !")
                
                # Afficher l'aperçu des données mappées
                st.subheader("📌 Aperçu des données après mapping :")
                # Filtrer le DataFrame pour ne garder que les colonnes mappées
                mapped_columns = set(st.session_state.column_mappings[i].values())
                df_mapped_preview = df_mapped[list(mapped_columns)]
                st.write(df_mapped_preview.head())

                # Afficher le tableau de mapping explicatif
                st.subheader("🔄 Tableau de mapping")
                mapping_explanation = []
                for source_col, target_col in st.session_state.column_mappings[i].items():
                    # Déterminer la catégorie de la colonne cible
                    category = "Autre"
                    for cat, cols in COLUMN_CATEGORIES.items():
                        if target_col in cols:
                            category = cat
                            break
                    
                    # Ajouter une ligne au tableau
                    mapping_explanation.append({
                        "Colonne source": source_col,
                        "Colonne cible": target_col,
                        "Catégorie": category,
                        "Obligatoire": "Oui" if target_col in REQUIRED_COLUMNS else "Non"
                    })
                
                # Créer et afficher le DataFrame de mapping avec des colonnes plus larges
                mapping_df = pd.DataFrame(mapping_explanation)
                st.dataframe(mapping_df, use_container_width=True, height=400)

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
                
                # Affichage du tableau récapitulatif des validations avec des colonnes plus larges
                if validation_summary:
                    st.write("📊 Tableau récapitulatif des validations :")
                    validation_df = pd.DataFrame(validation_summary)
                    st.dataframe(validation_df, use_container_width=True, height=400)
                
                # Affichage des erreurs détaillées avec des colonnes plus larges
                if format_errors:
                    st.error("❌ Détail des erreurs de format :")
                    for col, values in format_errors.items():
                        with st.expander(f"🔴 {col} - {len(values)} erreurs"):
                            st.write("Valeurs incorrectes :")
                            errors_df = pd.DataFrame({"Valeurs incorrectes": values})
                            st.dataframe(errors_df, use_container_width=True, height=200)
                            if col in df_mapped.columns:
                                st.write("Exemples de valeurs valides :")
                                valid_examples = df_mapped[~df_mapped[col].isna()][col].head()
                                valid_df = pd.DataFrame({"Valeurs valides": valid_examples.tolist()})
                                st.dataframe(valid_df, use_container_width=True, height=100)

    # Si au moins un fichier a été mappé, afficher le bouton de concaténation
    if len(st.session_state.mapped_dfs) > 0:
        st.markdown("### 🔄 Génération du fichier final")
        if st.button("✨ Générer le fichier final"):
            # Concaténer tous les DataFrames mappés (même s'il n'y en a qu'un)
            final_df = pd.concat(st.session_state.mapped_dfs.values(), ignore_index=True)
            
            # Afficher un aperçu du fichier final
            st.subheader("📌 Aperçu du fichier final :")
            st.write(final_df.head())
            
            # Afficher les points de jointure entre les fichiers
            if len(st.session_state.mapped_dfs) > 1:
                st.subheader("🔍 Points de jointure entre les fichiers :")
                current_row = 0
                for i, df in enumerate(st.session_state.mapped_dfs.values()):
                    if i > 0:  # Ne pas afficher pour le premier fichier
                        st.markdown(f"### Jointure entre le fichier {i} et {i+1}")
                        # Afficher les 3 dernières lignes du fichier précédent
                        st.write("3 dernières lignes du fichier précédent :")
                        st.write(final_df.iloc[current_row-3:current_row])
                        # Afficher les 3 premières lignes du fichier actuel
                        st.write("3 premières lignes du fichier actuel :")
                        st.write(final_df.iloc[current_row:current_row+3])
                        st.markdown("---")
                    current_row += len(df)
            
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
