#!/usr/bin/env python3
"""Discord Bot — Community channel for Sovereign 7G swarm."""
import os, json, time, logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode

TOKEN=os.getenv("DISCORD_BOT_TOKEN","")

def send_discord(content: str = "", embed=None):
    if not TOKEN:
        return {"error": "DISCORD_BOT_TOKEN not set"}
    try:
        import urllib.request
        payload = {"content": content}
        if embed: payload["embeds"] = [embed]
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{os.getenv('DISCORD_CHANNEL_ID','')}/messages",
            data=data, headers={"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"},
            method="POST")
        return json.loads(urllib.request.urlopen(req, timeout=5).read())
    except Exception as e:
        return {"error": str(e)}

def alert_discovery(ip: str, ua: str):
    return send_discord(embed={"title":"🚀 First external agent!","color":3066993,
        "fields":[{"name":"IP","value":f"`{ip}`","inline":True},{"name":"UA","value":f"`{ua}`","inline":True}]})

def alert_payment(amount: float, addr: str, service: str):
    return send_discord(embed={"title":"💰 Payment received","color":15105570,
        "fields":[{"name":"Amount","value":f"`{amount} S7G`","inline":True},{"name":"From","value":f"`{addr}`","inline":True}]})

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Set DISCORD_BOT_TOKEN")
        print("   export DISCORD_BOT_TOKEN=...")
    else:
        r = send_discord("🤖 *Sovereign 7G Bot is live*\nMonitoring 30 agents on 3 venues.")
        if "error" in r:
            print(f"❌ {r['error']}")
        else:
            print("✅ Discord message sent")
