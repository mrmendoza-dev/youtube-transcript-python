from PySide6.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
	QLabel, QTextEdit, QFileDialog
)
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt
from youtube_transcript_api import YouTubeTranscriptApi
import re
import sys

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
		return None

def get_video_id(video_url):
	patterns = [
		r"youtube\.com/watch\?v=([^\&\#]+)",
		r"youtube\.com/watch\?.*v=([^\&\#]+)",
		r"youtube\.com/shorts/([^\?]+)",
		r"youtu\.be/([^\?]+)",
		r"youtube\.com/embed/([^\?]+)"
	]
	for pattern in patterns:
		match = re.search(pattern, video_url)
		if match:
			return match.group(1)
	return None

class TranscriptFetcher(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("YouTube Transcript Fetcher")
		self.setGeometry(100, 100, 600, 400)
		self.setMinimumSize(500, 400)

		# Dark mode palette
		dark_palette = QPalette()
		dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
		dark_palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
		dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
		dark_palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
		dark_palette.setColor(QPalette.ToolTipBase, QColor(30, 30, 30))
		dark_palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
		dark_palette.setColor(QPalette.Text, QColor(220, 220, 220))
		dark_palette.setColor(QPalette.Button, QColor(40, 40, 40))
		dark_palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
		dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
		dark_palette.setColor(QPalette.Highlight, QColor(60, 120, 200))
		dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
		self.setPalette(dark_palette)
		self.setAutoFillBackground(True)
		self.setFont(QFont("Segoe UI", 11))

		main_layout = QVBoxLayout()
		main_layout.setSpacing(18)
		main_layout.setContentsMargins(24, 24, 24, 24)

		# --- Input Row ---
		input_row = QHBoxLayout()
		self.url_input = QLineEdit()
		self.url_input.setPlaceholderText("YouTube Video URL")
		self.url_input.setMinimumWidth(300)
		self.url_input.setStyleSheet("QLineEdit { background: #222; color: #eee; border-radius: 6px; padding: 8px; border: 1px solid #444; }")
		input_row.addWidget(QLabel("URL:"))
		input_row.addWidget(self.url_input)

		self.title_input = QLineEdit()
		self.title_input.setPlaceholderText("Title (optional)")
		self.title_input.setMinimumWidth(150)
		self.title_input.setStyleSheet("QLineEdit { background: #222; color: #eee; border-radius: 6px; padding: 8px; border: 1px solid #444; }")
		input_row.addWidget(QLabel("Title:"))
		input_row.addWidget(self.title_input)
		main_layout.addLayout(input_row)

		# --- Buttons Row ---
		btn_row = QHBoxLayout()
		self.fetch_btn = QPushButton("Fetch Transcript")
		self.fetch_btn.setStyleSheet("QPushButton { background: #3b4252; color: #fff; border-radius: 6px; padding: 8px 18px; font-weight: bold; } QPushButton:hover { background: #4c566a; }")
		self.fetch_btn.clicked.connect(self.fetch_transcript)
		btn_row.addWidget(self.fetch_btn)

		self.save_btn = QPushButton("Download Simple")
		self.save_btn.setEnabled(False)
		self.save_btn.setStyleSheet("QPushButton { background: #444; color: #fff; border-radius: 6px; padding: 8px 18px; font-weight: bold; } QPushButton:disabled { background: #222; color: #888; }")
		self.save_btn.clicked.connect(self.save_transcript)
		btn_row.addWidget(self.save_btn)

		self.save_full_btn = QPushButton("Download Full")
		self.save_full_btn.setEnabled(False)
		self.save_full_btn.setStyleSheet("QPushButton { background: #444; color: #fff; border-radius: 6px; padding: 8px 18px; font-weight: bold; } QPushButton:disabled { background: #222; color: #888; }")
		self.save_full_btn.clicked.connect(self.save_transcript_with_timestamps)
		btn_row.addWidget(self.save_full_btn)
		main_layout.addLayout(btn_row)

		# --- Transcript Display ---
		self.transcript_display = QTextEdit()
		self.transcript_display.setReadOnly(True)
		self.transcript_display.setStyleSheet("QTextEdit { background: #181818; color: #eee; border-radius: 6px; padding: 10px; border: 1px solid #444; }")
		main_layout.addWidget(self.transcript_display, stretch=1)

		# --- Status Label ---
		self.status = QLabel("")
		self.status.setStyleSheet("QLabel { color: #8ec07c; font-weight: bold; min-height: 24px; }")
		main_layout.addWidget(self.status)

		self.setLayout(main_layout)

		# Data
		self.last_transcript = None
		self.last_transcript_full = None

	def fetch_transcript(self):
		url = self.url_input.text().strip()
		video_id = get_video_id(url)
		if not video_id:
			self.status.setText("Invalid YouTube URL.")
			self.transcript_display.clear()
			self.save_btn.setEnabled(False)
			self.save_full_btn.setEnabled(False)
			return
		transcript = get_transcript(video_id)
		transcript_full = get_transcript(video_id, with_timestamps=True)
		if transcript:
			self.transcript_display.setPlainText(transcript)
			self.status.setText("Transcript fetched.")
			self.save_btn.setEnabled(True)
			self.save_full_btn.setEnabled(True)
			self.last_transcript = transcript
			self.last_transcript_full = transcript_full
		else:
			self.transcript_display.clear()
			self.status.setText("No transcript found or error occurred.")
			self.save_btn.setEnabled(False)
			self.save_full_btn.setEnabled(False)

	def save_transcript(self):
		title = slugify(self.title_input.text().strip())
		url = self.url_input.text().strip()
		initial_filename = f"transcript-{title}.txt" if title else "transcript.txt"
		file_path, _ = QFileDialog.getSaveFileName(self, "Save Transcript", initial_filename, "Text Files (*.txt);;All Files (*)")
		if file_path:
			with open(file_path, "w", encoding="utf-8") as f:
				if title:
					f.write(f"Title: {title}\n")
				f.write(f"URL: {url}\n\n")
				f.write(self.last_transcript or "")

	def save_transcript_with_timestamps(self):
		title = slugify(self.title_input.text().strip())
		url = self.url_input.text().strip()
		initial_filename = f"transcript-timestamps-{title}.txt" if title else "transcript_w_timestamps.txt"
		file_path, _ = QFileDialog.getSaveFileName(self, "Save Transcript with Timestamps", initial_filename, "Text Files (*.txt);;All Files (*)")
		if file_path and self.last_transcript_full:
			with open(file_path, "w", encoding="utf-8") as f:
				if title:
					f.write(f"Title: {title}\n")
				f.write(f"URL: {url}\n\n")
				for item in self.last_transcript_full:
					line = f"[{item['start']}] {item['text']}\n"
					f.write(line)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = TranscriptFetcher()
	win.show()
	sys.exit(app.exec())
