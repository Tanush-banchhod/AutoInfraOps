from dotenv import load_dotenv
import os
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.llm_agent import suggest_improvements # Ensure the current working directory is treated as the root
sys.path.insert(0, os.path.abspath("."))  # Forces Python to treat CWD as root
from utils.static_checks import check_dockerfile, check_requirements

load_dotenv()                        # pulls vars from .env
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def _gh(url: str):
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def repo_info(owner: str, repo: str):
    return _gh(f"https://api.github.com/repos/{owner}/{repo}")

def open_issues(owner: str, repo: str):
    return _gh(f"https://api.github.com/repos/{owner}/{repo}/issues")

def workflow_files(owner: str, repo: str):
    path = ".github/workflows"
    items = _gh(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}")
    return [f["name"] for f in items if f["name"].endswith((".yml", ".yaml"))]

def get_file_content(owner: str, repo: str, filepath: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    content = resp.json()
    if content.get("encoding") == "base64":
        import base64
        return base64.b64decode(content["content"]).decode("utf-8")
    return None

def create_github_issue(owner, repo, title, body, labels=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": labels or []
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        print(f"✅ Created issue: {title}")
        return response.json() # Returns the created issue JSON
    elif response.status_code == 422:
        print(f"⚠️ Issue already exists: {title}")
    else:
        print(f"❌ Failed to create issue: {title} ({response.status_code})")
        print(response.json())

def extract_owner_repo(repo_url: str):
    """
    Extracts owner and repo name from GitHub URL.
    Example: https://github.com/Tanush-banchhod/AutoInfraOps
             → ("Tanush-banchhod", "AutoInfraOps")
    """
    try:
        parts = repo_url.strip().rstrip("/").split("/")
        return parts[-2], parts[-1]
    except Exception:
        raise ValueError("Invalid GitHub repo URL")


def analyze_repo(repo_url):
    owner, repo = extract_owner_repo(repo_url)

    docker = get_file_content(owner, repo, "Dockerfile")
    reqs = get_file_content(owner, repo, "requirements.txt")

    docker_warnings = check_dockerfile(docker) if docker else []
    req_warnings = check_requirements(reqs) if reqs else []

    docker_suggestions = suggest_improvements(docker, "Dockerfile") if docker else ""
    req_suggestions = suggest_improvements(reqs, "requirements.txt") if reqs else ""

    issues_created = []

    for warning in docker_warnings:
        issue = create_github_issue(owner, repo, warning, f"Dockerfile Warning:\n\n{warning}", ["docker", "autofix"])
        if issue:
            issues_created.append({
                "title": issue["title"],
                "url": issue["html_url"]
            })

    for warning in req_warnings:
        issue = create_github_issue(owner, repo, warning, f"Requirements Warning:\n\n{warning}", ["dependency", "autofix"])
        if issue:
            issues_created.append({
                "title": issue["title"],
                "url": issue["html_url"]
            })

    if docker_suggestions:
        issue = create_github_issue(owner, repo, "LLM Suggestions: Dockerfile", docker_suggestions, ["ai-review", "docker"])
        if issue:
            issues_created.append({
                "title": issue["title"],
                "url": issue["html_url"]
            })

    if req_suggestions:
        issue = create_github_issue(owner, repo, "LLM Suggestions: requirements.txt", req_suggestions, ["ai-review", "dependency"])
        if issue:
            issues_created.append({
                "title": issue["title"],
                "url": issue["html_url"]
            })

    return {
        "static_warnings": {
            "Dockerfile": docker_warnings,
            "requirements.txt": req_warnings
        },
        "llm_suggestions": {
            "Dockerfile": docker_suggestions,
            "requirements.txt": req_suggestions
        },
        "created_issues": issues_created
    }


if __name__ == "__main__":
    owner, repo = "Tanush-banchhod", "AutoInfraOps"
    print(repo_info(owner, repo)["full_name"])
    print("Issues:", [i["title"] for i in open_issues(owner, repo)])
    print("Workflows:", workflow_files(owner, repo))
    print("Dockerfile:\n", get_file_content(owner, repo, "Dockerfile"))
    print("requirements.txt:\n", get_file_content(owner, repo, "requirements.txt"))





