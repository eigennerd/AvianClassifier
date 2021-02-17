import numpy as np
import pandas as pd
import streamlit as st
import os
import pydeck as pdk
import json
import requests
import re
from googletrans import Translator
from settings import *

AUDIO_EXTENSIONS = ["wav", "mp3"]


@st.cache()
def get_audio_files_in_dir(directory):
    '''
    :param directory: default directory to pick mp3 files from
    :return: list of mp3 files
    '''
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
    '''
    :param audiopath:
    :return:
    '''
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
    '''
    :param audiopath:
    :param train_path:
    :param meta_path:
    :return:
    '''
    metadata = pd.read_csv(meta_path, encoding="ISO-8859-1", low_memory=False)
    num = float(audiopath.split('/')[-1].split('.')[0][4:])
    ebird_code = metadata[metadata['o'] == num]['ebird_code'].values[0]

    trn_df = pd.read_csv(train_path, low_memory=False)

    coords = trn_df[trn_df['ebird_code'] == ebird_code][['lat', 'lng', 'alt']]
    coords.dropna(inplace=True)
    coords['alt'] = pd.to_numeric(coords['alt'].replace(['?', '-'], 0))
    return coords


def get_vernacular(scientific_name='troglodytes troglodytes', lang='en'):
    """
    function that uses GBIF API to translate species scientific name into common English
    then it uses google api to translate that name into any other language if specified

    :param lang:
    :type lang:
    :param scientific_name: str
    :return: common_name: str
    """
    res = requests.get('https://api.gbif.org/v1/species?name={}'.format(scientific_name.lower()))
    key = json.loads(res.text)['results'][0]['speciesKey']  # get species key
    res2 = requests.get('https://api.gbif.org/v1/species/{}/vernacularNames'.format(key))
    vernacularName = ''
    for dict_element in json.loads(res2.text)['results']:
        if dict_element['language'] == 'eng' and '/' not in dict_element['vernacularName']:  # get the last english (and perhaps the most correct) vernacular (without forward slash)
            vernacularName = dict_element['vernacularName']

    out = scientific_name if vernacularName == '' else re.sub(' \((.*?)\)', '',
                                                              vernacularName)  # without anything in parentheses

    return out if lang == 'en' else Translator().translate(out, dest='en' if lang == 'ua' else lang.lower()).text


def handle_uploaded(file):
    name = 'data/tmp/upl.mp3'
    if not os.path.exists('data/tmp'):
        os.mkdir('data/tmp')

    with open(name, 'wb') as f:
        f.write(file.read())
    return name


def compare(bird_name, audio):
    true_data = pd.read_csv(meta, index_col=False)

    record_number = audio.split('.')[0][-2:]
    test_row = true_data[true_data['ind'] == int(record_number)]
    true_name = test_row['ebird_code'].values[0]

    predicted_name = '{}{}'.format(bird_name.split(' ')[0][:4].lower(),
                                   bird_name.split(' ')[1][:4].lower())

    if true_name == predicted_name:
        return True
    return False


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


