import streamlit as st

st.set_page_config(page_title="Codebase Whisperer", page_icon="🔎", layout="wide")
st.title("Codebase Whisperer")
st.caption("Understand a repository with answers grounded in its indexed evidence.")

with st.sidebar:
    st.subheader("Workspace")
    st.info("No repository indexed yet.")
    st.selectbox("Guide language", ["English"], disabled=True)
    st.caption("Repository indexing is the next implementation milestone.")

tabs = st.tabs(["Chat", "Onboarding", "Changes", "Pending Actions", "Eval"])
with tabs[0]:
    st.subheader("Ask about a repository")
    st.text_input("Question", placeholder="Where is request routing handled?", disabled=True)
    st.caption("Cited Q&A becomes available after ingestion and retrieval are connected.")
for tab, title, description in zip(
    tabs[1:],
    ["Onboarding guide", "Repository changes", "Human review queue", "Retrieval evaluation"],
    ["Personalised, evidence-cited guides will appear here.",
     "Incremental change summaries are a stretch goal.",
     "Proposed GitHub actions will require explicit approval here.",
     "Recall, ranking, citation, and not-found metrics will appear here."],
):
    with tab:
        st.subheader(title)
        st.info(description)
