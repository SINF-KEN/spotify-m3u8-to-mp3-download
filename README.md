# Spotify Playlist Downloader

A simple Python script that downloads all the songs from a Spotify playlist.

## Getting Started

To get the m3u8 file, visit [Spotify to m3u8](https://lukasticky.gitlab.io/spotify-to-m3u/).
https://lukasticky.gitlab.io/spotify-to-m3u/ 

### Prerequisites

Ensure you have Python installed. Create a virtual environment and install the necessary dependencies.

### Installation

1. **Set up the virtual environment:**

   ```bash
   python3 -m venv env
   ```

2. **Activate the virtual environment:**

   - **macOS:**

     ```bash
     source env/bin/activate
     ```

   - **Windows:**

     ```powershell
     .\env\Scripts\activate
     ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Open the script:**
   
   Edit `music_download.py` to update the file path (output and also m3u8) and insert your Last.fm API key.

### Usage

Run the script:

```bash
python music_download.py
```

---
i hope you like it :) 