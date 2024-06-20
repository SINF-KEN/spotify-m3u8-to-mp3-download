import os
import re
import yt_dlp
import shutil
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON, TYER, error
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time

# Define the path to your M3U8 file and the root directory for the output
m3u8_file_path = 'file.m3u8' ## change this to the path of your m3u8 file
root_dir = '/path/to/output' ## change this to the path of the output directory


# Read the M3U8 file and extract song information
with open(m3u8_file_path, 'r') as file:
    lines = file.readlines()

songs = []
for line in lines:
    match = re.match(r'#EXTINF:\d+,(.+) - (.+)', line)
    if match:
        artist, title = match.groups()
        songs.append((artist, title))

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.4',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.5',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Avast/125.0.0.0'
]


download_counter = 0

# Define yt-dlp options
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        'nopostoverwrites': False,
    }],
    'nocheckcertificate': True,
}

def switch_user_agent():
    global download_counter
    global ydl_opts

    if download_counter % 200 == 0:
        new_user_agent = random.choice(user_agents)
        ydl_opts['http_headers'] = {'User-Agent': new_user_agent}
        print(f'Switching to new user-agent: {new_user_agent}')

# Function to fetch song metadata from Last.fm
def fetch_metadata(artist, title):
    api_key = 'API'  # Replace with your Last.fm API key
    url = f'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artist}&track={title}&format=json'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        track = data.get('track', {})
        album = track.get('album', {}).get('title', 'Unknown Album')
        genre = track.get('toptags', {}).get('tag', [{}])[0].get('name', 'Unknown Genre')
        year = track.get('wiki', {}).get('published', '2023').split('-')[0]  # Default year to 2023
        return album, genre, year
    return 'Unknown Album', 'Unknown Genre', '2023'

# Function to download a song using yt-dlp
def download_song(artist, title):
    global download_counter

    switch_user_agent()

    query = f'{artist} {title} audio'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        attempts = 3
        for attempt in range(attempts):
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                ydl.download([info['webpage_url']])
                download_counter += 1
                return ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3'), info
            except yt_dlp.utils.DownloadError as e:
                print(f'Error downloading {artist} - {title}: {e}. Retrying ({attempt + 1}/{attempts})...')
                time.sleep(5)
        raise Exception(f"Failed to download {artist} - {title} after {attempts} attempts.")

# Function to download album cover
def download_album_cover(album_cover_url, album_cover_path):
    response = requests.get(album_cover_url)
    if response.status_code == 200:
        with open(album_cover_path, 'wb') as cover_file:
            cover_file.write(response.content)

# Function to make an image square
def make_image_square(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        new_size = min(width, height)
        left = (width - new_size) / 2
        top = (height - new_size) / 2
        right = (width + new_size) / 2
        bottom = (height + new_size) / 2
        img = img.crop((left, top, right, bottom))
        img = img.resize((new_size, new_size), Image.LANCZOS)
        img.save(image_path)

# Function to embed album cover and metadata into MP3
def embed_metadata(mp3_file, album_cover_path, artist, title, album, genre, year):
    audio = MP3(mp3_file, ID3=ID3)
    # Add ID3 tag if not present
    try:
        audio.add_tags()
    except error:
        pass

    # Add metadata
    audio.tags.add(TIT2(encoding=3, text=title))  # Title
    audio.tags.add(TPE1(encoding=3, text=artist))  # Artist
    audio.tags.add(TALB(encoding=3, text=album))  # Album
    audio.tags.add(TCON(encoding=3, text=genre))  # Genre
    audio.tags.add(TYER(encoding=3, text=str(year)))  # Year
    
    # Add album cover
    with open(album_cover_path, 'rb') as album_art:
        audio.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime='image/jpeg',  # image mime type
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=album_art.read()
            )
        )
    audio.save()

# Function to process a song
def process_song(artist, title):
    print(f'Downloading: {artist} - {title}')
    try:
        mp3_file, info = download_song(artist, title)
        
        album, genre, year = fetch_metadata(artist, title)
        album_cover_url = info['thumbnail']
        
        album_dir = os.path.join(root_dir, album)
        os.makedirs(album_dir, exist_ok=True)
        
        output_file = os.path.join(album_dir, f'{artist} - {title}.mp3')
        shutil.move(mp3_file, output_file)
        
        # Download album cover
        album_cover_path = os.path.join(album_dir, f'{artist} - {title}.jpg')
        download_album_cover(album_cover_url, album_cover_path)
        
        # Make album cover square
        make_image_square(album_cover_path)
        
        # Embed metadata into MP3
        embed_metadata(output_file, album_cover_path, artist, title, album, genre, year)
        
        #print(f'Saved to: {output_file}')
        #print(f'Album cover saved to: {album_cover_path}')
        #print(f'Album name: {album}')
        #print(f'Genre: {genre}')
        #print(f'Year: {year}')
    except Exception as e:
        print(f'Failed to download {artist} - {title}: {e}')

# Multithreading for processing songs
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_song, artist, title) for artist, title in songs]
    for future in as_completed(futures):
        future.result()  # To catch and print any exceptions raised
