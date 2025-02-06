# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:26:01 2025

@author: jerem
"""

import streamlit as st
import sqlite3
from datetime import datetime
import hashlib  # For password hashing

# Database setup
def init_db():
    conn = sqlite3.connect('user_accounts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            birth_date TEXT,
            instiution TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create a new user
def create_user(first_name, last_name, email, username, password, birth_date, institution, department):
    conn = sqlite3.connect('user_accounts.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('''
        INSERT INTO users (first_name, last_name, email, username, password, birth_date, institution, department)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, email, username, hashed_password, birth_date, institution, department))
    conn.commit()
    conn.close()

# Verify user login
def verify_login(username, password):
    conn = sqlite3.connect('user_accounts.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Initialize the database
init_db()

# Page configuration
st.set_page_config(
    page_title="Account Management",
    page_icon="👤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
    <style>
    .header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.1rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 3rem;
    }
    .stButton button {
        width: 100%;
        background-color: #3498db;
        color: white;
        padding: 0.8rem;
        border-radius: 0.5rem;
        font-size: 1.1rem;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #2980b9;
        color: white;
    }
    .success-message {
        text-align: center;
        padding: 2rem;
        background-color: #ecf8f2;
        border-radius: 0.5rem;
        color: #27ae60;
        margin-top: 2rem;
    }
    .error-message {
        text-align: center;
        padding: 2rem;
        background-color: #f8d7da;
        border-radius: 0.5rem;
        color: #dc3545;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Account creation page
def account_creation_page():
    st.markdown('<p class="header">Create New Account</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Join our community to get started</p>', unsafe_allow_html=True)
    
    with st.form("account_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First name", placeholder="John")
        with col2:
            last_name = st.text_input("Last name", placeholder="Doe")
        
        email = st.text_input("Email address", placeholder="john.doe@example.com")
        username = st.text_input("Choose a username", placeholder="@john_doe")
        password = st.text_input("Create password", type="password", placeholder="••••••••")
        
        birth_date = st.date_input("Date of birth", min_value=datetime(1900, 1, 1))
        institution = st.text_input("Institution", placeholder="University of ?")
        department = st.text_input("Department", placeholder="Biochemistry")
        submitted = st.form_submit_button("Create Account")

    if submitted:
        if not all([first_name, last_name, email, username, password, institution, department]):
            st.error("Please fill in all required fields")
        else:
            try:
                create_user(first_name, last_name, email, username, password, birth_date, institution, department)
                st.markdown("""
                <div class="success-message">
                    <h3>🎉 Account Created Successfully!</h3>
                    <p>Welcome to our community, {}!</p>
                </div>
                """.format(first_name), unsafe_allow_html=True)
            except sqlite3.IntegrityError:
                st.error("Username or email already exists. Please choose a different one.")

# Login page
def login_page():
    st.markdown('<p class="header">Login</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Welcome back! Please log in to continue</p>', unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="@john_doe")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    if st.button("Log In"):
        if verify_login(username, password):
            st.markdown("""
            <div class="success-message">
                <h3>🎉 Login Successful!</h3>
                <p>Welcome back, {}!</p>
            </div>
            """.format(username), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-message">
                <h3>❌ Login Failed</h3>
                <p>Invalid username or password. Please try again.</p>
            </div>
            """, unsafe_allow_html=True)

# Main app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Create Account", "Login"])

    if page == "Create Account":
        account_creation_page()
    elif page == "Login":
        login_page()

if __name__ == "__main__":
    main()
