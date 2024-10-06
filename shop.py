import streamlit as st
import bedrock

def shop():
    st.title("Sustainable Shopping")
    
    form = st.form(key="my_form")
    # Input from user
    item = form.text_input("Enter an item to Buy:")
    material = form.text_input("With material:")
    budget = form.number_input("What is your burdget:")
    location = form.text_input("What location do you prefer")
    eco_friendly = form.checkbox("Do you want to see eco-friendly brands?")
    submit_button = form.form_submit_button("Search")

    # When the form is submitted, process the topic with Amazon Bedrock
    if submit_button and item:
        prompt = f"How can I sustainably buy a {item} with a budget of {budget} made out of {material} near {location}? Give me specific product data"
        prompt += " Also, suggest eco-friendly brands." 

        temperature = 1.0
        max_tokens = 200

        # Invoke Bedrock and handle potential exceptions
        try:
            result = bedrock.invoke(prompt, temperature, max_tokens)
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            
        print("Response from Chat:", result)

