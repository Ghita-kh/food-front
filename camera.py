import streamlit as st
from PIL import Image

import streamlit as st
import requests
from PIL import Image
import io
import base64
from time import sleep

import streamlit as st
import base64
from time import sleep
from PIL import Image
import io

original_title = '<h1 style="font-family: Cursive; position: fixed; top: 40px; left: 950px; color: #A23138; font-size: 3rem; margin: 0;">Food Recognition </h1>'
st.markdown(original_title, unsafe_allow_html=True)


background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1612198791461-e26e3b5dcb86?q=80&w=1888&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def get_prediction(image_bytes):
    # Define the correct API endpoint URL
    url = "https://nfg-repo-rmhuz6i5bq-ew.a.run.app/predict"
    # Create an in-memory file-like object
    files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}

    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            # Assuming the server responds with JSON
            return response.json()
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"



# Streamlit application setup
st.write("Upload an image of a plate, and we'll recognize the food placed in it.")

# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])

# if uploaded_file:
#     # Display the uploaded image
#     image = Image.open(io.BytesIO(uploaded_file.getvalue()))
#     st.image(image, caption="Uploaded Image", use_column_width=True)

#     # Convert the uploaded file to bytes for the request
#     img_bytes = uploaded_file.getvalue()
#     prediction = get_prediction(img_bytes)

#     # Display the prediction result
#     st.write(f"Prediction: {prediction['class']}")
#     # st.audio(f"./audios/{prediction['class']}.mp3",autoplay=True)

picture = st.camera_input("Take a picture")

if picture:
    image = Image.open(io.BytesIO(picture.getvalue()))
    st.image(image, caption="Captured Image", use_column_width=True)

    # Convert the uploaded file to bytes for the request
    img_bytes = picture.getvalue()
    prediction = get_prediction(img_bytes)

    # Display the prediction result
    st.write(f"Prediction: {prediction['class']}")
    # st.audio(f"./audios/{prediction['class']}.mp3",autoplay=True)

    st.write("# Auto-playing Audio!")
    sleep(1)
    autoplay_audio(f"./audios/{prediction['class']}.mp3")
