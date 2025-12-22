import streamlit as st
from database.auth_db import create_user, authenticate_user

def login_ui():
    st.subheader("🔐 Login to LegalEase AI")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

def register_ui():
    st.subheader("📝 Register New Account")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):
        if create_user(username, password):
            st.success("Account created. Please login.")
        else:
            st.error("Username already exists")
