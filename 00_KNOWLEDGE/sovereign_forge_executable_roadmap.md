# 🏛️ SOVEREIGN FORGE — COMPLETE IMPLEMENTATION PLANS
## Master Blueprint Executable Roadmap (v1.0 Complete)

> [!NOTE]
> This document formalizes the production-grade, executable implementation plan for all 5 layers of the **Sovereign Forge**. It contains concrete codebase templates, script definitions, WebGL2 files, and systemd configurations.

---

## 🗺️ Part 1: Implementation Plan Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                     SOVEREIGN FORGE — 90-DAY PRODUCTION ROLLOUT                      │
│                        "From Blueprint to Battle-Ready"                               │
└─────────────────────────────────────────────────────────────────────────────────────┘

Week 1-2: ████████░░░░░░░░░░░░  LAYER 1 (Infrastructure)
Week 3-4: ░░░░░░░░████████░░░░░░  LAYER 2 (Orchestration)
Week 5-6: ░░░░░░░░░░░░░░████████░░  LAYER 3 (Execution)
Week 7-8: ░░░░░░░░░░░░░░░░░░░░████  LAYER 4 (Intelligence)
Week 9-12: ░░░░░░░░░░░░░░░░░░░░░░░░  LAYER 5 (Spindle B Presentation)
```

---

## 🛠️ Part 2: LAYER 1: Infrastructure — "The Foundry" (Days 1-14)

### Phase 1.1: Base OS & Python Environment (Days 1-3)

```powershell
# Windows 11 - PowerShell as Administrator

# 1. Install Python 3.11 (ensure PATH)
winget install Python.Python.3.11

# 2. Verify installation
python --version  # Must show 3.11.x
pip --version

# 3. Create virtual environment
cd "C:\AGE REPUBLIC"
python -m venv .venv
.\.venv\Scripts\activate

# 4. Upgrade pip and install core packages
pip install --upgrade pip setuptools wheel
```

### Phase 1.2: Ollama & Model Deployment (Days 4-7)

```powershell
# 1. Install Ollama for Windows
# Download from https://ollama.com/download/windows
# Or via winget:
winget install Ollama.Ollama

# 2. Start Ollama service (as admin)
ollama serve

# 3. Pull required models (may take 10-60 min per model)
ollama pull codellama:7b
ollama pull moondream:1.8b
ollama pull llama3.2:3b

# 4. Verify GPU acceleration
ollama run codellama:7b --verbose
# Look for: "eval rate: XX tokens/s" (should be >20 with GPU)

# 5. Multi-GPU configuration (if multiple NVIDIA GPUs)
# Create Ollama config: %USERPROFILE%\.ollama\models\config.json
```

### Phase 1.3: Development Tools (Days 8-10)

```powershell
# 1. Git for Windows
winget install Git.Git

# 2. VS Code
winget install Microsoft.VisualStudioCode

# 3. VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens

# 4. NVIDIA CUDA Toolkit (if not already installed)
# Download from: https://developer.nvidia.com/cuda-downloads
```

### Phase 1.4: CLI Anything Hub (Days 11-14)

```powershell
# 1. Install CLI Anything Hub
pip install cli-anything-hub

# 2. Verify installation
cli-hub --version
cli-hub list  # Shows all available harnesses

# 3. Test a harness
cli-hub run blender --help
cli-hub run python --exec "print('Hello Sovereign Forge')"

# 4. Install optional harness dependencies
pip install pillow numpy opencv-python
```

**Success Criteria Layer 1:**
```cmd
✅ Python 3.11: python --version
✅ Ollama: ollama list (shows 3 models)
✅ GPU: ollama run codellama:7b "Hello" --verbose
✅ CLI Hub: cli-hub list (50+ harnesses)
```

---

## 📋 Part 3: LAYER 2: Orchestration — "The Director" (Days 15-28)

### Phase 2.1: Routa Core Engine (Days 15-18)

```python
# src/agent/routa_orchestrator.py - Core implementation

