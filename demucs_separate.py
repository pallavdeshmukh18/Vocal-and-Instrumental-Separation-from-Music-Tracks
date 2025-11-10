import os
import subprocess
import time


def separate_vocals(input_song):
    print("🎧 Starting vocal separation with Demucs...")
    start_time = time.time()

    # Create output folder
    output_dir = "output_demucs"
    os.makedirs(output_dir, exist_ok=True)

    # Run Demucs command
    cmd = ["demucs", "-n", "htdemucs", input_song, "-o", output_dir]
    subprocess.run(cmd, check=True)

    elapsed = time.time() - start_time
    print(f"\n✅ Done! Time taken: {elapsed:.2f}s")
    print("Check inside:")
    print(
        f"{output_dir}/htdemucs/{os.path.splitext(os.path.basename(input_song))[0]}/")
    print("Files include:")
    print(" • vocals.wav (isolated voice)")
    print(" • drums.wav, bass.wav, other.wav, etc.")


if __name__ == "__main__":
    # Change this to your file name
    separate_vocals("song.mp3")
