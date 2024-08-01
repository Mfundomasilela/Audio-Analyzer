import streamlit as st
import openai

# Directly set the API key
api_key = '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'
openai.api_key = api_key

MODEL = 'gpt-4'

st.title('AI AUDIO ANALYZER')

# Upload audio file
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if audio_file:
    # Display audio player
    st.audio(audio_file)

    # Convert audio file to bytes
    audio_bytes = audio_file.read()

    # Transcribe audio
    try:
        transcription_response = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_bytes,
        )
        transcription_text = transcription_response['text']

        # Analyze transcription
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an audio analyzer AI. Analyze the audio and create a summary of the provided transcription. Respond in Markdown."},
                {"role": "user", "content": f"The audio transcription is: {transcription_text}"}
            ],
            temperature=0,
        )

        # Display the response
        st.markdown(response['choices'][0]['message']['content'])

    except Exception as e:
        st.error(f"An error occurred: {e}")
