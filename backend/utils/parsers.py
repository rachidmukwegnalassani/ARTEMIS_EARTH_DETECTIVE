# -*- coding: utf-8 -*-

import json
import io
from typing import Dict, Any

# Importations sécurisées des librairies d'extraction de documents
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
    Transforme les indicateurs calculés par le StatisticsAnalyzer Pandas
    en un format textuel structuré (Markdown) pour le Chat Artemis.
    """
    if not table_data:
        return "Aucune donnée statistique disponible pour le moment."
    
    output = "\n=== [DONNÉES DU COMPTE-RENDU STATISTIQUE D'ENQUÊTE] ===\n"
    
    # Si les statistiques viennent de notre nouvel analyseur Pandas (dictionnaire de clés)
    if "mean" in table_data:
        headers = ["Indicateur Statistique", "Valeur Calculée"]
        rows = [
            ["Nombre d'échantillons", str(table_data.get("count", 0))],
            ["Moyenne Générale", f"{table_data.get('mean', 0.0):.4f}"],
            ["Médiane", f"{table_data.get('median', 0.0):.4f}"],
            ["Minimum Détecté", f"{table_data.get('minimum', 0.0):.4f}"],
            ["Maximum Détecté", f"{table_data.get('maximum', 0.0):.4f}"],
            ["Écart-Type (Dispersion)", f"{table_data.get('std', 0.0):.4f}"]
        ]
        
        if pd is not None:
            try:
                df = pd.DataFrame(data=rows, columns=headers)
                return output + df.to_markdown(index=False) + "\n"
            except Exception:
                pass
        
        # Fallback manuel si tabulate/pandas échoue pour l'affichage Markdown
        output += " | ".join(headers) + "\n"
        output += "-" * 40 + "\n"
        for row in rows:
            output += " | ".join(row) + "\n"
        return output

    # Fallback pour l'ancienne structure au cas où (compatibilité descendante)
    headers = table_data.get('headers', [])
    rows = table_data.get('rows', [])
    if pd is not None and headers and rows:
        try:
            df = pd.DataFrame(data=rows, columns=headers)
            return output + df.to_markdown(index=False) + "\n"
        except Exception:
            pass
            
    return "Format statistique non pris en charge pour l'interprétation IA."


def parse_nasa_text_document(file_content: bytes, filename: str) -> str:
    """
    Détecte automatiquement l'extension du fichier scientifique (TXT, JSON, PDF, WORD, EXCEL)
    et en extrait le contenu textuel nettoyé pour le Chat Artemis.
    """
    ext = filename.split('.')[-1].lower()
    output_header = f"\n=== [CONTENU DU DOCUMENT IMPORTÉ : {filename}] ===\n"

    try:
        # 1. Gestion des fichiers PDF scientifiques de la NASA
        if ext == 'pdf':
            if pypdf is None:
                return f"{output_header}[Erreur backend : La librairie 'pypdf' n'est pas installée]."
            
            pdf_file = io.BytesIO(file_content)
            reader = pypdf.PdfReader(pdf_file)
            extracted_text = ""
            for page in reader.pages[:5]:  # Limitation aux 5 premières pages pour préserver le contexte du LLM
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            return f"{output_header}{extracted_text[:5000]}"

        # 2. Gestion des rapports Word (.docx)
        elif ext == 'docx':
            if docx is None:
                return f"{output_header}[Erreur backend : La librairie 'python-docx' n'est pas installée]."
            
            docx_file = io.BytesIO(file_content)
            doc = docx.Document(docx_file)
            extracted_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return f"{output_header}{extracted_text[:5000]}"

        # 3. Gestion des fichiers de mesures Excel (.xlsx, .xls)
        elif ext in ['xlsx', 'xls']:
            if pd is None:
                return f"{output_header}[Erreur backend : La librairie 'pandas' n'est pas installée]."
            
            excel_file = io.BytesIO(file_content)
            df = pd.read_excel(excel_file)
            return f"{output_header}{df.to_markdown(index=False)[:5000]}"

        # 4. Gestion des configurations JSON
        elif ext == 'json':
            text = file_content.decode('utf-8', errors='ignore')
            data = json.loads(text)
            return f"{output_header}{json.dumps(data, indent=2)[:5000]}"

        # 5. Gestion du texte brut (.txt, .md, .csv)
        else:
            text = file_content.decode('utf-8', errors='ignore')
            return f"{output_header}{text[:5000]}"

    except Exception as e:
        return f"Erreur lors de l'extraction automatique du document {filename} : {str(e)}"
