import os
from pathlib import Path
from typing import List, Optional, Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    NODE_ID: int = 1
    NODE_ROLE: str = "follower"
    COMMITTEE_SIZE: int = 4
    PEERS: Any = []
    GENESIS_FILE: Path = Path("/app/genesis.json")
    LEDGER_PATH: Path = Path("/app/ledger")
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 1317
    P2P_PORT: int = 26656

    @field_validator("PEERS", mode="before")
    @classmethod
    def parse_peers(cls, v):
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [p.strip() for p in v.split(",") if p.strip()]
        return v

settings = Settings()
