# 🏛️ AGE REPUBLIC: KNOWLEDGE ASSET (ERA 225.0)
## Identifier: `00_KNOWLEDGE/339_B_REPUBLIC_GEMMA4_TOOL_CALLING_ANALYSIS_WISDOM`
## Theme: Gemma 4 Tool Calling Security Analysis — Resolve-Then-Verify, Whitelisted namespaces, and Chained Local Operations

---

> [!IMPORTANT]
> **EDGE SANDBOX AUDIT MANIFEST:**
> This manifest formalizes the security designs, empirical findings, and architectural principles derived from the **Gemma 4 agentic Tool Calling** framework. It establishes a robust blueprint for local containment, whitelisted code execution loops, resolve-then-verify path traversal blocks, and multi-tool chaining on Edge hardware.

---

## 🧭 I. The Problem Argument (Status Quo)

**Premise:** Most "agentic" tool-calling demonstrations are not truly agentic — they are chatbots with read-only web API access, which is "more akin to retrieval augmented generation than true agency."

**The critique of web-API-only agents:**
> *"When the only tools you give a language model are read-only web APIs, essentially you still really have a chatbot, albeit one with potential access to better information. The model receives a prompt, decides which API to ping, and stitches the JSON response into a paragraph. There is no real notion of environment, no state to inspect, no consequence to reason about."*

**What true agency requires:**
> *"Agency, in the practical sense practitioners use the word, shows up when a model starts interacting with the system it is running on. That can mean reading from a local filesystem, executing code, modifying files, calling other processes, or any combination of those."*

**Implicit Claim:** The distinguishing feature of an agentic system is not tool calling per se — it is the ability to interact with a **stateful environment** where actions have consequences that must be reasoned about. Web API calls are stateless and consequence-free; local filesystem and code execution are not.

---

## 🏛️ II. The Core Thesis (Solution)

**Proposition:** Give Gemma 4 (specifically the `gemma4:e2b` edge variant) two tools that run code on the local machine — a sandboxed filesystem explorer and a restricted Python interpreter — and observe the model decide, on its own, when to look around and when to compute.

**The two tools:**
| Tool | Function | Risk | Safeguard |
| :--- | :--- | :--- | :--- |
| **`list_directory_contents`** | Inspect local filesystem | Path traversal to sensitive files | Path resolution + prefix check against `SAFE_BASE_DIR` |
| **`execute_python_code`** | Run arbitrary Python snippets | Code execution, file access, system calls | Whitelisted `__builtins__`, no `open`, `eval`, or `__import__` |

**Key capability demonstrated:** The model can chain tools — using `list_directory_contents` to discover file sizes, then `execute_python_code` to compute total kilobytes — producing grounded answers that combine observation and calculation.

---

## 🔬 III. The Technical Arguments (Architectural Decisions)

### Argument A: Read-Only Web APIs Are Not Agency
| Dimension | Web API Tools | Local Filesystem + Code Tools |
| :--- | :--- | :--- |
| **Statefulness** | Stateless | Stateful (files exist, code runs) |
| **Consequences** | None | Can read/write/execute |
| **Reasoning required** | Which API to call? | What files exist? What does this code evaluate to? |
| **Failure mode** | Invalid JSON | Path traversal, code injection |

**Argument:** The moment a tool can do something other than return a clean string from a remote service, the model has to start asking about its environment: *"what files exist, what does this number actually equal, what is in this folder before I claim it contains anything."* That questioning is the essence of agency.

### Argument B: Path Traversal Protection via Resolve-Then-Verify
**The naive approach (rejected):**
```python
os.listdir(path)  # path = "../../etc" — walks right out of the sandbox
```
**The secure pattern:**
```python
SAFE_BASE_DIR = os.path.abspath(os.getcwd())
requested = os.path.abspath(os.path.join(SAFE_BASE_DIR, path))
if not requested.startswith(SAFE_BASE_DIR + os.sep):
    return "Error: Access denied."
```
**Why this works:**
1. Join user-provided path to base directory
2. Resolve absolutely (normalizes `..` and `.`)
3. Verify resolved path still starts with base directory
4. Reject if outside

**Argument:** Never trust the string the model produced. Normalize it, resolve it, then verify it is still inside the permitted workspace before performing any I/O.

### Argument C: Whitelist-Based Builtins for Python Interpreter
**The naive approach (rejected):**
```python
exec(code)  # Full access to everything — open(), eval(), __import__()
```
**The secure pattern:**
```python
safe_builtins = {
    "abs": abs, "len": len, "print": print, "range": range,
    "int": int, "str": str, "list": list, "dict": dict,
    # ... no open, no eval, no __import__, no exec
}
restricted_globals = {
    "__builtins__": safe_builtins,
    "math": math,
    "statistics": statistics,
}
exec(code, restricted_globals, {})
```
**Why whitelist over blacklist:**
- Blacklisting `open` is fragile (model could use `().__class__.__mro__...`)
- Whitelisting defines exactly what is available
- Functions not in the whitelist simply do not exist in the snippet's namespace

**Limitation acknowledged:**
> *"A determined adversary can break out of a Python `exec` sandbox in a dozen ways... For a single-user agent running on your own laptop on your own prompts, the whitelist is plenty. For anything else, you would want a real isolation layer — a subprocess with seccomp, a container, or RestrictedPython."*

