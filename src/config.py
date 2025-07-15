import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    config = {
        "app_name": os.getenv("APP_NAME", "airtasker"),
        "server_host": os.getenv("SERVER_HOST", ""),
        "server_port": int(os.getenv("SERVER_PORT", "8000")),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "log_format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
        "cors_origin": os.getenv("CORS_ORIGIN", "*"),
        "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true"
    }
    return config

# Global config instance
config = load_config() 