import streamlit as st
from agno.media import Image
from agent import create_agent
from utils import save_uploaded_file, delete_file


st.set_page_config(
    page_title="MultiModal AI Agent",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MultiModal AI Agent")
st.write("Upload an image and asl AI agent anything about it")

#sidebar
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Enter your Anthropic API Key", type="password")
    st.caption("Get your key from https://console.anthropic.com")
    
#main
# ── Main ─────────────────────────────────────────────────
if not api_key:
    st.warning("Please enter your Anthropic API key in the sidebar to continue.")
    st.stop()
    
#create the agent once so it doesn't rebuild on every click
@st.cache_resource
def get_agent(key:str):
    return create_agent(api_key=key)
agent = get_agent(api_key)

# file uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # show the image to the user
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    # text input for the user's question
    question = st.text_area("What do you want to know about this image?")

    if st.button("Analyze") and question:
        # save uploaded file to disk so the agent can read it
        temp_path = save_uploaded_file(uploaded_file, suffix=".jpg")

        try:
            with st.spinner("Agent is thinking... 🤖"):
                response = agent.run(question, images=[Image(filepath=temp_path)])

            st.markdown("### Response")
            st.markdown(response.content)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

        finally:
            # always delete the temp file whether it worked or not
            delete_file(temp_path)