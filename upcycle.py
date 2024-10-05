import streamlit as st
import bedrock

def upcycle():
    st.title("Upcycling Ideas")
    
    form = st.form(key="my_form")
    # Input from user
    item = form.text_input("Enter an item to upcycle:")
    submit_button = form.form_submit_button("Search")

    # When the form is submitted, process the topic with Amazon Bedrock
    if submit_button and item:
        prompt = "How can I upcycle a" + item
        temperature = 1.0
        max_tokens = 200

        result = bedrock.invoke(prompt, temperature, max_tokens)
    
        print("Response from Chat:", result)
