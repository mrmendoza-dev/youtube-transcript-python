# YouTube Transcript Generator

A simple GUI application to generate and download YouTube video transcripts with a modern dark interface.

## Features

- Simple PySide6-based GUI interface
- Generate transcripts with or without timestamps
- Works with various YouTube URL formats (videos, shorts, etc.)
- Save transcripts as text files
- Modern dark mode interface

## Prerequisites

- Python 3.7+ installed on your system
- Terminal/Command Prompt access

## Quick Start

### 1. Clone or Download

```bash
git clone <your-repo-url>
cd youtube-transcript-python
```

### 2. Activate Virtual Environment

```bash
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python youtube_transcript.py
```

## Alternative Installation Methods

### Manual dependency installation (if requirements.txt doesn't work)

```bash
pip install PySide6
pip install youtube-transcript-api
```

## Environment Setup (Required First Step)

Virtual environments keep your project dependencies isolated from your system Python. This prevents conflicts between different projects.

### Option 1: Automated Setup (Easiest)

**On Linux/macOS:**

```bash
chmod +x setup_env.sh
./setup_env.sh
```

**On Windows:**

```cmd
setup_env.bat
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (REQUIRED before installing packages)
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python youtube_transcript.py
```

### Why Use Virtual Environments?

- **Isolation**: Each project has its own packages
- **Clean system**: No conflicts with system Python
- **Reproducibility**: Easy to recreate the exact environment
- **Dependency management**: Clear what packages your project needs

## Usage

1. **Launch the application** - A dark-themed GUI window will appear
2. **Enter YouTube URL** - Paste any YouTube video URL in the URL field
3. **Optional title** - Add a custom title for your transcript file
4. **Fetch transcript** - Click "Fetch Transcript" to retrieve the transcript
5. **Download options**:
   - **Download Simple** - Plain text transcript
   - **Download Full** - Transcript with timestamps

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Troubleshooting

### Common Issues

**"Module not found" errors:**

- Ensure all dependencies are installed: `pip install -r requirements.txt`

**GUI not displaying:**

- Check if PySide6 is properly installed
- Verify Python version compatibility (3.7+)

**Transcript fetch failures:**

- Ensure the YouTube video has available transcripts
- Check your internet connection
- Verify the URL format is correct

### System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **Memory**: Minimum 100MB RAM
- **Display**: 500x400 minimum resolution

## Development

To contribute or modify:

1. Install development dependencies
2. Make your changes
3. Test with various YouTube URLs
4. Ensure the GUI remains responsive

## License

[Add your license information here]

---

**Note**: This application uses the YouTube Transcript API and is subject to YouTube's terms of service. Ensure you have permission to download transcripts for the content you're accessing.
