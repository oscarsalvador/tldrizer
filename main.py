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



if __name__ == '__main__':
  args = vars(parser.parse_args())

  example = AppGUI("clearlooks", "1400x800", args["sockets_timestamp"])
  example.mainloop()
