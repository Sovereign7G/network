#!/usr/bin/env python3
"""s7g init — Generate boilerplate 7G app (web, mobile, backend)."""
import os, argparse
from pathlib import Path

TEMPLATES = {
    "web": {
        "index.js": "const { S7GClient } = require('@s7g-network/sdk');\nconst client = new S7GClient({ identity: 'alice.eth' });\nclient.call({ to: 'bob.eth', type: 'voice' });\n",
        ".env": "S7G_IDENTITY=alice.eth\nS7G_API_URL=http://localhost:8080",
        "package.json": '{"name":"my-s7g-app","dependencies":{"@s7g-network/sdk":"^1.0.0"}}'
    },
    "mobile": {
        "App.js": "import { S7GClient } from '@s7g-network/sdk';\nconst client = new S7GClient();\n",
        "package.json": '{"name":"my-s7g-app","dependencies":{"@s7g-network/sdk":"^1.0.0"}}'
    },
    "backend": {
        "index.py": "from s7g import S7GClient\nclient = S7GClient()\nprint(client.health())\n",
        "requirements.txt": "s7g>=1.0.0"
    }
}

def init_app(app_type: str, name: str):
    base = Path(name)
    base.mkdir(exist_ok=True)
    for fname, content in TEMPLATES.get(app_type, TEMPLATES["web"]).items():
        fp = base / fname
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
    print(f"✅ 7G {app_type} app created: {name}/")
    print(f"   cd {name} && npm install")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("name"); p.add_argument("--type", choices=["web","mobile","backend"], default="web")
    args = p.parse_args()
    init_app(args.type, args.name)
