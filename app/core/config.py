class Config:
    # Указание адреса для обращения
    LLM_ENDPOINT = "http://192.168.23.17:1234/v1"
    # Указание API ключа для модели
    LLM_API_KEY = "not-needed"
    # Указание модели
    MODEL_NAME = "qwen/qwen3-vl-4b"
    # Указание типа базы данных
    DB_TYPE = "sqlite"
    # Указание базы данных
    DB_NAME = "database.db"
    # Указание срока жизни токена в часах
    JWT_EXPIRATION_TIME = 2
    # Ключ для шифрования
    SECRET_KEY = "ElkinCode2026"