import numpy as np
import pandas as pd
import streamlit as st
import os

AUDIO_EXTENSIONS = ["wav", "mp3"]

@st.cache()
def get_audio_files_in_dir(directory):
    out = ['<select>']
    for item in os.listdir(directory):
        try:
            name, ext = item.split(".")
        except:
            continue
        if name and ext:
            if ext in AUDIO_EXTENSIONS:
                out.append(item)
    return out

