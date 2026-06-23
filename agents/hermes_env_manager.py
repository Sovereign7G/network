#!/usr/bin/env python3
"""Hermes Environment Manager Agent"""
import subprocess
import os
from datetime import datetime
from typing import Dict


class HermesEnvironmentManager:
    def __init__(self):
        self.name = "hermes_environment_manager"
        self.env_prefix = "/home/cherry/miniforge3/envs/developer-env"
        self.home_dir = "/home/cherry"

    def check_mojo_status(self) -> Dict:
        status = {"status": "ok", "checks": {}}
        mojo_path = f"{self.env_prefix}/bin/mojo"
        if os.path.exists(mojo_path):
            status["checks"]["mojo_binary"] = "found"
            try:
                res = subprocess.run([mojo_path, "--version"], capture_output=True, text=True)
                status["checks"]["mojo_version"] = res.stdout.strip()
            except Exception as e:
                status["checks"]["mojo_version"] = f"error checking version: {e}"
        else:
            status["checks"]["mojo_binary"] = "missing"
            status["status"] = "degraded"
        cfg_path = f"{self.home_dir}/.modular/modular.cfg"
        status["checks"]["modular_cfg"] = "found" if os.path.exists(cfg_path) else "missing"
        if status["checks"]["modular_cfg"] == "missing":
            status["status"] = "degraded"
        lldb_link = f"{self.env_prefix}/bin/mojo-lldb"
        status["checks"]["mojo_lldb_link"] = "active" if os.path.islink(lldb_link) else "inactive"
        lib_link = f"{self.env_prefix}/lib/libMojoLLDB.so"
        status["checks"]["lib_mojo_lldb_link"] = "active" if os.path.islink(lib_link) else "inactive"
        std_dir = f"{self.env_prefix}/lib/mojo"
        if os.path.exists(f"{std_dir}/std.mojoc") and os.path.exists(f"{std_dir}/layout.mojoc"):
            status["checks"]["mojo_std_libraries"] = "linked"
        else:
            status["checks"]["mojo_std_libraries"] = "missing"
            status["status"] = "degraded"
        return status

    def check_rux_status(self) -> Dict:
        status = {"status": "ok", "checks": {}}
        rux_path = f"{self.home_dir}/.local/bin/rux"
        if os.path.exists(rux_path):
            status["checks"]["rux_binary"] = "found"
            try:
                res = subprocess.run([rux_path, "--version"], capture_output=True, text=True)
                status["checks"]["rux_version"] = res.stdout.strip()
            except Exception as e:
                status["checks"]["rux_version"] = f"error checking version: {e}"
        else:
            status["checks"]["rux_binary"] = "missing"
            status["status"] = "degraded"
        cmake_path = f"{self.env_prefix}/bin/cmake"
        if os.path.exists(cmake_path):
            try:
                res = subprocess.run([cmake_path, "--version"], capture_output=True, text=True)
                status["checks"]["cmake_version"] = res.stdout.strip().split("\n")[0]
            except Exception as e:
                status["checks"]["cmake_version"] = f"error: {e}"
        else:
            status["checks"]["cmake_version"] = "missing from conda environment"
        scan_deps = f"{self.env_prefix}/bin/clang-scan-deps"
        status["checks"]["clang_scan_deps"] = "found" if os.path.exists(scan_deps) else "missing"
        return status

    def check_rust_status(self) -> Dict:
        status = {"status": "ok", "checks": {}}
        try:
            res = subprocess.run(["rustc", "--version"], capture_output=True, text=True)
            status["checks"]["rustc_version"] = res.stdout.strip()
        except Exception as e:
            status["checks"]["rustc_version"] = f"unavailable: {e}"
            status["status"] = "degraded"
        return status

    def run_full_environment_audit(self) -> Dict:
        mojo = self.check_mojo_status()
        rux = self.check_rux_status()
        rust = self.check_rust_status()
        overall = "healthy"
        if mojo["status"] == "degraded" or rux["status"] == "degraded" or rust["status"] == "degraded":
            overall = "degraded"
        return {"status": overall, "mojo_audit": mojo, "rux_audit": rux,
                "rust_audit": rust, "timestamp": datetime.now().isoformat()}
