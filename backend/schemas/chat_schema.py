# backend/schemas/chat_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.schemas.statistics_schema import TableDataSchema

class UIContextSchema(BaseModel):
    """
    Rassemble les variables actives de vos 3 composants d'interface 
    (Carte, Graphique, Statistiques) pour les envoyer proprement à l'IA.
    """
    table_data: Optional[TableDataSchema] = None
    active_layer: Optional[str] = Field(None, example="nasa_temperature_anomaly")
    chart_metric: Optional[str] = Field(None, example="Air Temperature")

class ChatAnalysisRequestSchema(BaseModel):
    """
    Modèle de requête envoyé par le bouton frontend 'Analyser ce tableau' 
    contenant le contexte de l'interface et le message utilisateur.
    """
    ui_state: UIContextSchema
    user_message: Optional[str] = Field(
        "Analyse de manière croisée ce tableau statistique par rapport au projet Artemis Ray Detective.",
        example="Que remarques-tu sur ces indicateurs ?"
    )

class ChatMessageSchema(BaseModel):
    """Structure d'un message individuel pour l'historique du chat scientifique."""
    role: str = Field(..., description="Le rôle du messager : 'user' ou 'assistant'")
    content: str = Field(..., description="Le contenu textuel du message")

class ChatSessionSchema(BaseModel):
    """Structure complète d'une session de chat avec son identifiant et son historique."""
    session_id: str = Field(..., example="artemis-session-4567")
    history: List[ChatMessageSchema] = []