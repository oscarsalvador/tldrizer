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



if __name__ == '__main__':
  args = vars(parser.parse_args())

  example = AppGUI("clearlooks", "1400x800", args["sockets_timestamp"])
  example.mainloop()
