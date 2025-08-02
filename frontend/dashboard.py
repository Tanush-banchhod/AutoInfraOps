import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.repo_agent import analyze_repo



st.set_page_config(page_title="AutoInfraOps", layout="wide")

st.title("🚀 AutoInfraOps Dashboard")
st.markdown("AI-powered DevOps agent that analyzes repos and suggests infra improvements.")

repo_url = st.text_input("Enter GitHub Repo URL", "https://github.com/Tanush-banchhod/AutoInfraOps")

if st.button("Analyze"):
    with st.spinner("Running analysis..."):
        results = analyze_repo(repo_url)

    st.success("Analysis complete!")

    st.subheader("⚙️ Static Warnings")
    for filetype, warnings in results["static_warnings"].items():
        st.markdown(f"### {filetype}")
        for w in warnings:
            st.warning(w)

    st.subheader("🧠 LLM Suggestions")
    for filetype, suggestion in results["llm_suggestions"].items():
        st.markdown(f"### {filetype}")
        st.code(suggestion, language="markdown")

    st.subheader("📌 GitHub Issues Created")
    created = results.get("created_issues", [])
    if created:
        for issue in created:
            st.markdown(f"- [{issue['title']}]({issue['url']})")
    else:
        st.write("No issues were created.")

