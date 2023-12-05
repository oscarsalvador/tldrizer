from threading import Thread
from yt_dlp import YoutubeDL

import tkinter as tk
import os
import subprocess
import time
import json

def download(gui):
  print("\ndownload")
  gui.video_path = "/tmp/" + str(int(time.time()))

  options = {
    "format": "bestaudio",
    "outtmpl": gui.video_path ,
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'm4a',
    }],
  }

  try:
    with YoutubeDL(options) as ytdl:
      info = ytdl.extract_info(gui.url.get(), download=False)
      gui.title.config(text=info.get("title", None))
      gui.video_len.config(text= time.strftime("%H:%M:%S", time.gmtime(info.get("duration", None))))
      gui.update_progressbar(1)


      result = ytdl.download([gui.url.get()])
      gui.update_progressbar(2)
      return True
  except Exception as e:
    print("Error in download: ", e)
    gui.clear()
    gui.title.config(text="Error, bad URL")
    return False

def transcribe(gui):
  print("\ntranscribe")

  model = whisper.load_model("base", download_root=gui.models_dir, device="cuda")
  gui.update_progressbar(2)

  # model = whisper.load_model("base", device="cuda")
  transcript = model.transcribe(gui.video_path + ".m4a")
  gui.update_progressbar(4)

  gui.capt_text = transcript["text"]
  gui.capt_segments = transcript["segments"]
  gui.fill_l_text()