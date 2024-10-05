import bedrock
import streamlit as st
import boto3
from botocore.exceptions import ClientError

form = st.form(key='my_form')
topic = form.text_input(label='Item')

# Submit button for the form
submit_button = form.form_submit_button(label='Submit')

# When the form is submitted, process the topic with Amazon Bedrock
if submit_button and topic:
    prompt = "How can I upcycle an" + topic
    temperature = 1.0
    max_tokens = 200

    result = bedrock.invoke(prompt, temperature, max_tokens)
    
    st.text(result)
    print("Response from Chat:", result)