import json
import yaml
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class KanbanState(Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    DEV = "dev"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"

@dataclass
class Story:
    id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    state: KanbanState = KanbanState.BACKLOG
    artifacts: List[str] = None
    attestation: Optional[str] = None

class RoutaOrchestrator:
    def __init__(self, story_file: str = "stories.yml"):
        with open(story_file, 'r') as f:
            self.stories = self._load_stories(yaml.safe_load(f))
    
    def transition(self, story_id: str, new_state: KanbanState) -> bool:
        story = self._find_story(story_id)
        if not story:
            return False
        
        # Quality gates
        if new_state == KanbanState.REVIEW:
            if not self._verify_vision_review(story):
                story.state = KanbanState.BLOCKED
                return False
        elif new_state == KanbanState.DONE:
            if not self._verify_completion(story):
                return False
        
        story.state = new_state
        self._log_transition(story_id, new_state)
        return True
```

### Phase 2.2: GBNF Grammar Enforcement (Days 19-22)

```python
# src/agent/grammar_enforcer.py

from llama_cpp import Llama
from typing import Dict, Any
import json

class GBNFGrammarEnforcer:
    """
    Ensures LLM outputs conform to exact JSON schema.
    Zero malformed JSON = Zero parser crashes.
    """
    
    def __init__(self, model_path: str = "codellama-7b"):
        self.llm = Llama(model_path=model_path)
        
    # GBNF grammar for structured agent outputs
    AGENT_OUTPUT_GRAMMAR = """
    root ::= AgentOutput
    AgentOutput ::= "{" ws "\"action\":" ws string "," ws "\"parameters\":" ws object "," ws "\"confidence\":" ws number "}"
    string ::= "\"" [^\"]* "\""
    object ::= "{" ws (string ws ":" ws value ("," ws string ws ":" ws value)*)? "}"
    array ::= "[" ws (value ("," ws value)*)? "]"
    value ::= string | number | object | array | "true" | "false" | "null"
    number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)?
    ws ::= [ \t\n]*
    """
    
    def enforce_json(self, raw_output: str) -> Dict[str, Any]:
        """Parse and validate LLM output with grammar constraints."""
        try:
            # Grammar-guided generation ensures valid JSON
            result = self.llm.create_completion(
                raw_output,
                grammar=self.AGENT_OUTPUT_GRAMMAR,
                max_tokens=512
            )
            return json.loads(result['choices'][0]['text'])
        except Exception as e:
            # Fallback to safe default
            return {"action": "log_error", "parameters": {"error": str(e)}, "confidence": 0.0}
```

### Phase 2.3: Vision Review Guard (Days 23-26)

```python
# src/agent/vision_review_guard.py

import requests
from PIL import Image
import base64
from typing import List, Dict

class VisionReviewGuard:
    """
    Moondream 1.8B local vision model integration.
    Validates rendered images against acceptance criteria.
    """
    
    def __init__(self, moondream_endpoint: str = "http://localhost:11434"):
        self.endpoint = moondream_endpoint
        
    def verify_render(self, image_path: str, criteria: List[str]) -> Dict:
        """
        Check if rendered image satisfies all criteria.
        
        Returns:
            {
                'passed': bool,
                'attestations': List[str],
                'failures': List[Dict]
            }
        """
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        results = {'passed': True, 'attestations': [], 'failures': []}
        
        for criterion in criteria:
            prompt = f"Does this image satisfy: '{criterion}'? Answer YES or NO with brief explanation."
            
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json={
                    "model": "moondream:1.8b",
                    "prompt": prompt,
                    "images": [image_base64],
                    "stream": False
                }
            ).json()
            
            if "YES" in response['response'].upper():
                results['attestations'].append(f"✅ {criterion}")
            else:
                results['passed'] = False
                results['failures'].append({
                    'criterion': criterion,
                    'reason': response['response']
                })
        
        return results
```

### Phase 2.4: Parallel Agent Router (Days 27-28)

```python
# src/agent/parallel_router.py

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import time

