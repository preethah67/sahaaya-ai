import asyncio
import os
import edge_tts

# Microsoft Edge TTS Voices:
# Tamil: ta-IN-PallaviNeural
# English/Tanglish: en-IN-NeerjaNeural or en-IN-PrabhatNeural
TAMIL_VOICE = "ta-IN-PallaviNeural"
ENGLISH_VOICE = "en-IN-NeerjaNeural"

async def generate_speech_async(text, output_path, lang="ta"):
    """
    Generates MP3 audio from text using Microsoft Edge TTS.
    """
    voice = TAMIL_VOICE if lang == "ta" else ENGLISH_VOICE
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def text_to_speech(text, output_filename="output.mp3", lang="ta"):
    """
    Synchronous wrapper for Flask app usage.
    """
    output_dir = os.path.join("static", "audio")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Run async function in sync environment
    asyncio.run(generate_speech_async(text, output_path, lang))
    return output_path

if __name__ == "__main__":
    sample_text = "வணக்கம்! சகாயா ஏஐ உங்களை வரவேற்கிறது."
    audio_file = text_to_speech(sample_text, "test_tamil.mp3", lang="ta")
    print(f"Audio generated successfully at: {audio_file}")