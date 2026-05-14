import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

  # --- UI Configuration ---
st.set_page_config(page_title="AI Video Deep Analyzer", page_icon="🎥", layout="wide")

st.title("🎥 AI Video Deep Analyzer & Prompt Generator")
st.markdown("""
  Is app mein aap koi bhi video upload karein, AI use deeply analyze karega aur aapko:
  1. **Detailed Description** dega.
  2. **AI Video/Image Prompts** generate karke dega.
  """)

  # --- Sidebar ---
with st.sidebar:
      st.header("Settings")
      api_key = st.text_input("Enter Google Gemini API Key:", type="password")
      st.info("Get your free key from [Google AI Studio](https://aistudio.google.com/)")

  # --- AI Logic ---
def find_best_model(api_key):
      """Automatically finds the best available vision model for the given API key."""
      try:
          genai.configure(api_key=api_key)
          models = genai.list_models()

          # Priority list of models to look for
          priority = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro-vision"]

          for p in priority:
              for m in models:
                  if p in m.name:
                      return m.name # Returns the full name like 'models/gemini-1.5-flash'

          # If none of the priority models are found, just return the first one that supports
          generateContent
          for m in models:
              if 'generateContent' in m.supported_generation_methods:
                  return m.name

          return None
      except Exception as e:
          st.error(f"Model search error: {e}")
          return None

def analyze_video(video_path, user_api_key):
      try:
          genai.configure(api_key=user_api_key)

          # STEP 1: Smart Model Selection
          model_name = find_best_model(user_api_key)
          if not model_name:
              return "Error: No compatible AI models found for this API key."

          st.caption(f"Using model: {model_name}")
          model = genai.GenerativeModel(model_name=model_name)

          # STEP 2: Upload and Process
          st.info("Uploading video to AI server... please wait.")
          video_file = genai.upload_file(path=video_path)

          while video_file.state.name == "PROCESSING":
              time.sleep(2)
              video_file = genai.get_file(video_file.name)

          if video_file.state.name == "FAILED":
              raise Exception("Video processing failed.")

          # STEP 3: Analysis
          prompt = """
          Please analyze this video deeply. Provide the following:
          1. **Deep Visual Description**: Describe everything happening in the video.
          2. **Temporal Analysis**: Explain how the scenes transition.
          3. **AI Generation Prompts**: Generate 3 high-quality prompts for Sora or Runway.
          Format the output clearly with headings.
          """

          response = model.generate_content([prompt, video_file])
          genai.delete_file(video_file.name)
          return response.text

      except Exception as e:
          return f"Error: {str(e)}"

  # --- Main Interface ---
uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
      ext = os.path.splitext(uploaded_file.name)[1]
      with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
          tmp.write(uploaded_file.read())
          tmp_path = tmp.name

      st.video(uploaded_file)

      if st.button("🚀 Analyze Video"):
          if not api_key:
              st.error("Please enter your API Key in the sidebar first!")
          else:
              with st.spinner("Smart-searching for best model and analyzing..."):
                  result = analyze_video(tmp_path, api_key)
                  st.success("Analysis Complete!")
                  st.markdown("---")
                  st.markdown(result)

      os.remove(tmp_path)