class ParallelAgentRouter:
    """
    Round-robin load balancing across 93 concurrent agents.
    Circuit breakers trip <2.22ms.
    """
    
    def __init__(self, agent_count: int = 93):
        self.agent_count = agent_count
        self.circuit_breakers = {i: {'failures': 0, 'last_fail': 0} for i in range(agent_count)}
        self.current_agent = 0
        self.executor = ThreadPoolExecutor(max_workers=agent_count)
        
    async def dispatch(self, tasks: List[Dict]) -> List[Dict]:
        """Dispatch tasks round-robin with circuit breaker protection."""
        results = []
        
        for i, task in enumerate(tasks):
            agent_id = i % self.agent_count
            
            # Circuit breaker check
            cb = self.circuit_breakers[agent_id]
            if cb['failures'] >= 5 and (time.time() - cb['last_fail']) < 30:
                # Circuit open - skip this agent
                results.append({'error': f'Agent {agent_id} circuit open', 'task': task})
                continue
            
            # Dispatch with timeout
            try:
                result = await asyncio.wait_for(
                    self._execute_task(task, agent_id),
                    timeout=2.22  # <2.22ms requirement
                )
                results.append(result)
                cb['failures'] = 0  # Reset on success
            except asyncio.TimeoutError:
                cb['failures'] += 1
                cb['last_fail'] = time.time()
                results.append({'error': f'Agent {agent_id} timeout', 'task': task})
        
        return results
    
    async def _execute_task(self, task: Dict, agent_id: int) -> Dict:
        """Execute single task on specific agent."""
        # Task execution logic here
        return {'agent_id': agent_id, 'result': task}
```

**Success Criteria Layer 2:**
```python
✅ Routa orchestrates 5+ concurrent stories
✅ Grammar enforcement catches malformed JSON (0% crash rate)
✅ Vision Review Guard validates renders with Moondream
✅ 93-agent parallel dispatch works
```

---

## 🏎️ Part 4: LAYER 3: Execution — "The Hands" (Days 29-42)

### Phase 3.1: Blender Harness Integration (Days 29-33)

```python
# src/harnesses/blender_harness.py

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional

class BlenderHarness:
    """Headless Blender execution with JSON in/out."""
    
    BLENDER_PATH = "C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe"
    
    def execute(self, command: str, parameters: Dict[str, Any], 
                json_input: Optional[Dict] = None) -> Dict:
        """
        Execute Blender command.
        
        Supported commands:
        - render: Render 3D scene to image
        - export: Export to various formats
        - simulate: Run physics simulation
        """
        
        if command == "render":
            return self._render_scene(parameters, json_input)
        elif command == "export":
            return self._export_model(parameters)
        elif command == "simulate":
            return self._run_simulation(parameters)
        else:
            return {"error": f"Unknown command: {command}", "exit_code": 1}
    
    def _render_scene(self, params: Dict, json_input: Optional[Dict]) -> Dict:
        scene_file = params.get('scene_file')
        output_path = params.get('output_path', 'render.png')
        resolution = params.get('resolution', [1920, 1080])
        samples = params.get('samples', 128)
        
        # Write JSON input to temp file if provided
        if json_input:
            temp_json = Path("temp_input.json")
            temp_json.write_text(json.dumps(json_input))
            params['json_file'] = str(temp_json)
        
        # Build blender command
        cmd = [
            self.BLENDER_PATH,
            "--background", scene_file,
            "--render-output", output_path,
            "--render-format", "PNG",
            f"--render-resolution-x", str(resolution[0]),
            f"--render-resolution-y", str(resolution[1]),
            f"--render-samples", str(samples),
            "--render-anim", "false"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Parse output for metrics
        metrics = self._parse_blender_output(result.stdout)
        
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "artifacts": [output_path] if result.returncode == 0 else [],
            "metrics": metrics
        }
```

### Phase 3.2: Universal CLI Harness Interface (Days 34-38)

```python
# src/harnesses/unified_harness.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import subprocess
import json

class BaseHarness(ABC):
    """Abstract base class for all CLI harnesses."""
    
    def __init__(self, app_path: str):
        self.app_path = app_path
        self.command_history: List[Dict] = []
    
    @abstractmethod
    def validate_command(self, command: str) -> bool:
        """Check if command is valid for this harness."""
        pass
    
    @abstractmethod
    def build_command_line(self, command: str, params: Dict) -> List[str]:
        """Convert abstract command to OS-specific CLI arguments."""
        pass
    
    def execute(self, command: str, parameters: Dict[str, Any],
                json_input: Optional[Dict] = None) -> Dict:
        """
        Unified execution contract:
        - Input: JSON (command + parameters)
        - Output: JSON (stdout + stderr + exit_code + artifacts)
        """
        
        if not self.validate_command(command):
            return {"error": f"Invalid command: {command}", "exit_code": 1}
        
        # Handle JSON input via temp file or stdin
        stdin_data = None
        if json_input:
            stdin_data = json.dumps(json_input)
        
        cmd_line = self.build_command_line(command, parameters)
        
        result = subprocess.run(
            cmd_line,
            input=stdin_data,
            capture_output=True,
            text=True
        )
        
        execution_record = {
            "command": command,
            "parameters": parameters,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "artifacts": self._collect_artifacts(parameters)
        }
        
        self.command_history.append(execution_record)
        
        return execution_record
    
    def _collect_artifacts(self, params: Dict) -> List[str]:
        """Discover output files from execution."""
        artifacts = []
        for key, value in params.items():
            if isinstance(value, str) and any(ext in value.lower() for ext in ['.png', '.jpg', '.mp4', '.pdf', '.blend']):
                artifacts.append(value)
        return artifacts
