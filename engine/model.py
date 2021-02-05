import numpy as np
import pandas as pd
import librosa
import sklearn
import shutil
import os
from PIL import Image
import streamlit as st
from uuid import uuid4
from librosa.feature import melspectrogram
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator

birds_df = pd.read_csv('data/test_birds.csv', encoding='latin1')

classes_to_predict = sorted(birds_df.ebird_code.unique())  # TODO: add 'nocall' later


def load_model(classes_to_predict=classes_to_predict, weights_path='model/tf24_cpu_RN50_521_20sp_ns_1000s_newDataGen.h5'):
    input_shape = (216, 216, 3)
    resnet_layers = ResNet50(weights=None, include_top=False, input_shape=input_shape)

    model = Sequential()
    model.add(resnet_layers)
    model.add(GlobalAveragePooling2D())

    model.add(Dense(512, use_bias=False))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(Dense(256, use_bias=False))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(Dense(128, use_bias=False))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(Dense(len(classes_to_predict), activation="softmax"))

    model.load_weights(weights_path)

    return model


model = load_model()

def read_mp3(uploaded_mp3):
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
        song_sample = []
        sample_length = 5 * wave_rate
        samples_from_file = []

        temp_folder = 'temp'

        if os.path.exists(temp_folder): ## create temporary folder to which to dump spectrograms
            shutil.rmtree(temp_folder)

        os.mkdir(temp_folder)

        N_mels = 216
        for idx in range(0, len(wave_data), sample_length): # dumping spectrograms, making an array for output
            song_sample = wave_data[idx:idx + sample_length]
            if len(song_sample) >= sample_length:
                mel = melspectrogram(song_sample, n_mels=N_mels, fmin=1400)
                db = librosa.power_to_db(mel ** 2 )
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

        #st.write(samples_from_file)

        datagen = ImageDataGenerator(rescale=1./255)

        test_generator = datagen.flow_from_dataframe( # creating test generator
            dataframe=samples_from_file,
            x_col='song_sample',
            y_col='y',
            target_size=target_size,
            shuffle=False,
            batch_size=1,
            class_mode='categorical'
        )

        preds = model.predict(test_generator, steps=len(samples_from_file))  # feeding test generator to model
        list_of_preds = []
        table_of_probabilities = pd.DataFrame({"ebird_code": classes_to_predict,
                                             "probability": preds.mean(axis=0)}).merge(
                                             birds_df[['ebird_code', 'en']], on='ebird_code'
                                            )

        for i in range(0, len(samples_from_file)):
            list_of_preds.append({"bird":f"{classes_to_predict[np.argmax(preds[i])]}"})

        predicted_bird = table_of_probabilities.nlargest(1, columns='probability').ebird_code.values[0]

        seconds_30 = 2160

        return table_of_probabilities, \
               output_array[0:seconds_30, ], \
               birds_df.loc[birds_df.ebird_code == predicted_bird].url.values[0], \
               "{} {}".format(birds_df.loc[birds_df.ebird_code == predicted_bird].gen.values[0],
                              birds_df.loc[birds_df.ebird_code == predicted_bird].sp.values[0])


    except Exception as e:
        print(e)
