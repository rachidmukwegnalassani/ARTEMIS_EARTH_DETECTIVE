# -*- coding: utf-8 -*-
# backend/schemas/chat_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional
from backend.schemas.statistics_schema import TableDataSchema


class UIContextSchema(BaseModel):
    table_data: Optional[TableDataSchema] = None
    active_layer: Optional[str] = Field(None, example="nasa_temperature_anomaly")
    chart_metric: Optional[str] = Field(None, example="Air Temperature")


class ChatAnalysisRequestSchema(BaseModel):
    ui_state: UIContextSchema
    user_message: Optional[str] = Field(
        "Analyse de manière croisée ce tableau statistique par rapport au projet Artemis Earth Detective.",
        example="Que remarques-tu sur ces indicateurs ?"
    )


class ChatMessageSchema(BaseModel):
    role: str = Field(..., description="Le rôle du messager : 'user' ou 'assistant'")
    content: str = Field(..., description="Le contenu textuel du message")


class ChatSessionSchema(BaseModel):
    session_id: str = Field(..., example="artemis-session-4567")
    history: List[ChatMessageSchema] = []
