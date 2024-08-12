import streamlit as st
import openai
import os
from io import BytesIO

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def meeting_note_taker():
    st.title("Meeting Note Taker")
    st.markdown("### Record your meeting and automatically generate notes")

    # Function to handle audio recording and transcription (simplified for this example)
    def transcribe_audio(audio_file):
        # Example using OpenAI's Whisper or any other ASR service
        with open(audio_file, 'rb') as file:
            transcript = openai.Audio.transcribe("whisper-1", file)  # Simplified example
        return transcript

    # Function to summarize notes using GPT-4
    def summarize_notes(transcript_text):
        prompt = f"""
        Summarize the following meeting transcript into key points, action items, and decisions:
        {transcript_text}
        """
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )
        summary = response.choices[0].text.strip()
        return summary

    # Upload or record an audio file
    audio_file = st.file_uploader("Upload your meeting audio file", type=["mp3", "wav", "m4a"])

    if audio_file:
        st.audio(audio_file)
        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio(audio_file)
            st.text_area("Transcript", value=transcript, height=300)

        with st.spinner("Summarizing notes..."):
            summary = summarize_notes(transcript)
            st.text_area("Summary", value=summary, height=200)

        # Option to download summary
        st.download_button(label="Download Summary", data=summary, file_name="meeting_summary.txt")

    # Provide option to record live audio (Note: This requires additional setup for real-time recording)
    st.markdown("---")
    st.markdown("### Record Live Meeting (Coming Soon)")
