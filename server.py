from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess
import os
import tempfile
import shutil

app = FastAPI()

# ✅ Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/separate")
async def separate_audio(file: UploadFile = File(...)):
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, file.filename)

    # Save the uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_dir = os.path.join(temp_dir, "output")
    cmd = ["demucs", "-n", "htdemucs", input_path, "-o", output_dir]
    subprocess.run(cmd, check=True)

    song_name = os.path.splitext(file.filename)[0]
    song_dir = os.path.join(output_dir, "htdemucs", song_name)

    # Collect file paths
    files = {
        "vocals": os.path.join(song_dir, "vocals.wav"),
        "drums": os.path.join(song_dir, "drums.wav"),
        "bass": os.path.join(song_dir, "bass.wav"),
        "other": os.path.join(song_dir, "other.wav"),
    }

    # Copy all WAVs to a static public folder for access
    public_dir = "static_outputs"
    os.makedirs(public_dir, exist_ok=True)
    result_urls = {}
    for stem, path in files.items():
        if os.path.exists(path):
            new_path = os.path.join(public_dir, f"{song_name}_{stem}.wav")
            shutil.copy(path, new_path)
            result_urls[stem] = f"http://127.0.0.1:8000/{new_path}"

    return JSONResponse(content={"files": result_urls, "message": "Separation complete ✅"})

# Serve files from static_outputs/
app.mount("/static_outputs",
          StaticFiles(directory="static_outputs"), name="static")


@app.get("/")
def root():
    return {"message": "Demucs backend running!"}
