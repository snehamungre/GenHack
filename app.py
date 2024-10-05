import streamlit as st
from upcycle import upcycle
from shop import shop

# Create a sidebar for navigation
st.sidebar.title("ReMakeIt! 🌱")
# st.sidebar.image("logo.png")  
page = st.sidebar.selectbox("Your go-to Recycling and Upcycling Hub!", ("Upcycling Ideas ✨", "Sustainable Purchases 🛍️"))

# Render the selected page
if page == "Upcycling Ideas ✨":
    upcycle()
elif page == "Sustainable Purchases 🛍️":
    shop()
