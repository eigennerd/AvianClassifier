import numpy as np
import pandas as pd
import librosa
import sklearn
import streamlit as st
from uuid import uuid4
from librosa.feature import melspectrogram
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation,BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.applications import EfficientNetB0

birds_df = pd.read_csv('data/test_birds.csv', encoding='latin1')

classes_to_predict = sorted(birds_df.ebird_code.unique())


def load_model(classes_to_predict=classes_to_predict, weights_path='model/EN4_cpu_20sp_1000s_20e.h5'):
    input_shape = (216, 216, 3)
    effnet_layers = EfficientNetB0(weights=None, include_top=False, input_shape=input_shape)

    for layer in effnet_layers.layers:
        layer.trainable = True

    dropout_dense_layer = 0.3

    model = Sequential()
    model.add(effnet_layers)
    model.add(GlobalAveragePooling2D())
    model.add(Dense(256, use_bias=False))
    model.add(BatchNormalization())
    model.add(Activation('relu'))  #
    model.add(Dropout(dropout_dense_layer))  # dropout layer to probabilistically remove inputs from previous layers or data sample. makes robust
    model.add(Dense(len(classes_to_predict), activation="softmax"))

    model.load_weights(weights_path)

    return model


model = load_model()


def read_mp3(uploaded_mp3):
    try:
        wave_data, wave_rate = librosa.load(uploaded_mp3)

        wave_data, _ = librosa.effects.trim(wave_data)
        song_sample = []
        sample_length = 5*wave_rate
        samples_from_file = pd.DataFrame(columns=['subsample_begin','subsample_id','pred_bird', 'prediction'])

        N_mels = 216
        for idx in range(0, len(wave_data), sample_length):
            song_sample = wave_data[idx:idx + sample_length]
            if len(song_sample) >= sample_length:
                mel = melspectrogram(song_sample, n_mels=N_mels, fmin=1400)
                db = librosa.power_to_db(mel**2)
                normalised_db = sklearn.preprocessing.minmax_scale(db)
                sample_name = str(uuid4())
                db_array = (np.asarray(normalised_db) * 255).astype(np.uint8)
                spectre_array = np.array([db_array, db_array, db_array]).T
                #spectre_image = Image.fromarray(spectre_array)
                prediction = model.predict(spectre_array.reshape(1, 216, 216, 3))
                predicted_bird=classes_to_predict[np.argmax(prediction)]
                output = {
                         "subsample_begin": idx,
                         "subsample_id": sample_name,
                         "pred_bird": predicted_bird,
                         "prediction": prediction
                        }
                samples_from_file = samples_from_file.append(pd.DataFrame.from_dict(output, orient='index').transpose())

                if idx == 0:
                    output_array = spectre_array
                else:
                    output_array = np.concatenate((output_array, spectre_array), axis=0)

        return samples_from_file, output_array
    except:
        raise
