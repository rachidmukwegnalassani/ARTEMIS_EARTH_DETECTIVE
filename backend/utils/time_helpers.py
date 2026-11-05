# -*- coding: utf-8 -*-
# backend/utils/time_helpers.py

from typing import List, Dict, Any


def filter_time_series_by_range(data_points: List[Dict[str, Any]], start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    Filtre une série temporelle de variables NASA entre deux dates 
    reçues au format standard ISO (AAAA-MM-JJ) pour l'affichage du graphique.
    """
    filtered_data = []
    for point in data_points:
        timestamp = point.get("timestamp", point.get("date", ""))
        if timestamp and start_date <= timestamp <= end_date:
            filtered_data.append(point)
    return filtered_data


def format_timestamp_for_ui(iso_string: str) -> str:
    """
    Convertit une chaîne de date ISO (ex: 2026-11-02T12:00:00Z) en format lisible
    pour les axes de vos graphiques de tendances (ex: 02/11/2026 12:00).
    """
    if not iso_string or len(iso_string) < 10:
        return iso_string
    try:
        date_part = iso_string[:10]
        time_part = iso_string[11:16] if len(iso_string) >= 16 else ""
        
        year, month, day = date_part.split("-")
        formatted_date = f"{day}/{month}/{year}"
        
        return f"{formatted_date} {time_part}".strip()
    except Exception:
        return iso_string


def aggregate_data_by_period(data_points: List[Dict[str, Any]], period: str = "daily") -> Dict[str, float]:
    """
    Agrège les valeurs scientifiques (moyenne brute) par jour ou par mois 
    pour simplifier la génération des tableaux de statistiques globales.
    """
    aggregated = {}
    counts = {}
    
    for point in data_points:
        timestamp = point.get("timestamp", point.get("date", ""))
        val = point.get("value")
        
        if not timestamp or val is None:
            continue
            
        key = timestamp[:10] if period == "daily" else timestamp[:7]
        
        aggregated[key] = aggregated.get(key, 0.0) + float(val)
        counts[key] = counts.get(key, 0) + 1
        
    return {k: round(aggregated[k] / counts[k], 2) for k in aggregated}
