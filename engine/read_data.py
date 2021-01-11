import numpy as np
import pandas as pd
import streamlit as st
from engine.model import *
from pydub import AudioSegment
import sklearn
import librosa
from librosa.feature import melspectrogram
from uuid import uuid4
from PIL import Image

import pandas as pd
import wave
from scipy.io import wavfile
import os
import warnings

AUDIO_EXTENSIONS = ["wav", "mp3"]

classes_to_predict=sorted([
    "athenoct",
    "cocccocc",
    "crexcrex",
    "embecitr",
    "eritrube",
    "frincoel",
    "garrglan",
    "hirurust",
    "luscmega",
    "nocall",
    "parumajo",
    "passdome",
    "phylcoll",
    "phyltroc",
    "picapica",
    "picucanu",
    "pyrrpyrr",
    "sitteuro",
    "trogtrog",
    "turdilia",
    "turdphil"
  ])

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


def read_mp3(uploaded_mp3, model=load_model()):
    try:
        wave_data, wave_rate = librosa.load(uploaded_mp3)

        wave_data, _ = librosa.effects.trim(wave_data)
        song_sample = []
        sample_length = 5*wave_rate
        samples_from_file = pd.DataFrame(columns=['subsample_begin','subsample_id','pred_bird'])

        N_mels = 216
        for idx in range(0, len(wave_data), sample_length):
            song_sample = wave_data[idx:idx + sample_length]
            if len(song_sample) >= sample_length:
                mel = melspectrogram(song_sample, n_mels=N_mels)
                db = librosa.power_to_db(mel)
                normalised_db = sklearn.preprocessing.minmax_scale(db)
                sample_name = str(uuid4())
                db_array = (np.asarray(normalised_db) * 255).astype(np.uint8)
                spectre_array = np.array([db_array, db_array, db_array]).T
                #spectre_image = Image.fromarray(spectre_array)
                prediction = model.predict(spectre_array.reshape(1,216,216,3))
                predicted_bird=classes_to_predict[np.argmax(prediction)]
                output={
                         "subsample_begin": idx,
                         "subsample_id": sample_name,
                         "pred_bird": predicted_bird
                        }
                samples_from_file = samples_from_file.append(pd.DataFrame.from_dict(output, orient='index').transpose())

                if idx == 0:
                    output_array = spectre_array
                else:
                    output_array = np.concatenate((output_array, spectre_array), axis=0)

        return samples_from_file, output_array
    except:
        raise