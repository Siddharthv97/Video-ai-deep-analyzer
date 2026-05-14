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
  2. **AI Video/Image Prompts** generate karke dega taaki aap waisa hi content create kar sakein.
  """)

  # --- Sidebar for API Key & Model Selection ---
  with st.sidebar:
      st.header("Settings")
      api_key = st.text_input("Enter Google Gemini API Key:", type="password")
      st.info("Get your free key from [Google AI Studio](https://aistudio.google.com/)")

      st.markdown("---")
      st.subheader("Model Selection")
      selected_model = st.selectbox(
          "Choose AI Model:",
          options=["gemini-1.5-pro", "gemini-1.5-flash"],
          index=0,
          help="Pro is better for deep analysis; Flash is faster and more stable."
      )

  # --- AI Logic ---
  def analyze_video(video_path, user_api_key, model_name):
      try:
          genai.configure(api_key=user_api_key)
          model = genai.GenerativeModel(model_name=model_name)

          st.info("Uploading video to AI server... please wait.")
          video_file = genai.upload_file(path=video_path)

          while video_file.state.name == "PROCESSING":
              time.sleep(2)
              video_file = genai.get_file(video_file.name)

          if video_file.state.name == "FAILED":
              raise Exception("Video processing failed.")

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
              with st.spinner("AI is watching and analyzing..."):
                  result = analyze_video(tmp_path, api_key, selected_model)
                  st.success("Analysis Complete!")
                  st.markdown("---")
                  st.markdown(result)

      os.remove(tmp_path)
