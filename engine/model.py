import numpy as np
import pandas as pd
import librosa
import sklearn
import shutil
import os
from scipy.special import logit
from PIL import Image
import streamlit as st
from uuid import uuid4
from librosa.feature import melspectrogram
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.compat.v1.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
from google.cloud import storage
## setting page width here as this is the file where first streamlit commands are exec'td


birds_df = pd.read_csv('data/test_birds.csv', encoding='latin1')

classes_to_predict = sorted(birds_df.ebird_code.unique())  # TODO: add 'nocall' later


def download_from_bucket(bucket_name='acoustic-scarab-bucket', prefix='model/'):
    '''
        downloads model and other data from the public bucket
    '''
    storage_client = storage.Client.create_anonymous_client()

    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        directory = "/".join(file_split[0:-1])
        Path(directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(blob.name)

def check_download_data():
    ## check for model
    if os.path.exists('model'):
        pass
    else:
        with st.spinner('We are fetching some data for initial run, please allow a few moments...'):
            download_from_bucket()
    ## check for test_audio
    if os.path.exists('test_audio'):
        pass
    else:
        with st.spinner('Almost there... '):
            download_from_bucket(prefix='test_audio/')

@st.cache(allow_output_mutation=True)
def load_model_to_st(model_path='model'):
    '''
        loads complete model architecture with weights
    '''
    check_download_data()
    with st.spinner('Loading model...'):
        model = tf.keras.models.load_model(model_path)
    model.make_predict_function()
    model.summary()

    return model


def read_mp3(uploaded_mp3, model = load_model_to_st()):
    '''

    :param uploaded_mp3:
    :return:
                #  complete output
                #  spectra of the processed mp3
                #  url of the predicted bird
                #  Scientific name
    '''
    try:


        wave_data, wave_rate = librosa.load(uploaded_mp3)

        wave_data, _ = librosa.effects.trim(wave_data)
        target_size = (216, 216)
        sample_length = 5 * wave_rate
        samples_from_file = []

        temp_folder = 'temp'

        if os.path.exists(temp_folder): ## create temporary folder to which to dump spectrograms
            shutil.rmtree(temp_folder)

        os.mkdir(temp_folder)

        with st.spinner('Reading data'):
            N_mels = 216
            for idx in range(0, len(wave_data), sample_length): # dumping spectrograms, making an array for output
                song_sample = wave_data[idx:idx + sample_length]
                if len(song_sample) >= sample_length:
                    mel = melspectrogram(song_sample, n_mels=N_mels, fmin=1400)
                    db = librosa.power_to_db(mel ** 2)
                    normalised_db = sklearn.preprocessing.minmax_scale(db)
                    sample_name = str(uuid4())+".tif"
                    db_array = (np.asarray(normalised_db) * 255).astype(np.uint8)
                    spectre_array = np.array([db_array, db_array, db_array]).T
                    spectre_image = Image.fromarray(spectre_array)
                    spectre_image.save(f"{temp_folder}/{sample_name}") ## saving files to temp folder
                    samples_from_file.append({"song_sample":f"{temp_folder}/{sample_name}",
                                                        "y":"nocall"})
                    if idx == 0: #
                        output_array = spectre_array
                    else:
                        output_array = np.concatenate((output_array, spectre_array), axis=0)

        samples_from_file = pd.DataFrame(samples_from_file)

        datagen = ImageDataGenerator(rescale=1./255, preprocessing_function=preprocess_input)

        test_generator = datagen.flow_from_dataframe( # creating test generator
            dataframe=samples_from_file,
            x_col='song_sample',
            y_col='y',
            target_size=target_size,
            shuffle=False,
            batch_size=1,
            class_mode='categorical'
        )
        with st.spinner('Running predictions...'):
            preds = model.predict(test_generator, steps=len(samples_from_file))  # feeding test generator to model
            logits = logit(preds)
            list_of_preds = []
            table_of_probabilities = pd.DataFrame({"ebird_code": classes_to_predict,
                                                 "certainty": (1/(1+np.exp(-logits.mean(axis=0)))),
                                                  "logit": logits.mean(axis=0)}).merge(
                                                 birds_df[['ebird_code', 'en', 'gen', 'sp']], on='ebird_code'
                                                )

            for i in range(0, len(samples_from_file)):
                list_of_preds.append({"bird":f"{classes_to_predict[np.argmax(preds[i])]}"})

            predicted_bird = table_of_probabilities.nlargest(1, columns='certainty').ebird_code.values[0]

        seconds_30 = 2160

        return table_of_probabilities, \
               output_array[0:seconds_30, ], \
               birds_df.loc[birds_df.ebird_code == predicted_bird].url.values[0], \
               "{} {}".format(birds_df.loc[birds_df.ebird_code == predicted_bird].gen.values[0],
                              birds_df.loc[birds_df.ebird_code == predicted_bird].sp.values[0]), \
                preds


    except Exception as e:
        print(e)
