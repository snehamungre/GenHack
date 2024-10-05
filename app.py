import bedrock
import streamlit as st
import boto3
from botocore.exceptions import ClientError

import streamlit as st


# app.py
import streamlit as st
from upcycle import upcycle
from shop import shop

# Create a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", ("Upcycling Ideas", "Sustainable Purchases"))

# Render the selected page
if page == "Upcycling Ideas":
    upcycle()
elif page == "Sustainable Purchases":
    shop()
