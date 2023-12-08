# import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
# from PIL import Image
from datetime import timedelta
import subprocess
import argparse

from utils import *


class AppGUI(ThemedTk):
  def __init__(self, theme, geometry, timestamp):
    ThemedTk.__init__(self, fonts=True, themebg=True)
    self.set_theme(theme)
    self.title("tldrizer")
    self.geometry(geometry)


    self.sockets_timestamp = timestamp
    self.url = tk.StringVar()
    self.search = tk.StringVar()
    self.search_results = []
    self.search_current_index = ""
    self.capt_text = ""
    self.capt_segments = ""
    self.summ_text = ""
    self.video_path = ""
    self.models_dir="/tldrizer/models/"
    self.current_tasks = 0
    self.done_tasks = 0


    self.title_frame = ttk.Frame(self)
    self.title_frame.pack(fill=tk.X, padx=5, pady=5)
    self.style = ttk.Style()
    self.style.configure("Title.TLabel", font=("Arial", 12, "bold"))
    self.title = ttk.Label(self.title_frame, text="[Untitled]", style="Title.TLabel", wraplength=1300)
    self.title.pack(side=tk.LEFT)
    self.video_len = ttk.Label(self.title_frame, text="00:00:00", style="Title.TLabel")
    self.video_len.pack(side=tk.RIGHT)

    self.top_text = ttk.Entry(self, justify="left", textvariable=self.url)
    self.top_text.pack(fill="x", padx=5, pady=5)


    self.bar_frame = ttk.Frame(self)
    self.bar_frame.pack(fill=tk.X)

    self.button_frame = ttk.Frame(self.bar_frame)
    self.button_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

    self.clear_button = ttk.Button(self.button_frame, text="Clear", 
      command=lambda: self.clear())
    self.clear_button.pack(side=tk.LEFT)

    self.clear_button = ttk.Button(self.button_frame, text="Summarize text",
      command=lambda: (
        self.clear(True),
        self.summarize_left()

      ))
    self.clear_button.pack(side=tk.LEFT, padx=5)
    
    self.mpv_button = ttk.Button(self.button_frame, text="Open video",
      command=lambda: (
        print("open video: "+ self.sockets_timestamp),
        subprocess.run('echo "mpv ' + self.url.get() + 
          ' --input-ipc-server=/tmp/tldrizer/mpvsocket' + self.sockets_timestamp + 
          '" | nc -q 0 -U "/tmp/tldrizer/tldrizersocket' + self.sockets_timestamp + '"', shell=True)
        # VideoPlayer(self).start()
      ))
    self.mpv_button.pack(side=tk.LEFT)

    self.all_button = ttk.Button(self.button_frame, text="DL, transcribe & summarize",
      command=lambda: (
        print("\nDL, transcribe & summarize"),
        Worker(self, "dl capt summ").start()
      ))
    self.all_button.pack(side=tk.LEFT, padx=5)

    self.dl_trns_button = ttk.Button(self.button_frame, text="DL & transcribe", 
      command=lambda: (
        print("\nDL & transcribe"),
        Worker(self, "dl capt").start()
    ))
    self.dl_trns_button.pack(side=tk.LEFT)

    self.summarize_button = ttk.Button(self.button_frame, text="Summarize video",
      command=lambda: (
        print("\nSummarize"),
        Worker(self, "summ").start()
    ))
    self.summarize_button.pack(side=tk.LEFT, padx=5)

    self.progress_frame = ttk.Frame(self.bar_frame)
    self.progress_frame.pack(side=tk.RIGHT)

    self.progress = ttk.Progressbar(self.progress_frame, 
      maximum=100, 
      value=0, 
      length=300,
      orient="horizontal",
      mode="determinate")
    self.progress.pack(side=tk.RIGHT, expand=True, padx=5, ipady=2)
    # self.progress.start()


    self.l_text = tk.Text(self, height=30, width=60, wrap='word')
    self.l_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    self.l_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL)
    self.l_scroll.pack(side=tk.LEFT, fill="y", pady=5)
    # self.l_text.config(yscrollcommand=self.l_scroll.set)
    self.l_text['yscrollcommand'] = self.l_scroll.set
    self.l_scroll['command'] = self.l_text.yview


    self.right_frame = ttk.Frame(self)
    self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    self.r_text_frame = ttk.Frame(self.right_frame)
    self.r_text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    self.r_text = tk.Text(self.r_text_frame, height=30, width=40, wrap='word')
    self.r_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    self.r_scroll = ttk.Scrollbar(self.r_text_frame, orient=tk.VERTICAL)
    self.r_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,5), pady=5)
    self.r_text['yscrollcommand'] = self.r_scroll.set
    self.r_scroll['command'] = self.r_text.yview


    self.search_frame = ttk.Frame(self.right_frame)
    self.search_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5)

    self.search_label = ttk.Label(self.search_frame, text="Find in transcription: ")
    self.search_label.pack(side=tk.LEFT)

    self.search_text = ttk.Entry(self.search_frame, justify="left", textvariable=self.search)
    self.search_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
    self.search_text.bind('<KeyRelease>', lambda event: (self.clear_search(self)))
    
    self.n_search_button = ttk.Button(self.search_frame, text="Next", 
      command=lambda: self.search_l_text())
    self.n_search_button.pack(side=tk.RIGHT)
    self.bind('<Control-End>', lambda event:   self.n_search_button.invoke())

    self.p_search_button = ttk.Button(self.search_frame, text="Prev", 
      command=lambda: self.search_l_text_prev())
    self.p_search_button.pack(side=tk.RIGHT, padx=5)
    self.bind('<Control-Home>', lambda event:   self.p_search_button.invoke())  
    



  def clear(self, skip_l_text=False):
    self.title.config(text="[Untitled]")
    self.video_len.config(text="00:00:00")
    self.top_text.delete(0, tk.END)
    if not skip_l_text: 
      self.l_text.delete("1.0", tk.END)
    self.r_text.delete("1.0", tk.END)
    # self.progress.config(value=0)
    print("progressbar: " + str(self.progress.cget("value")))
    self.progress.config(value=0)
    self.current_tasks = 0
    self.done_tasks = 0
    self.search_text.delete(0, tk.END)
    

  def fill_l_text(self):
    self.l_text.delete("1.0", tk.END)

    # last tstamp without decimals
    has_hours = True
    last_timestamp = str(timedelta(seconds=self.capt_segments[-1]["start"])).split(".")[0]
    if last_timestamp.split(":")[0] == "0" :
      has_hours = False

    for caption in self.capt_segments:
      button = tk.Button(self.l_text, borderwidth=0, highlightthickness=0, highlightbackground='white',
        text= str(timedelta(seconds=caption["start"])).split(".")[0] 
          if has_hours else str(timedelta(seconds=caption["start"])).split(".")[0][2:],
        command=lambda start=caption["start"]: # pass as arg so that it has it later, instead of being overwritten
          # print(start)
          self.seek_timestamp(start)
      )
      self.l_text.window_create(tk.END, window=button)
      self.l_text.insert(tk.END,  f"{caption['text']}\n")
      

  def summarize_left(self):
    self.capt_text = self.l_text.get("1.0", tk.END)
    Worker(self, "summ").start()
    

  def fill_r_text(self):
    self.r_text.delete("1.0", tk.END)
    text = self.summ_text[1:] if self.summ_text[0] == " " else self.summ_text
    self.r_text.insert(tk.END, text)


  def seek_timestamp(self, timestamp):
    print("\nseek_timestamp()")
    subprocess.run('echo \'{ "command": ["seek", "' + str(timestamp) + 
      '", "absolute"] }\' | nc -q 0 -U "/tmp/tldrizer/mpvsocket' + self.sockets_timestamp + '"', shell=True)


  def update_progressbar(self, increase):
    print("\nupdate_progressbar()")
    print("self.current_tasks: ", self.current_tasks)

    print("self.done_tasks: ", self.done_tasks)
    print("increase: ", increase)
    
    self.done_tasks = self.done_tasks + increase
    print("self.done_tasks: ", self.done_tasks)

    self.progress.config(value=int(self.done_tasks / self.current_tasks * 100))