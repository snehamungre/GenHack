import streamlit as st
import bedrock
from PIL import Image
import base64
from io import BytesIO
import re  # Import the regex module

def encode_image_to_base64(image):
    """Encodes a PIL image to a Base64 string."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def display_upcycling_ideas(ideas):
    """Displays upcycling ideas, with each idea in a clickable box."""
    for idea in ideas:
        idea_text, tutorial_link = idea.get('text'), idea.get('link')
        st.markdown(
            f"""
            <div class="idea-box">
                <p>{idea_text}</p>
                <a href="{tutorial_link}" target="_blank">Go to tutorial</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

def parse_response_to_ideas(response_text):
    """Extracts and structures ideas and links from the response."""
    ideas = []
    
    # Regular expression to capture ideas that start with a number followed by a period (e.g., "1. ", "2. ")
    idea_blocks = re.split(r'\d+\.\s+', response_text)
    
    # Iterate through the extracted blocks, skip the first split as it's empty
    for block in idea_blocks[1:]:
        # Split the block to find the link and the main idea text
        lines = block.strip().split("\n")
        idea_text = lines[0].strip()  # First line is the idea text
        tutorial_link = ""
        
        # Try to find the line that contains the tutorial link (assuming 'http' is in the link)
        for line in lines:
            if "http" in line:
                tutorial_link = line.strip()
                break
        
        if idea_text and tutorial_link:
            ideas.append({"text": idea_text, "link": tutorial_link})
    
    return ideas

def upcycle():
    st.title("Upcycling Ideas")
    
    form = st.form(key="my_form")
    item = form.text_input("Enter an item to upcycle:")
    uploaded_image = form.file_uploader("Upload an image of the item you want to upcycle", type=["jpg", "jpeg", "png"])
    submit_button = form.form_submit_button("Search")

    if submit_button and item:
        prompt = f"How can I upcycle this item? For each idea, give me how long it will take. Please give me links to tutorials as well: {item}"
        temperature = 1.0
        max_tokens = 200

        result = bedrock.invoke(prompt, temperature, max_tokens)
        st.success("Here are some upcycling ideas based on your input!")
        st.write(result)

        # Parse and display ideas
        # ideas = parse_response_to_ideas(result)
        # display_upcycling_ideas(ideas)

    elif submit_button and uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        base64_image = encode_image_to_base64(image)
        result = bedrock.invokewithImage("How can I upcycle this item? For each idea, give me how long it will take. Please give me links to tutorials as well:", image_base64=base64_image)

        st.success("Here are some upcycling ideas based on your image!")
        st.text(result)
        # Parse and display ideas
        # ideas = parse_response_to_ideas(result)
        # display_upcycling_ideas(ideas)