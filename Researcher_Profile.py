# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:35:42 2025

@author: jerem
"""

import streamlit as st
import pandas as pd

# Title of the app
st.title("Jeremy Burgess Profile Page")

# Collect basic information
name = "Mr Jeremy Gareth Burgess"
field = "Biochemistry / Bioinformatics"
institution = "University of the Western Cape"
department = "SANBI"
email = "3135134@myuwc.ac.za"

# Display basic profile information

col1, col2 = st.columns(2)

col1.subheader("Researcher Overview")
col1.write(f"**Name:** {name}")
col1.write(f"**Field of Research:** {field}")
col1.write(f"**Institution:** {institution}")
col1.write(f"**Department:** {department}")

col2.image(f"JemPic2.jpg", width=200)

st.subheader("Contact Information")
#email = "jane.doe@example.com"
st.write(f"You can reach {name} at {email}.")