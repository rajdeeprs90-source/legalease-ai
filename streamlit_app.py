# ==================================================
# Python Path Fix (MUST BE FIRST)
# ==================================================
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# ==================================================
# Imports
# ==================================================
import streamlit as st

from services.clause_splitter import split_into_clauses
from services.rule_engine import analyze_clause_with_rules
from services.llm_analyzer import analyze_clause_with_llm
from services.report_generator import generate_pdf_report

from database.auth_db import init_db
from app.auth import login_ui, register_ui

# ==================================================
# Streamlit Page Config
# ==================================================
st.set_page_config(
    page_title="LegalEase AI",
    layout="wide",
)

# ==================================================
# Initialize Database
# ==================================================
init_db()

# ==================================================
# Session State Initialization
# ==================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "results" not in st.session_state:
    st.session_state.results = None

if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False

# ==================================================
# PUBLIC AREA — LOGIN / REGISTER
# ==================================================
if not st.session_state.authenticated:
    st.title("LegalEase AI")
    st.write("Automated Legal Text Simplification & Risk Detection")

    st.info(
        "Disclaimer: This tool provides automated analysis for educational purposes "
        "and does not constitute legal advice."
    )

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        login_ui()

    with tab2:
        register_ui()

    st.stop()

# ==================================================
# PROTECTED AREA — MAIN APP
# ==================================================
st.sidebar.success(f"Logged in as {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.title("LegalEase AI — Document Analysis")

# ==================================================
# User Input
# ==================================================
user_text = st.text_area(
    "Paste legal text here",
    height=220,
    placeholder="Paste terms & conditions, contract clauses, or policy text here..."
)

# ==================================================
# Analyze Button
# ==================================================
if st.button("Analyze"):
    if not user_text.strip():
        st.warning("Please paste some legal text before analyzing.")
    else:
        clauses = split_into_clauses(user_text)

        if not clauses:
            st.warning("No valid clauses were detected in the provided text.")
        else:
            results = []

            for i, clause in enumerate(clauses, start=1):
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

            st.session_state.results = results
            st.session_state.pdf_ready = False

# ==================================================
# PDF Download Section
# ==================================================
if st.session_state.results:
    st.success("Analysis complete.")

    if not st.session_state.pdf_ready:
        generate_pdf_report(st.session_state.results, "legalease_report.pdf")
        st.session_state.pdf_ready = True

    with open("legalease_report.pdf", "rb") as f:
        st.download_button(
            label="Download PDF Report",
            data=f,
            file_name="legalease_report.pdf",
            mime="application/pdf"
        )
