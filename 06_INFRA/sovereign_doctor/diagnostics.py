#!/usr/bin/env python3
"""Sovereign Doctor - Diagnostics Module under 400 lines"""

import subprocess
import socket
import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple

def is_port_open(port: int, host: str = "localhost") -> bool:
    """Check if a port is listening"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def run_cmd(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            env=os.environ.copy()
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def check_systemd_service(service_name: str) -> Dict[str, Any]:
    """Check systemd service status"""
    code, stdout, stderr = run_cmd(["systemctl", "--user", "is-active", service_name])
    is_active = (code == 0)
    
    code, stdout, stderr = run_cmd(["systemctl", "--user", "is-enabled", service_name])
    is_enabled = (code == 0)
    
    return {
        "name": service_name,
        "active": is_active,
        "enabled": is_enabled,
        "status": "✅ running" if is_active else "❌ stopped"
    }

def run_full_diagnostic() -> Dict[str, Any]:
    """Complete system diagnostic"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "services": {},
        "config_issues": [],
        "log_errors": [],
        "port_status": {},
        "recommendations": []
    }
    
    # 1. Check all services
    services = {
        "router": {"port": 9877, "systemd": "age-local-router"},
        "bifrost": {"port": 8080, "systemd": "age-bifrost-gateway"},
        "ollama": {"port": 11434, "cmd": "ollama"},
        "litellm": {"port": 4000, "cmd": "litellm"}
    }
    
    for name, config in services.items():
        port_ok = is_port_open(config["port"]) if config.get("port") else False
        service_ok = check_systemd_service(config["systemd"]) if config.get("systemd") else None
        
        report["services"][name] = {
            "port": config["port"],
            "port_open": port_ok,
            "service_active": service_ok["active"] if service_ok else None,
            "status": "✅ operational" if (port_ok or not config.get("port")) else "❌ down"
        }
        report["port_status"][config["port"]] = "✅ open" if port_ok else "❌ closed"
    
    # 2. Check Continue config
    config_path = Path.home() / ".continue" / "config.yaml"
    if config_path.exists():
        try:
            with open(config_path, encoding='utf-8') as f:
                config = yaml.safe_load(f)
            if not config.get("models"):
                report["config_issues"].append("Missing 'models' section in Continue config")
            if not config.get("embeddingsProvider"):
                report["config_issues"].append("Missing 'embeddingsProvider' section")
        except Exception as e:
            report["config_issues"].append(f"Failed to parse config.yaml: {e}")
    else:
        report["config_issues"].append("~/.continue/config.yaml not found")
    
    # 3. Check for malformed rule files
    rules_dir = Path.cwd() / ".agents" / "rules"
    if rules_dir.exists():
        for rule_file in rules_dir.glob("*.md"):
            content = rule_file.read_text(encoding='utf-8')
            if "trigger: always_on" in content:
                report["config_issues"].append(f"Malformed rule: {rule_file.name} uses 'trigger: always_on'")
    
    # 4. Scan Continue logs
    log_path = Path.home() / ".continue" / "logs" / "cn.log"
    if log_path.exists():
        content = log_path.read_text(encoding='utf-8', errors='ignore')
        error_patterns = [
            ("rules.1: Invalid input", "Malformed rule frontmatter"),
            ("ResponseError", "API call failed (Sovereign Preload issue)"),
            ("Errno 5", "Input/output error (orphaned process)"),
            ("ECONNREFUSED", "Connection refused to localhost")
        ]
        for pattern, diagnosis in error_patterns:
            if pattern in content:
                report["log_errors"].append(f"Found '{pattern}': {diagnosis}")
    
    # 5. Generate recommendations
    for name, svc in report["services"].items():
        if "❌" in svc["status"]:
            report["recommendations"].append(f"Restart {name}: run `restart_service('{name}')`")
    
    if any("Malformed rule" in issue for issue in report["config_issues"]):
        report["recommendations"].append("Fix rule files: run `repair_rule_frontmatter()`")
    
    if any("missing" in issue.lower() for issue in report["config_issues"]):
        report["recommendations"].append("Validate Continue config: run `validate_continue_config()`")
    
    if report["log_errors"]:
        report["recommendations"].append("Check system logs: run `scan_journal_logs('age-local-router')`")
    
    return report

