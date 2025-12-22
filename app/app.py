import streamlit as st

from services.clause_splitter import split_into_clauses
from services.rule_engine import analyze_clause_with_rules
from services.llm_analyzer import analyze_clause_with_llm
from services.report_generator import generate_pdf_report

# --------------------------------------------------
# Streamlit Page Config
# --------------------------------------------------
st.set_page_config(page_title="LegalEase AI", layout="wide")

st.title("LegalEase AI")
st.write("Automated Legal Text Simplification & Risk Detection")

st.info(
    "Disclaimer: This tool provides automated analysis for educational purposes "
    "and does not constitute legal advice."
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None

# --------------------------------------------------
# User Input
# --------------------------------------------------
user_text = st.text_area(
    "Paste legal text here",
    height=220,
    placeholder="Paste terms & conditions, contract clauses, or policy text here..."
)

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------
if st.button("Analyze"):
    clauses = split_into_clauses(user_text)
    results = []

    for i, clause in enumerate(clauses, 1):
        analysis = analyze_clause_with_rules(clause)

        record = {
            "clause": clause,
            "risk_level": analysis["risk_level"],
            "plain_english": "",
            "risk_justification": "",
            "safer_wording": ""
        }

        st.markdown(f"### Clause {i}")
        st.write(clause)
        st.write(f"**Risk Level:** {analysis['risk_level']}")

        if analysis["risk_level"] != "Low":
            llm_result = analyze_clause_with_llm(
                clause,
                analysis["risk_level"],
                analysis["categories"]
            )

            record.update(llm_result)

            st.write("**Plain English Explanation**")
            st.write(record["plain_english"])

            st.write("**Risk Justification**")
            st.write(record["risk_justification"])

            st.write("**Suggested Safer Wording**")
            st.write(record["safer_wording"])

        results.append(record)
        st.divider()

    # Persist results across reruns
    st.session_state.results = results

# --------------------------------------------------
# PDF Download Section (OUTSIDE Analyze button)
# --------------------------------------------------
if st.session_state.results:
    st.success("Analysis complete. You can now download the PDF report.")

    output_file = "legalease_report.pdf"
    generate_pdf_report(st.session_state.results, output_file)

    with open(output_file, "rb") as f:
        st.download_button(
            label="Download PDF Report",
            data=f,
            file_name="legalease_report.pdf",
            mime="application/pdf"
        )
