from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NasaMission(Base):
    __tablename__ = "nasa_missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    launch_year = Column(Integer, nullable=True)

class NasaVariable(Base):
    __tablename__ = "nasa_variables"

    id = Column(Integer, primary_key=True, index=True)
    variable_name = Column(String, unique=True, index=True, nullable=False)
    unit = Column(String, nullable=False)
    current_value = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

class ScientificAnalysis(Base):
    __tablename__ = "scientific_analyses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    engine_used = Column(String, nullable=False)  # Rhea, Jeans, ou NASA engine
    result_data = Column(Text, nullable=True)     # Contenu ou GeoJSON text

class SpatialFileRegistry(Base):
    __tablename__ = "spatial_file_registry"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)    # GeoJSON ou GeoTIFF
    geom = Column(Geometry("GEOMETRY", srid=4326), nullable=True) # Pour PostGIS
    is_active =Column(Boolean,default=True)