def _validate_continue_config() -> Dict[str, Any]:
    """Validate Continue config.yaml for common schema errors"""
    result = {
        "valid": False,
        "errors": [],
        "warnings": [],
        "suggestions": []
    }
    
    config_path = Path.home() / ".continue" / "config.yaml"
    
    if not config_path.exists():
        result["errors"].append("~/.continue/config.yaml not found")
        return result
    
    try:
        with open(config_path, encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result["errors"].append(f"Invalid YAML: {e}")
        return result
    except Exception as e:
        result["errors"].append(f"Failed to read config: {e}")
        return result
    
    # Check required sections
    required_sections = ["models", "embeddingsProvider"]
    for section in required_sections:
        if section not in config:
            result["errors"].append(f"Missing '{section}' section")
        elif not isinstance(config[section], dict if section == "embeddingsProvider" else list):
            result["errors"].append(f"'{section}' has incorrect type")
    
    # Validate models
    if "models" in config and isinstance(config["models"], list):
        for i, model in enumerate(config["models"]):
            if "name" not in model:
                result["warnings"].append(f"Model {i} missing 'name'")
            if "model" not in model:
                result["warnings"].append(f"Model {i} missing 'model' field")
    
    # Validate embeddings provider
    if "embeddingsProvider" in config and isinstance(config["embeddingsProvider"], dict):
        ep = config["embeddingsProvider"]
        if "provider" not in ep:
            result["errors"].append("embeddingsProvider missing 'provider'")
        if "model" not in ep:
            result["errors"].append("embeddingsProvider missing 'model'")
    
    # Check for rule files
    rules_dir = Path.cwd() / ".agents" / "rules"
    import re
    if rules_dir.exists():
        for rule_file in rules_dir.glob("*.md"):
            content = rule_file.read_text(encoding='utf-8')
            if "trigger: always_on" in content:
                result["warnings"].append(f"Rule file {rule_file.name} uses deprecated 'trigger: always_on'")
                result["suggestions"].append(f"Run repair_rule_frontmatter('{rule_file}') to fix")
    
    result["valid"] = len(result["errors"]) == 0
    
    if result["valid"]:
        result["suggestions"].append("Config is valid. Run full_diagnostic() for service health check.")
    
    return result

def _scan_journal_logs(service: str = "age-local-router", lines: int = 100) -> Dict[str, Any]:
    """Scan systemd journal logs for errors and warnings"""
    result = {
        "service": service,
        "lines_scanned": lines,
        "errors": [],
        "warnings": [],
        "info": []
    }
    
    # Get journal logs
    code, stdout, stderr = run_cmd([
        "journalctl", "--user", "-u", service, "-n", str(lines), "--no-pager", "--output=short"
    ])
    
    if code != 0:
        result["errors"].append(f"Failed to read journal: {stderr}")
        return result
    
    if not stdout.strip():
        result["info"].append(f"No logs found for {service}")
        return result
    
    # Parse log lines
    for line in stdout.split('\n'):
        line_lower = line.lower()
        if any(term in line_lower for term in ['error', 'exception', 'fail', 'fatal']):
            result["errors"].append(line[:200])  # Truncate long lines
        elif any(term in line_lower for term in ['warn', 'timeout', 'deprecated']):
            result["warnings"].append(line[:200])
    
    # Add summary
    result["summary"] = {
        "total_errors": len(result["errors"]),
        "total_warnings": len(result["warnings"])
    }
    
    return result
API_SECRET = "super_secret_sovereign_token_12345"

