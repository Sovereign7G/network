import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    NODE_ID: int = 1
    NODE_ROLE: str = "follower"
    COMMITTEE_SIZE: int = 4
    PEERS: List[str] = []
    GENESIS_FILE: Path = Path("/app/genesis.json")
    LEDGER_PATH: Path = Path("/app/ledger")
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 1317

settings = Settings()
