from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Création du dossier data s'il n'existe pas
os.makedirs("data", exist_ok=True)

# URL de connexion à la base SQLite
DATABASE_URL = "sqlite:///data/assurance.db"

# Initialisation du moteur et des sessions
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Définition du Modèle ORM (Table SQL)
class ProfilAssurance(Base):
    __tablename__ = 'profils_assurance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sexe = Column(String)
    age = Column(Integer)
    region = Column(String)
    ville = Column(String)
    secteur_activite = Column(String)
    revenu_mensuel = Column(String)
    perception_assurance = Column(String)
    niveau_connaissance = Column(String)
    niveau_confiance = Column(Integer)
    barriere_principale = Column(String)
    assurances_possedees = Column(String)
    canal_prefere = Column(String)
    sinistre_non_rembourse = Column(String)
    pret_digital_score = Column(Integer)
    utilisation_mobile_money = Column(String)

def init_db():
    """Crée les tables dans la base de données si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)

def reinitialiser_db():
    """Supprime et recrée les tables (utile pour regénérer une graine vierge)."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)