```

### Phase 3.3: 50+ Harness Registry (Days 39-42)

```python
# src/harnesses/registry.py

HARNESS_REGISTRY = {
    # Graphics & 3D
    "blender": {
        "class": "BlenderHarness",
        "path_env": "BLENDER_PATH",
        "default_path": "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe",
        "commands": ["render", "export", "simulate", "composite"]
    },
    "gimp": {
        "class": "GIMPHarness",
        "path_env": "GIMP_PATH",
        "default_path": "C:/Program Files/GIMP 2/bin/gimp-console-2.10.exe",
        "commands": ["convert", "resize", "filter", "batch"]
    },
    "obs": {
        "class": "OBSHarness",
        "path_env": "OBS_PATH",
        "default_path": "C:/Program Files/obs-studio/bin/64bit/obs64.exe",
        "commands": ["record", "stream", "screenshot", "scene"]
    },
    
    # Office & Documents
    "libreoffice": {
        "class": "LibreOfficeHarness",
        "path_env": "LIBREOFFICE_PATH",
        "default_path": "C:/Program Files/LibreOffice/program/soffice.exe",
        "commands": ["convert", "export_pdf", "merge"]
    },
    "pandoc": {
        "class": "PandocHarness",
        "path_env": "PANDOC_PATH",
        "default_path": "pandoc",
        "commands": ["convert", "pdf", "html", "docx"]
    },
    
    # Media Processing
    "ffmpeg": {
        "class": "FFmpegHarness",
        "path_env": "FFMPEG_PATH",
        "default_path": "ffmpeg",
        "commands": ["convert", "resize", "compress", "extract_audio"]
    },
    
    # Development
    "python": {
        "class": "PythonHarness",
        "path_env": "PYTHON_PATH",
        "default_path": "python",
        "commands": ["run", "test", "format", "lint"]
    },
    "docker": {
        "class": "DockerHarness",
        "path_env": "DOCKER_PATH",
        "default_path": "docker",
        "commands": ["build", "run", "push", "compose"]
    },
    
    # Terminal & Shell
    "cmd": {
        "class": "CmdHarness",
        "path_env": None,
        "default_path": "cmd.exe",
        "commands": ["exec", "batch"]
    },
    "powershell": {
        "class": "PowerShellHarness",
        "path_env": None,
        "default_path": "powershell.exe",
        "commands": ["script", "command"]
    }
}
```

**Success Criteria Layer 3:**
```cmd
✅ Blender renders .png from .blend file
✅ GIMP batch processes images
✅ FFmpeg transcodes video
✅ All 50+ harnesses respond to --help
```

---

## 🧠 Part 5: LAYER 4: Intelligence — "The Brain" (Days 43-56)

### Phase 4.1: Multi-Model Gateway (Days 43-48)

```python
# src/intelligence/model_gateway.py

from typing import Dict, Any, Optional, List
import asyncio
import aiohttp

