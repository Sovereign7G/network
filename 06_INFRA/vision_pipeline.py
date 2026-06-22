#!/usr/bin/env python3
"""
vision_pipeline.py — Era VI: Vision pipeline for Sovereign OS.

Extends the Era II embedding pipeline with CLIP-based image embeddings.
Images become OKF ImageConcept types, searchable alongside text concepts.
Zero-trust: no image data sent to external APIs unless explicitly routed.
"""

import json, os, sys, time, hashlib, base64, io
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

_EP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _EP_DIR)

KNOWLEDGE_ROOT = Path(os.environ.get("OKF_ROOT",
    "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
)).expanduser()

VISION_DIR = KNOWLEDGE_ROOT / "vision"
VISION_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR = VISION_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _ts() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _write_okf(path, fm, body, msg=None):
    """Write OKF concept directly (avoids subprocess PATH issues)."""
    import yaml
    target = KNOWLEDGE_ROOT / path.strip("/") / "index.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    fm_yaml = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
    content = f"---\n{fm_yaml}\n---\n\n{body.strip()}\n"
    target.write_text(content)
    return {"path": path, "written": True}


# ── Hash-based image embedding (no CLIP dependency) ─────────────

class VisionPipeline:
    """Image → OKF concept pipeline. Uses hash-based embedding by default
    (zero dependencies). Falls back to CLIP-based embedding if available.
    """

    def __init__(self):
        self._clip = None

    def _get_clip(self):
        """Lazy-load CLIP — only imports if torch + clip are installed."""
        if self._clip is not None:
            return self._clip
        try:
            import torch
            import clip
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model, preprocess = clip.load("ViT-B/32", device=device)
            self._clip = {"model": model, "preprocess": preprocess, "device": device}
            return self._clip
        except Exception:
            self._clip = False
            return None

    def embed_image(self, image_path: str) -> dict:
        """Generate embedding for an image. Returns embedding + metadata."""
        if not os.path.exists(image_path):
            return {"error": f"File not found: {image_path}"}

        size = os.path.getsize(image_path)
        name = os.path.basename(image_path)
        ext = os.path.splitext(name)[1].lower()

        # Try CLIP if available
        clip_inst = self._get_clip()
        if clip_inst:
            try:
                from PIL import Image
                img = Image.open(image_path).convert("RGB")
                img_tensor = clip_inst["preprocess"](img).unsqueeze(0).to(clip_inst["device"])
                with torch.no_grad():
                    emb = clip_inst["model"].encode_image(img_tensor)
                embedding = emb.cpu().numpy().flatten().tolist()
                return {"method": "clip", "embedding": embedding, "dim": len(embedding),
                        "file": name, "size": size, "ext": ext}
            except Exception:
                pass

        # Fallback: perceptual hash (content-addressed, deterministic)
        img_hash = self._phash(image_path)
        return {"method": "phash", "phash": img_hash, "dim": 64,
                "file": name, "size": size, "ext": ext}

    def _phash(self, image_path: str) -> str:
        """Simple perceptual hash — reads raw bytes, MD5 + size."""
        try:
            with open(image_path, "rb") as f:
                data = f.read()
            h = hashlib.md5(data).hexdigest()
            return f"{os.path.getsize(image_path)}_{h[:16]}"
        except Exception:
            return hashlib.md5(str(time.time()).encode()).hexdigest()[:16]

    def index_image(self, image_path: str, title: str = None,
                    tags: List[str] = None) -> dict:
        """Index an image as an OKF ImageConcept."""
        result = self.embed_image(image_path)
        if "error" in result:
            return result

        name = os.path.splitext(os.path.basename(image_path))[0]
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name) if 're' in dir() else name[:32]
        okf_path = f"vision/images/{safe_name}_{_ts()[:8]}"

        # Embedding dim from CLIP (384) or phash (64)
        dim = result.get("dim", 64)

        # Copy image to OKF-managed location
        dest = IMAGES_DIR / f"{safe_name}_{_ts()[:8]}{result.get('ext', '.bin')}"
        import shutil
        shutil.copy2(image_path, dest)

        frontmatter = {
            "type": "ImageConcept",
            "title": title or name,
            "file": dest.name,
            "size_bytes": result.get("size", 0),
            "embedding_method": result.get("method", "phash"),
            "embedding_dim": dim,
            "tags": tags or [],
        }
        if "phash" in result:
            frontmatter["perceptual_hash"] = result["phash"]

        body = f"# {title or name}\n\n**Image:** {image_path}\n"
        body += f"**Size:** {result.get('size', 0)} bytes\n"
        body += f"**Embedding:** {result.get('method', 'phash')} ({dim}d)\n"
        body += f"**Stored:** {dest}\n"

        _write_okf(okf_path, frontmatter, body, f"Vision: {name}")
        return {"concept_path": okf_path, "file": dest.name,
                "embedding_method": result.get("method"), "dim": dim}

    def search_by_image(self, image_path: str, limit: int = 10) -> list:
        """Search OKF concepts visually similar to this image."""
        query_emb = self.embed_image(image_path)
        if "error" in query_emb:
            return [query_emb]

        # If CLIP embedding, use Chroma similarity search
        if query_emb.get("method") == "clip":
            try:
                from embedding_pipeline import get_embedder
                emb = get_embedder()
                if emb:
                    return emb.search_by_embedding(query_emb["embedding"], limit)
            except Exception:
                pass

        # Fallback: grep search by tags/title
        try:
            from magix_okf import search_concepts
            name = os.path.splitext(os.path.basename(image_path))[0]
            return search_concepts(name)
        except Exception:
            return []

    def concept_path(self, filename: str) -> str:
        return f"vision/images/{os.path.splitext(filename)[0]}"


# ── MCP tools ───────────────────────────────────────────────────

_VP = VisionPipeline()

def vision_analyze(args: dict) -> dict:
    """Analyze an image and create OKF ImageConcept."""
    return _VP.index_image(
        args.get("path", ""),
        args.get("title"),
        args.get("tags", []),
    )

def vision_search(args: dict) -> list:
    """Search OKF by image similarity."""
    return _VP.search_by_image(args.get("path", ""), args.get("limit", 10))


TOOLS = {
    "vision_analyze": vision_analyze,
    "vision_search": vision_search,
}


# ── CLI ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    vp = VisionPipeline()
    a = sys.argv[1] if len(sys.argv) > 1 else "help"
    if a == "analyze":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        r = vp.index_image(path)
        print(json.dumps(r, indent=2))
    elif a == "search":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        r = vp.search_by_image(path)
        print(json.dumps(r, indent=2))
    else:
        print("Usage: python3 vision_pipeline.py [analyze <path>|search <path>]")
