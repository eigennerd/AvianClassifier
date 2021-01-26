import numpy as np
import pandas as pd
import streamlit as st
import os
import random
import pydeck as pdk
from settings import *

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


def form_pydeck(audiopath):
    df = extract_coords(audiopath, train_data, meta)

    layer = pdk.Layer(
        'ColumnLayer',
        data=df,
        get_position=["lng", "lat"],
        get_elevation="alt",
        elevation_scale=2000,
        radius=500,
        get_fill_color='[180, 0, 200, 140]',
        pickable=True,
        auto_highlight=True,
    )

    view = pdk.ViewState(
        longitude=df['lng'].values[0],
        latitude=df['lat'].values[0],
        zoom=10,
        min_zoom=1,
        max_zoom=23,
        pitch=50,
        bearing=0
    )

    return pdk.Deck(
        initial_view_state=view,
        layers=[layer]
    )


def extract_coords(audiopath, train_path, meta_path):
    metadata = pd.read_csv(meta_path, encoding="ISO-8859-1", low_memory=False)
    num = float(audiopath.split('/')[-1].split('.')[0][4:])
    ebird_code = metadata[metadata['o'] == num]['ebird_code'].values[0]

    trn_df = pd.read_csv(train_path, low_memory=False)

    coords = trn_df[trn_df['ebird_code'] == ebird_code][['lat', 'lng', 'alt']]
    coords.dropna(inplace=True)
    coords['alt'] = pd.to_numeric(coords['alt'].replace(['?', '-'], 0))
    print(coords.head(1))
    return coords