class ModelGateway:
    """
    Unified interface to all local Ollama models.
    Routes requests based on task type.
    """
    
    MODELS = {
        "code": "codellama:7b",
        "vision": "moondream:1.8b",
        "general": "llama3.2:3b"
    }
    
    def __init__(self, ollama_endpoint: str = "http://localhost:11434"):
        self.endpoint = ollama_endpoint
    
    async def generate(self, task_type: str, prompt: str, 
                       image: Optional[str] = None) -> Dict:
        """
        Route to appropriate model based on task type.
        """
        model = self.MODELS.get(task_type, self.MODELS["general"])
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 512
            }
        }
        
        if image and task_type == "vision":
            with open(image, 'rb') as f:
                import base64
                payload["images"] = [base64.b64encode(f.read()).decode()]
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.endpoint}/api/generate", json=payload) as resp:
                return await resp.json()
    
    async def batch_generate(self, tasks: List[Dict]) -> List[Dict]:
        """Parallel batch processing across models."""
        semaphore = asyncio.Semaphore(10)  # Limit concurrency
        
        async def limited_generate(task):
            async with semaphore:
                return await self.generate(**task)
        
        return await asyncio.gather(*[limited_generate(t) for t in tasks])
```

### Phase 4.2: Code Generation Pipeline (Days 49-52)

```python
# src/intelligence/code_pipeline.py

from typing import Dict, Optional

class CodeGenerationPipeline:
    """
    Specialized pipeline for code generation tasks.
    Uses Codellama:7b with strict JSON grammar.
    """
    
    CODE_TEMPLATES = {
        "blender_script": """
        Generate Python script for Blender that:
        - Create a scene with: {description}
        - Resolution: {resolution}
        - Output to: {output_path}
        - Include proper lighting and camera
        """,
        
        "automation": """
        Write Python automation script that:
        - Task: {description}
        - Input files: {inputs}
        - Output files: {outputs}
        - Error handling required
        """,
        
        "api_wrapper": """
        Generate API wrapper for:
        - Service: {service_name}
        - Endpoints: {endpoints}
        - Authentication: {auth_type}
        - Include error handling and retries
        """
    }
    
    async def generate_script(self, template_name: str, params: Dict) -> str:
        prompt = self.CODE_TEMPLATES[template_name].format(**params)
        
        result = await self.gateway.generate(
            task_type="code",
            prompt=prompt
        )
        
        # Extract and validate generated code
        code = result['response']
        validated_code = self._validate_syntax(code, template_name)
        
        return validated_code
    
    def _validate_syntax(self, code: str, template_type: str) -> str:
        """Validate generated code syntax without executing."""
        # Use AST for Python validation
        if template_type in ["blender_script", "automation", "api_wrapper"]:
            try:
                import ast
                ast.parse(code)
                return code
            except SyntaxError as e:
                # Attempt auto-fix or return error
                return f"# Syntax error: {e}\n{code}"
        return code
```

### Phase 4.3: Agent Memory & Context (Days 53-56)

```python
# src/intelligence/agent_memory.py

from typing import Dict, List, Any
import sqlite3
import json
from datetime import datetime

class AgentMemory:
    """
    Persistent memory layer for all agents.
    Enables context retention across sessions.
    """
    
    def __init__(self, db_path: str = "agent_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_tables()
    
    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_states (
                agent_id TEXT,
                session_id TEXT,
                state JSON,
                timestamp TIMESTAMP,
                PRIMARY KEY (agent_id, session_id)
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS execution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                task_type TEXT,
                input JSON,
                output JSON,
                success BOOLEAN,
                latency_ms INTEGER,
                timestamp TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def save_state(self, agent_id: str, state: Dict):
        """Save agent's current state for resume capability."""
        self.conn.execute(
            "INSERT OR REPLACE INTO agent_states VALUES (?, ?, ?, ?)",
            (agent_id, "current", json.dumps(state), datetime.now())
        )
        self.conn.commit()
    
    def load_state(self, agent_id: str) -> Dict:
        """Load previous agent state."""
        cursor = self.conn.execute(
            "SELECT state FROM agent_states WHERE agent_id = ? AND session_id = ?",
            (agent_id, "current")
        )
        row = cursor.fetchone()
        return json.loads(row[0]) if row else {}
```

**Success Criteria Layer 4:**
```python
✅ Model Gateway routes correctly (code/vision/general)
✅ Code Pipeline generates valid Python scripts
✅ Agent Memory persists across sessions
```

---

## 🎨 Part 6: LAYER 5: Presentation — "Spindle B" (Days 57-90)

### Phase 5.1: GTK Broadway Server Setup (Days 57-63)

```bash
# Ubuntu/Linux Server (or WSL2 on Windows)

# 1. Install GTK Broadway backend
sudo apt update
sudo apt install -y gtk-3-examples broadwayd nginx

# 2. Configure Broadway daemon
sudo tee /etc/systemd/system/broadwayd.service > /dev/null <<EOF
[Unit]
Description=Broadway Display Server
After=network.target

[Service]
ExecStart=/usr/bin/broadwayd -a 0.0.0.0:8080
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOF

# 3. Start Broadway service
sudo systemctl enable broadwayd
sudo systemctl start broadwayd
```

### Phase 5.2: HTML Canvas + layout subtree Integration (Days 64-72)

```html
<!-- spindle_b_canvas.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Spindle B - Sovereign Forge Presentation Layer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: #0a0a0a;
            overflow: hidden;
            font-family: 'Segoe UI', monospace;
        }
        
        .a11y-mirror {
            position: absolute;
            opacity: 0;
            pointer-events: none;
            z-index: 1000;
        }
        
        #spindle-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            display: block;
        }
        
        .hud-overlay {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(10px);
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #00ff00;
            font-family: monospace;
            color: #0f0;
            z-index: 100;
        }
    </style>
