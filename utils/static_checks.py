# utils/static_checks.py

def check_dockerfile(content):
    warnings = []
    if "HEALTHCHECK" not in content:
        warnings.append("Dockerfile is missing a HEALTHCHECK instruction.")
    if "FROM python" in content and ":" not in content.split("FROM python")[1]:
        warnings.append("Base image is not version-pinned (e.g., use python:3.10).")
    return warnings

def check_requirements(content):
    warnings = []
    for line in content.strip().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "==" not in line:
            warnings.append(f"Unpinned dependency: {line}")
    return warnings

