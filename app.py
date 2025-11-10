import gradio as gr
import subprocess
import os
import tempfile
import shutil
import time


def separate_vocals(input_audio):
    start_time = time.time()
    output_dir = tempfile.mkdtemp()

    try:
        # Run Demucs on the uploaded audio
        cmd = ["demucs", "-n", "htdemucs", input_audio, "-o", output_dir]
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Locate output folder
        song_name = os.path.splitext(os.path.basename(input_audio))[0]
        song_folder = os.path.join(output_dir, "htdemucs", song_name)

        vocals = os.path.join(song_folder, "vocals.wav")
        instrumental = os.path.join(song_folder, "drums.wav")
        bass = os.path.join(song_folder, "bass.wav")
        other = os.path.join(song_folder, "other.wav")

        elapsed = time.time() - start_time
        print(f"✅ Separation complete in {elapsed:.2f}s")

        return vocals, instrumental, bass, other, f"✅ Done! Time: {elapsed:.2f}s"

    except subprocess.CalledProcessError as e:
        return None, None, None, None, f"❌ Error: {e.stderr}"


# Gradio UI
ui = gr.Interface(
    fn=separate_vocals,
    inputs=gr.Audio(label="🎵 Upload your song (MP3/WAV)", type="filepath"),
    outputs=[
        gr.Audio(label="🎤 Vocals"),
        gr.Audio(label="🥁 Drums"),
        gr.Audio(label="🎸 Bass"),
        gr.Audio(label="🎶 Other (instruments)"),
        gr.Textbox(label="Status")
    ],
    title="🎧 AI Vocal & Music Separator (Demucs)",
    description="Upload a song and extract vocals, drums, bass, and other instruments using Meta’s Demucs model. Works offline on your Mac M3!",
    allow_flagging="never",
    theme="soft"
)

if __name__ == "__main__":
    ui.launch()
