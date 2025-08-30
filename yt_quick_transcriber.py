#!/usr/bin/env python3
import os
import sys
import whisper
import tempfile
import subprocess
import mimetypes

def download_audio(url):
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "audio.%(ext)s")
    subprocess.run([
        "yt-dlp", "-x", "--audio-format", "mp3", "-o", 
output_path, url
    ], check=True)
    return os.path.join(temp_dir, "audio.mp3")

def format_ts(sec, srt=True):
    ms = int((sec % 1) * 1000)
    sec = int(sec)
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    sep = "," if srt else "."
    return f"{h:02}:{m:02}:{s:02}{sep}{ms:03}"

def save_srt(res, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for i, seg in enumerate(res["segments"], start=1):
            
f.write(f"{i}\n{format_ts(seg['start'])} 
--> 
{format_ts(seg['end'])}\n{seg['text'].strip()}\n\n")
f.write(f"{i}\n{format_ts(seg['start'])} 
--> {format_ts(seg['end'])}\n{seg['text'].strip()}\n\n")
    print(f"[+] SRT saved: {filename}")

def save_vtt(res, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for seg in res["segments"]:
            f.write(f"{format_ts(seg['start'], srt=False)} 
--> {format_ts(seg['end'], 
srt=False)}\n{seg['text'].strip()}\n\n")
    print(f"[+] VTT saved: {filename}")

def transcribe(file_path, output_file="transcript.txt", 
model_name="tiny", out_format="all", lang=None):
    model = whisper.load_model(model_name)
    print(f"[+] Processing: {file_path} using model: 
{model_name}")
    
    result = model.transcribe(file_path, language=lang)

    text = result["text"]
    print("\n===== Transcript =====\n")
    print(text)
    print("\n=====================\n")

    base = os.path.splitext(output_file)[0]

    if out_format in ("all", "txt"):
        with open(base + ".txt", "w", encoding="utf-8") as 
f:
            f.write(text)
        print(f"[+] TXT saved: {base}.txt")

    if out_format in ("all", "srt"):
        save_srt(result, base + ".srt")

    if out_format in ("all", "vtt"):
        save_vtt(result, base + ".vtt")

    print(f"[+] Language detected: {result['language']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: yt_quick_transcriber.py <file_or_url> 
[output_file] [model] [format] [lang]")
        print("  model  = tiny | base | small | medium | 
large (default: tiny)")
        print("  format = all | txt | srt | vtt (default: 
all)")
        print("  lang   = ISO code (e.g. en, ar) or leave 
blank for autodetect")
        sys.exit(1)

    src = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else 
"transcript.txt"
    model_name = sys.argv[3] if len(sys.argv) > 3 else 
"tiny"
    out_format = sys.argv[4] if len(sys.argv) > 4 else "all"
    lang = sys.argv[5] if len(sys.argv) > 5 else None

    if src.startswith("http"):
        audio = download_audio(src)
        transcribe(audio, out_file, model_name, out_format, 
lang)
        os.remove(audio)
    else:
        mime, _ = mimetypes.guess_type(src)
        if mime and mime.startswith("video"):
            with tempfile.NamedTemporaryFile(suffix=".mp3", 
delete=False) as tmp:
                temp_audio = tmp.name
            subprocess.run(["ffmpeg", "-i", src, "-vn", 
"-acodec", "libmp3lame", temp_audio, "-y"], check=True)
            transcribe(temp_audio, out_file, model_name, 
out_format, lang)
            os.remove(temp_audio)
        else:
            transcribe(src, out_file, model_name, 
out_format, lang)
#!/usr/bin/env 
python3
import os
import sys
import whisper
import tempfile
import subprocess
import mimetypes

def download_audio(url):
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "audio.%(ext)s")
    subprocess.run([
        "yt-dlp", "-x", "--audio-format", "mp3", "-o", output_path, url
    ], check=True)
    return os.path.join(temp_dir, "audio.mp3")

def format_ts(sec, srt=True):
    ms = int((sec % 1) * 1000)
    sec = int(sec)
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    sep = "," if srt else "."
    return f"{h:02}:{m:02}:{s:02}{sep}{ms:03}"

def save_srt(res, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for i, seg in enumerate(res["segments"], start=1):
            f.write(f"{i}\n{format_ts(seg['start'])} --> {format_ts(seg['end'])}\n{seg['text'].strip()}\n\n")
    print(f"[+] SRT saved: {filename}")

def save_vtt(res, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for seg in res["segments"]:
            f.write(f"{format_ts(seg['start'], srt=False)} --> {format_ts(seg['end'], srt=False)}\n{seg['text'].strip()}\n\n")
    print(f"[+] VTT saved: {filename}")

def transcribe(file_path, output_file="transcript.txt", model_name="tiny", out_format="all", lang=None):
    model = whisper.load_model(model_name)
    print(f"[+] Processing: {file_path} using model: {model_name}")
    
    result = model.transcribe(file_path, language=lang)

    text = result["text"]
    print("\n===== Transcript =====\n")
    print(text)
    print("\n=====================\n")

    base = os.path.splitext(output_file)[0]

    if out_format in ("all", "txt"):
        with open(base + ".txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[+] TXT saved: {base}.txt")

    if out_format in ("all", "srt"):
        save_srt(result, base + ".srt")

    if out_format in ("all", "vtt"):
        save_vtt(result, base + ".vtt")

    print(f"[+] Language detected: {result['language']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: yt_quick_transcriber.py <file_or_url> [output_file] [model] [format] [lang]")
        print("  model  = tiny | base | small | medium | large (default: tiny)")
        print("  format = all | txt | srt | vtt (default: all)")
        print("  lang   = ISO code (e.g. en, ar) or leave blank for autodetect")
        sys.exit(1)

    src = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else "transcript.txt"
    model_name = sys.argv[3] if len(sys.argv) > 3 else "tiny"
    out_format = sys.argv[4] if len(sys.argv) > 4 else "all"
    lang = sys.argv[5] if len(sys.argv) > 5 else None

    if src.startswith("http"):
        audio = download_audio(src)
        transcribe(audio, out_file, model_name, out_format, lang)
        os.remove(audio)
    else:
        mime, _ = mimetypes.guess_type(src)
        if mime and mime.startswith("video"):
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                temp_audio = tmp.name
            subprocess.run(["ffmpeg", "-i", src, "-vn", "-acodec", "libmp3lame", temp_audio, "-y"], check=True)
            transcribe(temp_audio, out_file, model_name, out_format, lang)
            os.remove(temp_audio)
        else:
            transcribe(src, out_file, model_name, out_format, lang)
