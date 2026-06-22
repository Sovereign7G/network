# 🏛️ AGE REPUBLIC: KNOWLEDGE ASSET (ERA 225.0)
## Identifier: `00_KNOWLEDGE/335_I_REPUBLIC_GEMMA4_TOOL_CALLING_WISDOM`
## Theme: Easy Agentic Tool Calling with Gemma 4 — Confined Local File Systems and Restricted Code Execution Sandboxes

---

> [!IMPORTANT]
> **SYSTEM COMPACT-AGENTIC TOOL-CALLING BLUEPRINT:**
> This knowledge manifest formalizes the operational principles, security boundaries, and runtime execution loops of **Agentic Tool Calling with Gemma 4** (KDnuggets/Matthew Mayo). It establishes standard designs for local path-traversal guards (`SAFE_BASE_DIR`), restricted Python interpreters using whitelisted standard builtins, multi-tool sequencing, and secure error recovery.

---

## 🧭 I. The Problem Argument (Status Quo)

**Premise:** When tool-calling agents are limited entirely to read-only remote Web APIs, they remain chatbots rather than true agents — performing retrieval-augmented synthesis without environmental awareness or execution authority.

**The failure modes of remote-only tool calling:**
- **No notion of environment:** The model cannot inspect the system it is running on.
- **No state to verify:** The model is forced to guess folder contents or API schemas.
- **Precise logic limits:** Small models (like 2-billion-parameter edge models) reliably fail at exact arithmetic, standard deviations, and multi-step math if they try to calculate values within their own weights.
- **Opaque error feedback:** Empty outputs return silently, causing the model to confidently fabricate values.

**Implicit Claim:** True "agency" arises when a model interacts with its local host system. The moment a tool reads files or runs code, the design problem shifts from "how do I parse a JSON response" to "how do I restrict execution to a safe sandbox boundary."

---

## 🏛️ II. The Core Thesis (Solution)

**Proposition:** Fusing **Gemma 4** (`gemma4:e2b`) with a confined directory scanner and a restricted Python execution loop creates a fully grounded local agent capable of observing its environment and running deterministic arithmetic, without risking host system compromise.

**The Local Execution Pipeline:**
```
Prompt → Parse Tool Schema → Confined Resolution → Sandbox Exec → Standard Output Redirect → Re-query Response
```

**The Two Pillars of Confined Local Agency:**
1. **Confined Directory Contents (`list_directory_contents`):** Standardizes path-normalizations that reject traversal inputs (e.g. `../../etc` or `/`) before file queries execute.
2. **Restricted Python Interpreter (`execute_python_code`):** Strips the default `__builtins__` namespace down to a small math/stats whitelist, intercepting hostile introspections (`().__class__.__mro__`).

---

## 🔬 III. The Architectural & Security Arguments

### Argument A: Secure Path-Traversal Resolution
To prevent the model's curiosity from wandering into sensitive system directories, the filesystem explorer binds a fixed workspace path at launch:

```python
# Confine list_directory_contents to the permissible base directory
SAFE_BASE_DIR = os.path.abspath(os.getcwd())

def list_directory_contents(path: str = ".") -> str:
    # Normalize path and normalize '..' out of existence
    requested = os.path.abspath(os.path.join(SAFE_BASE_DIR, path))
    
    # Prefix verification check: reject access if outside safe tree
    if not (requested == SAFE_BASE_DIR or requested.startswith(SAFE_BASE_DIR + os.sep)):
        return f"Error: Access denied. Path is outside permitted workspace."
    
    # Safely perform os.listdir
    entries = sorted(os.listdir(requested))
    ...
```

**Argument:** We never trust the raw string produced by the model. Joining it onto the base, resolving it absolutely (normalizing `..`), and verifying the prefix ensures absolute directory isolation.

### Argument B: Builtins-Whitelisted Code Execution
To allow deterministic math (e.g. standard deviations) without exposing the host, `exec()` is run with a stripped global namespace:

```python
# Whitelist only safe, stateless operations
safe_builtins = {
    "abs": abs, "all": all, "any": any, "bool": bool, "dict": dict,
    "divmod": divmod, "enumerate": enumerate, "filter": filter,
    "float": float, "int": int, "len": len, "list": list, "map": map,
    "max": max, "min": min, "pow": pow, "print": print, "range": range,
    "repr": repr, "reversed": reversed, "round": round, "set": set,
    "sorted": sorted, "str": str, "sum": sum, "tuple": tuple, "zip": zip,
}

restricted_globals = {
    "__builtins__": safe_builtins,
    "math": math,
    "statistics": statistics,
}
```

**Argument:** Stripping `__builtins__` makes functions like `open`, `eval`, `compile`, and `__import__` non-existent inside the snippet. High-frequency calculation libraries (`math`, `statistics`) are pre-imported to prevent the model from needing to use runtime imports.

### Argument C: Explicit stdout Redirection & Empty Output Retries
Executing code requires collecting standard out via string buffers:

```python
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    exec(code, restricted_globals, {})
output = buffer.getvalue().strip()

if not output:
    return "Code executed successfully but produced no output. Use print() to return a value."
```

**Argument:** Small models frequently assign expressions (e.g. `x = sum(range(101))`) and forget to call `print(x)`. Returning a specific error detailing how to use print gives the orchestration loop a target to retry, preventing the model from hallucinating a final value based on empty output.

---

## 📊 IV. Empirical Evidence: Multi-Tool Sequencing

When tested under sequential execution on a standard local CPU, `gemma4:e2b` successfully coordinates multiple tools:

* **Prompt:** *"Look at the files in the current folder and tell me the total size in kilobytes, rounded to two decimal places."*
* **Sequence executed:**
  1. Calls `list_directory_contents(path='.')`.
  2. Receives a structured file list: `README.md (412 bytes)`, `csv_cleaner.py (1834 bytes)`, `main.py (10786 bytes)`.
  3. Formulates a Python script using retrieved sizes: `sizes = [412, 1834, 10786, 88, 2210]\nprint(round(sum(sizes)/1024, 2))`.
  4. Calls `execute_python_code()` with the script.
  5. Receives `15.33` from standard out and synthesizes the correct final response.

---

## 🏛️ V. The Design Philosophy

### Principle 1: Separate Hallucination from Observation
A model's weights cannot accurately track state. The directory tool grounds the model in what is actually *there*; the interpreter grounds the model in what is actually *true*. The model's role is to decide *which question* to ask of *which tool*.

### Principle 2: Build the Perimeter First
Security is a system-level constraint. Build the sandbox, whitelist the paths, and strip the builtins *before* exposing APIs to model generation.

### Principle 3: Degrade Gracefully to Useful Error Tokens
Hostile actions (e.g., trying to read `/etc`) must fail into standard, parsing-friendly error strings (`NameError`, `Access denied`) rather than crashing the loop, enabling the model to report its limits.
