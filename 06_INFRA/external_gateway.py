#!/usr/bin/env python3
"""external_gateway.py — zero-trust external model gateway"""
import json, os, sys, time, re, urllib.request
CONFIG = {
    "deepseek": {"endpoint":"https://api.deepseek.com/v1/chat/completions",
        "model":"deepseek-chat","region":"china",
        "enabled": bool(os.environ.get("DEEPSEEK_API_KEY",""))},
    "kimi": {"endpoint":"https://api.moonshot.cn/v1/chat/completions",
        "model":"moonshot-v1-8k","region":"china",
        "enabled": bool(os.environ.get("KIMI_API_KEY",""))},
}
SENSITIVE = [
    r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b',
    r'0x[a-fA-F0-9]{40}',
    r'00_KNOWLEDGE/\S+',
    r'oyipx-[\w-]+',
]

class Gateway:
    def infer(self, provider, prompt, skill="", max_tokens=1024):
        cfg = CONFIG.get(provider)
        if not cfg or not cfg["enabled"]:
            return {"status":"error","error":"Provider not available"}
        safe, redacts = self._sanitize(prompt)
        t0 = time.time()
        try:
            payload = json.dumps({"model":cfg["model"],
                "messages":[{"role":"user","content":safe}]}).encode()
            req = urllib.request.Request(cfg["endpoint"], data=payload,
                headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = json.loads(r.read())
                c = resp.get("choices",[{}])[0].get("message",{}).get("content","")
                status = "success"
        except Exception as e:
            c = None; status = "error"
        lat = round((time.time()-t0)*1000)
        return {"status":status,"provider":provider,"model":cfg["model"],
            "response":c[:2000] if c else None,
            "error":None if status=="success" else str(e)[:200],
            "latency_ms":lat,"redactions":redacts}

    def _sanitize(self, txt):
        c = 0
        for p in SENSITIVE:
            m = re.findall(p, txt)
            if m:
                c += len(m)
                txt = re.sub(p, "[REDACTED]", txt)
        return txt, c

    def health(self):
        return {n:{"enabled":c.get("enabled",False),"region":c.get("region"),
            "model":c.get("model")} for n,c in CONFIG.items()}

if __name__ == "__main__":
    g = Gateway()
    a = sys.argv[1] if len(sys.argv)>1 else "health"
    if a == "health":
        print(json.dumps(g.health(), indent=2))
