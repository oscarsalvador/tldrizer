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