import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os

def choose_video_file():
    video_file = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
    video_file_entry.delete(0, tk.END)
    video_file_entry.insert(0, video_file)

def choose_audio_file():
    audio_file = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
    audio_file_entry.delete(0, tk.END)
    audio_file_entry.insert(0, audio_file)

def merge_files():
    video_file = video_file_entry.get()
    audio_file = audio_file_entry.get()
    output_file_name = output_file_entry.get() + ".mp4"

    # Extract directory path of the input video file
    output_dir = os.path.dirname(video_file)

    # Construct the path of the output video file
    output_file = os.path.join(output_dir, output_file_name)

    # Update status label
    status_label.config(text="Merging...")

    try:
        # Get the duration of the audio file
        audio_duration_cmd = ['ffprobe', '-i', audio_file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
        audio_duration = subprocess.check_output(audio_duration_cmd)
        audio_duration = float(audio_duration.decode('utf-8').strip())

        # Get the duration of the video file
        video_duration_cmd = ['ffprobe', '-i', video_file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
        video_duration = subprocess.check_output(video_duration_cmd)
        video_duration = float(video_duration.decode('utf-8').strip())

        # Calculate the ratio of audio duration to video duration
        ratio = audio_duration / video_duration

        # Merge the video and audio files
        merge_cmd = [
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-filter_complex', f'[0:v]minterpolate=fps=30,setpts={ratio}*PTS,scale=512:512,setsar=1[v];[1:a]anull[a]',
            '-map', '[v]',
            '-map', '[a]',
            '-r', '30',
            '-c:v', 'libx264',
            '-crf', '18',
            '-c:a', 'aac',
            '-b:a', '128k',
            output_file
        ]
        subprocess.run(merge_cmd)

        # Update status label
        status_label.config(text="Merge successful")

        # Show success message box
        messagebox.showinfo("Success", "Merge successful. Output saved to:\n" + output_file)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during merging: {e}")
        # Update status label
        status_label.config(text="Error during merging")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Update status label
        status_label.config(text="Unexpected error")


# Create the main window
root = tk.Tk()
root.title("VidBork")

# Label for Video File
video_file_label = tk.Label(root, text="Video File:")
video_file_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

# Entry for Video File
video_file_entry = tk.Entry(root, width=40)
video_file_entry.grid(row=0, column=1, padx=5, pady=5)

# Button for choosing Video File
video_file_button = tk.Button(root, text="Choose Video File", command=choose_video_file)
video_file_button.grid(row=0, column=2, padx=5, pady=5)

# Label for Audio File
audio_file_label = tk.Label(root, text="Audio File:")
audio_file_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

# Entry for Audio File
audio_file_entry = tk.Entry(root, width=40)
audio_file_entry.grid(row=1, column=1, padx=5, pady=5)

# Button for choosing Audio File
audio_file_button = tk.Button(root, text="Choose Audio File", command=choose_audio_file)
audio_file_button.grid(row=1, column=2, padx=5, pady=5)

# Label for Output File
output_file_label = tk.Label(root, text="Output File Name:")
output_file_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Entry for Output File
output_file_entry = tk.Entry(root, width=40)
output_file_entry.grid(row=2, column=1, padx=5, pady=5)

# Label for Output File Format
output_file_label = tk.Label(root, text=".mp4")
output_file_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")

# Button for merging
merge_button = tk.Button(root, text="Merge", command=merge_files)
merge_button.grid(row=4, column=1, padx=5, pady=5)

# Label for indicating status
status_label = tk.Label(root, text="", fg="white")
status_label.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()
