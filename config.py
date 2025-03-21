# Configuración de la aplicación
class Config:
    SECRET_KEY = '24061998'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    CORS_HEADERS = 'Content-Type'