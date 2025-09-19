import streamlit as st
from gtts import gTTS
from moviepy.editor import *
import os

st.title("Filipino Text-to-Video Generator")

text_input = st.text_area("Enter your text in Filipino:")

background_choice = st.selectbox("Choose background type:",
                                ["Solid Color", "Image"])

if background_choice == "Image":
    uploaded_bg = st.file_uploader("Upload Background Image", type=["jpg", "png"])

if st.button("Generate Video"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Convert text to speech
        tts = gTTS(text=text_input, lang='tl')
        tts.save("audio.mp3")

        # Load audio
        audio_clip = AudioFileClip("audio.mp3")

        # Create video background
        if background_choice == "Solid Color":
            video_clip = ColorClip(size=(1280,720), color=(0, 0, 0), duration=audio_clip.duration)
        else:
            if uploaded_bg is not None:
                with open("bg.png","wb") as f:
                    f.write(uploaded_bg.getbuffer())
                bg_img = ImageClip("bg.png").set_duration(audio_clip.duration).resize((1280,720))
                video_clip = bg_img
            else:
                st.error("Please upload a background image.")
                st.stop()

        # Combine audio with video
        final_clip = video_clip.set_audio(audio_clip)

        # Export
        final_clip.write_videofile("output.mp4", fps=24)

        st.success("Video generated successfully!")
        with open("output.mp4", "rb") as file:
            st.download_button("Download Video", file, "filipino_video.mp4")
