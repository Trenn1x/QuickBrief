import streamlit as st
from core.summarizer   import synthesize
from core.notion_push  import push as push_notion
from core.trello_push  import push as push_trello   # keep even if creds not set yet

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="QuickBrief", page_icon="📝")
st.title("QuickBrief 📝")

# 1️⃣  Discovery-call notes
notes = st.text_area("Paste discovery-call notes")

# 2️⃣  Generate the brief
if st.button("Generate Brief") and notes.strip():
    st.session_state["brief_md"] = synthesize(notes)

# 3️⃣  Preview + downloads (only after a brief exists)
if "brief_md" in st.session_state:
    md = st.session_state["brief_md"]

    st.markdown(md, unsafe_allow_html=False)

    st.download_button(
        label="Download Markdown",
        data=md.encode(),
        file_name="brief.md",
        mime="text/markdown",
    )

    # 4️⃣  Push to Notion & Trello
    if st.button("Send to Notion & Trello"):
        push_notion(md)
        card_url = push_trello(md)
        st.success(
            f"Pushed to **Notion** *and* **Trello!**  \n"
            f"[Open Trello card]({card_url})"
        )
