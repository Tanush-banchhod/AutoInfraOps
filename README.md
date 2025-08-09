# 🚀 AutoInfraOps

**Your AI-powered DevOps sidekick** — scans GitHub repos, spots issues, suggests improvements, and keeps your infra in shape.

---

## 📌 Overview

AutoInfraOps is a **self-updating DevOps/Infra Agent** that automatically:

* Analyzes any GitHub repository you point it to
* Uses **LLMs** to suggest improvements & optimizations
* Flags **outdated dependencies** and potential **security risks**
* Detects **CI/CD misconfigurations** before they break your pipeline
* Creates **GitHub issues** with actionable fixes

It’s like having a tireless DevOps teammate who reviews your repo 24/7.

---

## ✨ Features

* **🔍 Smart Repo Analysis** — Reads your codebase, finds bottlenecks, suggests fixes
* **🤖 LLM-Powered Insights** — Context-aware improvement suggestions
* **📦 Dependency Checks** — Flags outdated or vulnerable packages
* **⚙️ CI/CD Validation** — Scans workflows for misconfigurations
* **📋 Auto GitHub Issues** — Creates ready-to-implement fixes

---

## 🛠️ Tech Stack

* **Python** — Core logic & scripting
* **LangChain** — LLM integration
* **GitHub API** — Repo metadata, file fetch, and issue creation
* **Streamlit** — Interactive dashboard
* **Groq/OpenRouter** — Fast LLM responses

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Tanush-banchhod/AutoInfraOps.git
cd AutoInfraOps

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your keys
GITHUB_TOKEN=your_github_token
GROQ_API_KEY=your_groq_api_key
```

---

## 🚀 Usage

```bash
# Run the Streamlit dashboard
streamlit run frontend/dashboard.py
```

1. Enter the **GitHub repo URL**
2. Click **Analyze Repo**
3. Review AI-generated suggestions
4. (Optional) Auto-create GitHub issues for fixes

---

## 📌 Roadmap

**v1 (Current)**
✅ LLM-based repo scanning
✅ CI/CD & dependency checks
✅ GitHub issue creation

**v2 (Planned)**
🔹 BrowserStack integration to test PRs across OS & browsers before merging
🔹 Auto PR review & merge (if tests pass)
🔹 Slack/Jira integration for alerts

---

## 🤝 Contributing

Have ideas for **v2** or found a bug?
Fork the repo, create a branch, and submit a PR — or just open an issue.

💡 *Let’s make AutoInfraOps smarter together.*

---

## 📜 License

MIT License — free to use and modify.

---

