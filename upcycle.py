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
    """Displays upcycling ideas, with each idea in a styled box."""
    items_per_row = 2  # Change this to 2 for 2 items per row
    num_ideas = len(ideas)

    for i in range(0, num_ideas, items_per_row):  # Step by items_per_row
        # Create columns for the current row
        cols = st.columns(items_per_row)

        for j in range(items_per_row):
            if i + j < num_ideas:  # Check if the idea exists
                idea = ideas[i + j]
                print(idea)
                with cols[j]:  # Use the inner index for columns
                    st.markdown(
                        f"""
                        <div style="border: 2px solid #4CAF50; border-radius: 8px; padding: 15px; margin: 10px 0; background-color: #f9f9f9;">
                            <h4 style="color: #333;">{idea['text']}</h4>
                            <p style="color: #555;">Time: {idea['time']} | 
                            <a href="{idea['link']}" target="_blank" style="color: #4CAF50; text-decoration: none;">Go to tutorial</a></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def parse_response_to_ideas(response_text):
    """Extracts and structures ideas and links from the response."""
    ideas = []
    
    # Regular expression to capture ideas that start with a number followed by a period
    idea_blocks = re.split(r'\d+\.\s+', response_text)
    
    for block in idea_blocks[1:]:
        lines = block.strip().split("\n")
        idea_text = lines[0].strip()
        tutorial_link = ""
        time_estimate = ""  # New variable for time estimate
        
        # Try to find the line that contains the tutorial link and time estimate
        for line in lines:
            if "http" in line:
                tutorial_link = line.strip()
            if "Time:" in line:
                time_estimate = line.strip()  # Extract time estimate
        
        if idea_text and tutorial_link and time_estimate:
            ideas.append({"text": idea_text, "link": tutorial_link, "time": time_estimate})
    
    return ideas

def parse_image_response_to_ideas(response_text):
    ideas = []
    
    # Split the response by line breaks to handle each idea individually
    idea_blocks = response_text.strip().split("\n")
    
    for block in idea_blocks:
        # Use regex to capture the idea details
        match = re.match(r'(\d+)\.\s*([^:]*):\s*([^\.]*\.)\s*(This could take [^\.]*\.)?\s*(Tutorial:\s*(https?://[^\s]+))?', block.strip())
        
        if match:
            # Extracting the captured groups
            idea_text = match.group(2).strip()  # Idea name
            description = match.group(3).strip()  # Description (if any)
            time = match.group(4).strip() if match.group(4) else "No time estimate"  # Time estimate
            tutorial_link = match.group(6).strip() if match.group(6) else "No tutorial"  # Tutorial link
            
            # Constructing the structured idea
            ideas.append({
                "text": f"{idea_text}: {description}",
                "time": time,
                "link": tutorial_link if "http" in tutorial_link else ""
            })
    
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
        ideas = parse_response_to_ideas(result)
        display_upcycling_ideas(ideas)
        

    elif submit_button and uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        prompt = f"How can I upcycle the items in this image? For each idea, give me how long it will take. Give it to me in this format: 1. Idea Name: Time: Time Estimate Description. Tutorial: URL Please give me links to tutorials as well:"
       
        
        base64_image = encode_image_to_base64(image)
        result = bedrock.invokewithImage(prompt,base64_image)

        # display results
        st.success("Here are some upcycling ideas based on your image!")
        # Parse and display ideas
        ideas = parse_image_response_to_ideas(result)
        display_upcycling_ideas(ideas)