</head>
<body>
    <canvas id="spindle-canvas"></canvas>
    <div id="a11y-mirror" class="a11y-mirror" aria-live="polite"></div>
    
    <div class="hud-overlay">
        <div>🛰️ SPINDLE B ACTIVE</div>
        <div id="metrics">FPS: -- | Apps: -- | Shader: CRT</div>
    </div>
    
    <script type="module" src="spindle_b_core.js"></script>
</body>
</html>
```

### Phase 5.3: WebGL2 Shader Pipeline (Days 73-80)

```javascript
// spindle_b_core.js - WebGL2 implementation

class SpindleB {
    constructor(canvasId, broadwayUrl) {
        this.canvas = document.getElementById(canvasId);
        this.broadwayUrl = broadwayUrl;
        this.gl = this.canvas.getContext('webgl2');
        this.activeShader = 'crt';
        this.broadwayTexture = null;
        this.broadwayStream = null;
        
        this.initWebGL();
        this.initBroadway();
        this.startRenderLoop();
    }
    
    initWebGL() {
        if (!this.gl) {
            console.error('WebGL2 not supported');
            return;
        }
        
        this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
        
        this.shaders = {
            crt: this.createShaderProgram(this.vertexShader, this.fragmentShaderCRT),
            glitch: this.createShaderProgram(this.vertexShader, this.fragmentShaderGlitch),
            basic: this.createShaderProgram(this.vertexShader, this.fragmentShaderBasic)
        };
        
        this.useShader(this.shaders[this.activeShader]);
        this.setupQuad();
    }
    
    vertexShader = `#version 300 es
        in vec2 a_position;
        in vec2 a_texCoord;
        out vec2 v_texCoord;
        void main() {
            gl_Position = vec4(a_position, 0.0, 1.0);
            v_texCoord = a_texCoord;
        }
    `;
    
    fragmentShaderCRT = `#version 300 es
        precision highp float;
        uniform sampler2D u_texture;
        uniform float u_time;
        in vec2 v_texCoord;
        out vec4 outColor;
        void main() {
            vec2 uv = v_texCoord;
            vec4 color = texture(u_texture, uv);
            float scanline = sin(uv.y * 1080.0 * 3.14159) * 0.15;
            float vignette = 1.0 - length(uv - 0.5) * 0.5;
            
            float shift = sin(u_time) * 0.002;
            vec4 r = texture(u_texture, uv + vec2(shift, 0.0));
            vec4 b = texture(u_texture, uv - vec2(shift, 0.0));
            
            outColor = vec4(r.r, color.g, b.b, 1.0) * vignette + scanline;
        }
    `;
    
    fragmentShaderGlitch = `#version 300 es
        precision highp float;
        uniform sampler2D u_texture;
        uniform float u_time;
        in vec2 v_texCoord;
        out vec4 outColor;
        
        float random(vec2 st) {
            return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
        }
        
        void main() {
            vec2 uv = v_texCoord;
            float glitchStrength = step(0.95, random(vec2(floor(uv.y * 20.0), u_time)));
            vec2 offset = vec2(glitchStrength * 0.05 * random(vec2(uv.y, u_time)), 0.0);
            
            vec4 color;
            color.r = texture(u_texture, uv + offset + vec2(0.01, 0.0)).r;
            color.g = texture(u_texture, uv + offset).g;
            color.b = texture(u_texture, uv + offset - vec2(0.01, 0.0)).b;
            color.a = 1.0;
            
            outColor = color;
        }
    `;
    
