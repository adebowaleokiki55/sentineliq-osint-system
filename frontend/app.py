import streamlit as st
import requests

st.title("🧠 OSINT Intelligence Dashboard")

claim = st.text_input("Enter claim")

if st.button("Verify"):

    try:
        res = requests.get(
            "http://localhost:8000/verify",
            params={"claim": claim}
        )

        if res.status_code != 200:
            st.error("Backend Error")
            st.write(res.text)
            st.stop()

        data = res.json()

    except Exception as e:
        st.error(f"Connection error: {e}")
        st.stop()

    # -------------------
    # CORE OUTPUT
    # -------------------
    st.metric("Score", round(data["score"], 2))
    st.subheader(data["verdict"])
    st.write("Confidence:", data["confidence_level"])

    st.divider()

    # -------------------
    # SUMMARY
    # -------------------
    st.subheader("🧠 Intelligence Summary")
    st.write(data["summary"])

    st.divider()

    # -------------------
    # FINDINGS
    # -------------------
    st.subheader("📌 Key Findings")

    findings = data.get("key_findings", {})

    st.write("Sources analyzed:", findings.get("sources_analyzed", 0))
    st.write("Contradictions:", findings.get("contradictions", []))

    st.divider()

    # -------------------
    # EVIDENCE
    # -------------------
    st.subheader("📄 Evidence")

    for ev in findings.get("top_evidence", []):

        st.markdown(f"""
**{ev.get('title','')}**

- Strength: `{ev.get('strength','')}`
- Source: {ev.get('url','')}
""")

        st.divider()

    # -------------------
    # CLEAN ANALYST NOTE (IMPROVED)
    # -------------------
    st.subheader("🧾 Analyst Note")

    st.info(
        "Assessment based on semantic similarity between claim and retrieved news sources, "
        "weighted by publisher credibility. This system does not perform real-world verification, "
        "only evidence correlation and consistency scoring."
    )