### Argument D: Empty Output Detection Enables Retry
**The pattern:**
```python
output = buffer.getvalue().strip()
if not output:
    return "Code executed successfully but produced no output. Use print() to return a value."
```
**Why this matters:**
> *"Small models will routinely write expressions like `x = sum(range(101))` and forget the `print(x)`. Returning a specific error telling them to use `print()` gives the orchestration loop the option to retry; without it, the model would synthesize a final answer based on an empty string and confidently invent a value."*

**Argument:** Tool outputs should guide the model toward correct usage. An empty output is ambiguous; a specific error message ("use print()") is instructional.

### Argument E: The Two-Pass Orchestration Pattern
**The loop structure:**
1. Query model with user prompt + tool registry (JSON schema)
2. If response contains `tool_calls`, dispatch each to `TOOL_FUNCTIONS`
3. Append tool result as `{"role": "tool", "content": str(result)}`
4. Re-query model with enriched payload
5. Model produces grounded final answer

**Why two passes:**
- First pass: model decides which tools to call and with what arguments
- Second pass: model synthesizes final answer from tool results

**Argument:** Separating tool selection from answer synthesis is more reliable than forcing the model to do both in one generation.

---

## 📊 IV. The Empirical Arguments (Test Results)

### Test 1: Filesystem Inspection Only
* **Prompt:** *"What scripts are in my current folder, and which one looks like it should be used to process CSVs?"*
* **Model action:** Called `list_directory_contents(path='.')`
* **Tool result:** Listed five files including `csv_cleaner.py`.
* **Model response:** Correctly selected `csv_cleaner.py` based on semantic name comparison.

### Test 2: Python Interpreter Only
* **Prompt:** *"What is the standard deviation of the numbers 12, 18, 23, 24, 29, 31, 35, 41, 44, 47, rounded to four decimal places?"*
* **Model action:** Called `execute_python_code` with snippet using `statistics.stdev`
* **Tool result:** `Output: 11.4659`
* **Model response:** Correctly reported `11.4659` with zero local model math calculations or approximations.

### Test 3: Chained Tools (Filesystem → Calculation)
* **Prompt:** *"Look at the files in the current folder and tell me the total size in kilobytes, rounded to two decimal places."*
* **Model actions (in sequence):**
  1. `list_directory_contents(path='.')` → returns file sizes
  2. `execute_python_code` with snippet summing sizes and converting to KB
* **Tool results:** File sizes → `Output: 15.33`
* **Model response:** Correctly computed `15.33 KB` by chaining observation and execution.

### Test 4: Safety Guard Verification
* **Attempted path traversal:** Listing `/etc` -> Tool returns access denied; model reports the denial gracefully.
* **Attempted code injection:** `open('/etc/passwd').read()` -> `NameError` (open is not in whitelisted builtins).

---

## 🏛️ V. The Design Philosophy

### Principle 1: Agency Requires Environment Interaction
True agency is not about calling APIs — it is about observing and acting upon a stateful environment. Web APIs are stateless; local files and code execution are not.

### Principle 2: Build the Perimeter First
Safety is not an afterthought — it is the foundation. Define the safe base directory before the model can inspect files. Whitelist builtins before the model can execute code. The perimeter determines what the model is allowed to touch.

### Principle 3: Resolve, Then Verify (Never Trust the String)
Path traversal is trivial to prevent with resolve-then-verify. There is no excuse for naive `os.listdir(user_input)`.

### Principle 4: Whitelist Over Blacklist for Security
Blacklisting is brittle — attackers find functions you forgot to block. Whitelisting defines exactly what is allowed; everything else is impossible.

### Principle 5: Tool Outputs Should Be Instructional on Failure
When a tool fails or produces ambiguous output, the error message should guide the model toward correct usage. Silent failure leads to hallucinated answers.

### Principle 6: Small Models + Local Execution Are Sufficient
You do not need a frontier model (GPT-5, Claude Opus) for agentic tool calling. A 2-billion-parameter model running on a laptop with no GPU can successfully chain filesystem inspection and code execution tools.

---

## 🚫 VI. The Anti-Arguments (What the Tutorial Rejects)

| Rejected Practice | Tutorial Alternative |
| :--- | :--- |
| **Read-only web APIs as "agentic"** | Local filesystem + code execution (stateful, consequential) |
| **Naive path joining** | Resolve-then-verify with prefix check |
| **Blacklisting dangerous functions** | Whitelisting allowed builtins |
| **Silent failure on empty output** | Instructional error ("use print()") |
| **Single-pass tool calling** | Two-pass orchestration (selection → synthesis) |
| **Large cloud-only models** | Small local models (Gemma 4 on Ollama) |
| **Untrusted code execution without safeguards** | Whitelisted builtins, no `open`, no `eval` |

---

## 🏛️ VII. Final Wisdom

> *"Build the perimeter first. Then hand the model the keys to whatever sits inside it."*

The tutorial's most important contribution is the **security-first design philosophy**. Before giving a model the ability to read files or execute code, define exactly what it is allowed to touch: a safe base directory, a whitelist of builtins, pre-imported safe modules. The perimeter is not an afterthought; it is the foundation. Once the perimeter is built, you can confidently hand the model the keys to everything inside — and observe genuine agency emerge as it inspects, computes, and chains tools to answer questions grounded in observation, not hallucination.
