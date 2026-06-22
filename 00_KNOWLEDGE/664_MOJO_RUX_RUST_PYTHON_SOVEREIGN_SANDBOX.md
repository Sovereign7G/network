# Mojo, Rux, Rust, & Python Sovereign Sandbox Environment Guide

This document preserves the exact systems engineering layout, troubleshooting steps, and configurations required to maintain, execute, and verify the high-performance multi-language developer sandbox on this workspace.

---

## 1. Operating Environment & Path Topology

The development environment consists of isolated runtimes, native system paths, and a dedicated conda sandbox directory:

```text
               ┌────────────────────────────────────────────────────────┐
               │         GLOBAL HARDWARE FRAME (LINUX MINT NOBLE)       │
               └───────────────────────────┬────────────────────────────┘
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                                                   ▼
┌─────────────────────────────────┐                                 ┌─────────────────────────────────┐
│     GLOBAL SYSTEM RUNTIMES      │                                 │    DEVELOPER-ENV CONDA SANDBOX  │
├─────────────────────────────────┤                                 ├─────────────────────────────────┤
│ • Rust Compiler (rustc 1.96.0)  │                                 │ • Python Engine (3.11.15)       │
│ • Rux Compiler (rux 0.3.1)      │                                 │ • Mojo AI Compiler (1.0.0b2)    │
│   - Built with LLVM libc++      │                                 │ • CMake Toolchain (4.3.4)       │
│   - Located in ~/.local/bin/    │                                 │ • Clang C++26 Dev Tools (22.1)  │
└─────────────────────────────────┘                                 └─────────────────────────────────┘
```

Active environment variables and path mappings must be configured as follows:
```bash
export PATH="/home/cherry/miniforge3/envs/developer-env/bin:$PATH"
```

---

## 2. Mojo AI Compiler (1.0.0b2) Implementation Log

Modular packages and dependencies for version `1.0.0b2` were deployed via Conda (`https://conda.modular.com/max`). Multiple runtime issues were encountered and patched:

### A. Missing `modular.cfg` Configuration Mapping
Mojo searches for `modular.cfg` to resolve package paths and locations. The template configuration from the Conda environment must be placed in the user's home folder:
* **Source:** `/home/cherry/miniforge3/envs/developer-env/share/max/modular.cfg`
* **Target:** `/home/cherry/.modular/modular.cfg`

### B. Broken `std` Module Resolution
During the Conda installation, std libraries were not automatically linked to the active environment's library paths. The `mojoc` files must be manually copied:
* **Source:** `/home/cherry/miniforge3/pkgs/mojo-compiler-1.0.0b2-release/lib/mojo/*`
* **Target:** `/home/cherry/miniforge3/envs/developer-env/lib/mojo/`

### C. Debugger Path Resolution Bug (`unable to resolve the lldb path`)
Mojo checks for the existence of `mojo-lldb` and `libMojoLLDB.so` under the environment prefix. Because the Conda packages do not contain them, the environment's LLVM 18 tools must be symlinked:
```bash
# Link mojo-lldb executable
ln -s /home/cherry/miniforge3/envs/developer-env/bin/lldb /home/cherry/miniforge3/envs/developer-env/bin/mojo-lldb

# Link libMojoLLDB.so plugin library
ln -s /home/cherry/miniforge3/envs/developer-env/lib/liblldb.so /home/cherry/miniforge3/envs/developer-env/lib/libMojoLLDB.so
```

### D. Crashpad Initialization Handler
Mojo utilizes the `modular-crashpad-handler` to trace compilation telemetries. If the environment bin path `/home/cherry/miniforge3/envs/developer-env/bin` is not in the system `$PATH`, Mojo throws a runtime warning. Ensuring the bin path is exported resolves this.

---

## 3. Rux Compiler (0.3.1) Native Source Build Log

Rux is a blazingly fast compiled systems language. Compiling Rux from source under Linux Mint requires satisfying several advanced modern C++ compiler constraints:

### A. CMake 3.31+ Requirement
System apt packages contain `cmake 3.28.3` which is outdated. We installed `cmake 4.3.4` from `conda-forge` inside the `developer-env` environment to support C++26 modules building features.

### B. LLVM `libc++` Dependency & Scanning
Rux is designed to compile using LLVM's `libc++` (`-stdlib=libc++`) and C++26 modules (`-std=gnu++26`). Standard system installations default to GNU's `libstdc++`, causing compilation to fail.
To satisfy this, the following packages must be installed inside the Conda environment:
1. `clangxx`: Installs environment-native `clang++` compiler wrapper.
2. `clang-tools`: Deploys `clang-scan-deps` (LLVM 22) for resolving C++26 modules dependency paths.
3. `libcxx` & `libcxx-devel`: Deploys target standard library headers (e.g. `<span\>`, `<cstdint\>`, `<filesystem\>`).

### C. Compilation & Installation Sequence
```bash
# Clean previous build artifacts
rm -rf /home/cherry/Rux/build

# Configure build directory using CMake 4.3.4 and Conda Clang++
/home/cherry/miniforge3/envs/developer-env/bin/cmake -S /home/cherry/Rux -B /home/cherry/Rux/build -G Ninja \
  -DCMAKE_CXX_COMPILER=/home/cherry/miniforge3/envs/developer-env/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release

# Compile the targets
/home/cherry/miniforge3/envs/developer-env/bin/cmake --build /home/cherry/Rux/build

# Install cleanly to local user path
/home/cherry/miniforge3/envs/developer-env/bin/cmake --install /home/cherry/Rux/build --prefix /home/cherry/.local
```

---

## 4. Verification Guides

### A. Mojo Test Module (`hello.mojo`)
File content:
```python
def main():
    print("Hello from Mojo!")
```
Command to verify:
```bash
export PATH="/home/cherry/miniforge3/envs/developer-env/bin:$PATH"
mojo hello.mojo
```
Expected output:
```text
Hello from Mojo!
```

### B. Rux Version Check
Command:
```bash
rux --version
```
Expected output:
```text
Rux 0.3.1 (yyyy-mm-dd hh:mm:ss)
```
