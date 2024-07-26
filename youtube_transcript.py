from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, VERTICAL, END, filedialog, Frame
from youtube_transcript_api import YouTubeTranscriptApi
import re

def slugify(title_text):
    title_text = re.sub(r'[^\w\s]', '', title_text)
    title_text = re.sub(r'\s+', '-', title_text)
    return title_text.lower()

def get_transcript(video_id, with_timestamps=False):
	try:
		transcript = YouTubeTranscriptApi.get_transcript(video_id)
		if with_timestamps:
			return transcript
		else:
			transcript_text = ' '.join([item['text'] for item in transcript])
			return transcript_text
	except Exception as e:
		print(f"Error: {e}")
		return None

def get_video_id(video_url):

	patterns = [
		r"youtube\.com/watch\?v=([^\&\#]+)",  # Standard format with exclusion of '&' and '#' in capture
		r"youtube\.com/watch\?.*v=([^\&\#]+)",  # Format with additional parameters, excluding '&' and '#'
		r"youtube\.com/shorts/([^\?]+)",  # Shorts format, excluding '?'
		r"youtu\.be/([^\?]+)",  # Shortened format, excluding '?'
		r"youtube\.com/embed/([^\?]+)"  # Embed format, excluding '?'
	]

	for pattern in patterns:
		match = re.search(pattern, video_url)
		if match:
			return match.group(1)
	return None


def fetch_and_display_transcript():
	video_url = url_entry.get()
	video_id = get_video_id(video_url)
	transcript_text = get_transcript(video_id)
	transcript_display.delete('1.0', END)
	if transcript_text is not None:
		transcript_display.insert(END, transcript_text)
		download_button.config(state="normal")
		download_full_button.config(state="normal")
	else:
		download_button.config(state="disabled")
		download_full_button.config(state="disabled")


def download_transcript():
	transcript_text = transcript_display.get("1.0", END)
	title_text = slugify(title_entry.get().strip())
	video_url = url_entry.get()
	initial_filename = f"transcript-{title_text}.txt" if title_text else "transcript.txt"

	file_path = filedialog.asksaveasfilename(
		initialfile=initial_filename,
		defaultextension=".txt",
		filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
	)

	if file_path:
		with open(file_path, "w", encoding="utf-8") as file:
			if title_text:
				file.write(f"Title: {title_text}\n")
			file.write(f"URL: {video_url}\n\n")
			file.write(transcript_text)


def download_transcript_with_timestamps():
	title_text = slugify(title_entry.get().strip())
	video_url = url_entry.get()
	initial_filename = f"transcript-timestamps-{title_text}.txt" if title_text else "transcript_w_timestamps.txt"
	video_id = get_video_id(video_url)
	transcript_with_timestamps = get_transcript(video_id, with_timestamps=True)

	title_text = title_entry.get().strip()
	if transcript_with_timestamps is not None:
		file_path = filedialog.asksaveasfilename(
			initialfile=initial_filename,
			defaultextension=".txt",
			filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
		)
		if file_path:
			with open(file_path, "w", encoding="utf-8") as file:
				if title_text:
					file.write(f"Title: {title_text}\n")
				file.write(f"URL: {video_url}\n\n")
				for item in transcript_with_timestamps:
					line = f"[{item['start']}] {item['text']}\n"
					file.write(line)
	else:
		print("Error: No transcript available or an error occurred")

root = Tk()
root.title("YouTube Transcript Fetcher")

input_frame = Frame(root)
input_frame.pack(fill="x", padx=5, pady=5)
url_label = Label(input_frame, text="YouTube Video URL:")
url_label.pack(side="left")
url_entry = Entry(input_frame, width=50)
url_entry.pack(side="left", expand=True, fill="x")

title_label = Label(input_frame, text="Title (optional):")
title_label.pack(side="left", padx=(10,0))
title_entry = Entry(input_frame, width=30)
title_entry.pack(side="left", fill="x", expand=True)

button_frame = Frame(root)
button_frame.pack(fill="x", padx=5, pady=5)
submit_button = Button(button_frame, text="Fetch Transcript", command=fetch_and_display_transcript)
submit_button.pack(side="left", expand=True)
download_button = Button(button_frame, text="Download Simple", command=download_transcript, state="disabled")
download_button.pack(side="left", expand=True)
download_full_button = Button(button_frame, text="Download Full", command=download_transcript_with_timestamps, state="disabled")
download_full_button.pack(side="left", expand=True)

display_frame = Frame(root)
display_frame.pack(fill="both", expand=True, padx=5, pady=5)
transcript_display = Text(display_frame, height=10)
transcript_display.pack(side="left", fill="both", expand=True)
scroll = Scrollbar(display_frame, command=transcript_display.yview, orient=VERTICAL)
transcript_display.configure(yscrollcommand=scroll.set)
scroll.pack(side="right", fill="y")

root.mainloop()
