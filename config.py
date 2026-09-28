"""Small .env loader used by the local diagnostic scripts."""

import os
from pathlib import Path


def load_env() -> None:
    env_file = Path(__file__).with_name(".env")
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def required(name: str) -> str:
    value = os.getenv(name)
    if not value or value.startswith(("SUBSTITUA_", "SECRET_", "AINDA_")):
        raise RuntimeError(f"Defina {name} no arquivo .env")
    return value
