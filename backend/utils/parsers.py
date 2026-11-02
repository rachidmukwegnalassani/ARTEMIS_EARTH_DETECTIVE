# backend/utils/parsers.py
import json
import io
from typing import Dict, Any

# Importations des librairies d'extraction de documents (sécurisées avec blocs try)
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None

try:
    import pandas as pd
except ImportError:
    pd = None


def format_ui_table_for_llm(table_data: Dict[str, Any]) -> str:
    """
    Transforme les lignes et colonnes du bloc Statistiques Globales
    en un format textuel structuré (Markdown) pour le Chat Artemis.
    """
    if not table_data or 'headers' not in table_data or 'rows' not in table_data:
        return "Aucune donnée statistique tabulaire disponible pour le moment."
    
    headers = table_data.get('headers', [])
    rows = table_data.get('rows', [])
    
    output = "\n=== [DONNÉES DU TABLEAU DE STATISTIQUES GLOBALES] ===\n"
    if pd is not None:
        try:
            df = pd.DataFrame(data=rows, columns=headers)
            return output + df.to_markdown(index=False) + "\n"
        except Exception:
            pass
            
    # Fallback manuel si pandas n'est pas disponible ou échoue
    output += " | ".join(headers) + "\n"
    output += "-" * (len(" | ".join(headers))) + "\n"
    for row in rows:
        output += " | ".join(map(str, row)) + "\n"
    return output


def parse_nasa_text_document(file_content: bytes, filename: str) -> str:
    """
    Détecte automatiquement l'extension du fichier (TXT, JSON, PDF, WORD, EXCEL)
    et en extrait le texte ou les données pour le Chat Artemis.
    Syntaxe compatible Python 3.12/3.13 sans Union.
    """
    ext = filename.split('.')[-1].lower()
    output_header = f"\n=== [CONTENU DU DOCUMENT IMPORTÉ : {filename}] ===\n"

    try:
        # 1. Gestion des fichiers PDF
        if ext == 'pdf':
            if pypdf is None:
                return f"{output_header}[Erreur backend: La librairie 'pypdf' n'est pas installée]."
            
            pdf_file = io.BytesIO(file_content)
            reader = pypdf.PdfReader(pdf_file)
            extracted_text = ""
            for page in reader.pages[:5]:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            return f"{output_header}{extracted_text[:5000]}"

        # 2. Gestion des fichiers Word (.docx)
        elif ext == 'docx':
            if docx is None:
                return f"{output_header}[Erreur backend: La librairie 'python-docx' n'est pas installée]."
            
            docx_file = io.BytesIO(file_content)
            doc = docx.Document(docx_file)
            extracted_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return f"{output_header}{extracted_text[:5000]}"

        # 3. Gestion des fichiers Excel (.xlsx, .xls)
        elif ext in ['xlsx', 'xls']:
            if pd is None:
                return f"{output_header}[Erreur backend: La librairie 'pandas' n'est pas installée]."
            
            excel_file = io.BytesIO(file_content)
            df = pd.read_excel(excel_file)
            return f"{output_header}{df.to_markdown(index=False)[:5000]}"

        # 4. Gestion des fichiers JSON
        elif ext == 'json':
            text = file_content.decode('utf-8', errors='ignore')
            data = json.loads(text)
            return f"{output_header}{json.dumps(data, indent=2)[:5000]}"

        # 5. Gestion des fichiers Texte brut (.txt, .md, .csv)
        else:
            text = file_content.decode('utf-8', errors='ignore')
            return f"{output_header}{text[:5000]}"

    except Exception as e:
        return f"Erreur lors de l'extraction automatique du document {filename} : {str(e)}"