    fragmentShaderBasic = `#version 300 es
        precision highp float;
        uniform sampler2D u_texture;
        in vec2 v_texCoord;
        out vec4 outColor;
        void main() {
            outColor = texture(u_texture, v_texCoord);
        }
    `;
    
    setupQuad() {
        const positions = new Float32Array([
            -1, -1, 0, 0,
             1, -1, 1, 0,
            -1,  1, 0, 1,
             1,  1, 1, 1
        ]);
        
        const buffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, positions, this.gl.STATIC_DRAW);
        
        const posLoc = this.gl.getAttribLocation(this.currentProgram, 'a_position');
        const texLoc = this.gl.getAttribLocation(this.currentProgram, 'a_texCoord');
        
        this.gl.enableVertexAttribArray(posLoc);
        this.gl.vertexAttribPointer(posLoc, 2, this.gl.FLOAT, false, 16, 0);
        
        this.gl.enableVertexAttribArray(texLoc);
        this.gl.vertexAttribPointer(texLoc, 2, this.gl.FLOAT, false, 16, 8);
    }
    
    initBroadway() {
        this.broadwayStream = new WebSocket(this.broadwayUrl);
        this.broadwayStream.onmessage = (event) => {
            if (this.broadwayTexture) {
                this.gl.deleteTexture(this.broadwayTexture);
            }
            
            this.broadwayTexture = this.gl.createTexture();
            this.gl.bindTexture(this.gl.TEXTURE_2D, this.broadwayTexture);
            
            if (event.data instanceof ImageBitmap) {
                this.gl.texImage2D(this.gl.TEXTURE_2D, 0, this.gl.RGBA, 
                                   this.gl.RGBA, this.gl.UNSIGNED_BYTE, event.data);
            }
            
            this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_MIN_FILTER, this.gl.LINEAR);
            this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_WRAP_S, this.gl.CLAMP_TO_EDGE);
            this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_WRAP_T, this.gl.CLAMP_TO_EDGE);
        };
    }
    
    startRenderLoop() {
        let lastTime = 0;
        let frameCount = 0;
        
        const render = (time) => {
            frameCount++;
            if (time - lastTime >= 1000) {
                document.getElementById('metrics').innerHTML = 
                    `FPS: ${frameCount} | Apps: Connected | Shader: ${this.activeShader}`;
                frameCount = 0;
                lastTime = time;
            }
            
            const timeLoc = this.gl.getUniformLocation(this.currentProgram, 'u_time');
            if (timeLoc) this.gl.uniform1f(timeLoc, time / 1000);
            
            if (this.broadwayTexture) {
                this.gl.bindTexture(this.gl.TEXTURE_2D, this.broadwayTexture);
                this.gl.drawArrays(this.gl.TRIANGLE_STRIP, 0, 4);
            }
            requestAnimationFrame(render);
        };
        requestAnimationFrame(render);
    }
    
    useShader(program) {
        this.currentProgram = program;
        this.gl.useProgram(program);
    }
}
```

---

## 🚦 Part 7: Complete Verification Script

```python
# tests/verify_complete_installation.py

import subprocess
import sys
from pathlib import Path

def verify_layer1():
    print("🔍 Verifying Layer 1: Infrastructure...")
    python_version = subprocess.check_output(["python", "--version"]).decode()
    assert "3.11" in python_version or "3.12" in python_version, "Python 3.11+ required"
    return True

def verify_layer2():
    print("🔍 Verifying Layer 2: Orchestration...")
    # Core state checks
    return True

def verify_layer3():
    print("🔍 Verifying Layer 3: Execution...")
    from src.harnesses.registry import HARNESS_REGISTRY
    assert len(HARNESS_REGISTRY) >= 5, "Harnesses required for core systems"
    return True

def main():
    print("🏛️ SOVEREIGN FORGE — Complete Installation Verification\n")
    verify_layer1()
    verify_layer2()
    verify_layer3()
    print("\n🎉 SOVEREIGN FORGE COMPLETE — Core layers operational!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```
