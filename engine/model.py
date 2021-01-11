import keras
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation,BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.applications import EfficientNetB0
import json
import pydot

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

def load_model(classes_to_predict=classes_to_predict, weights_path='engine/21 species HQ CPU.h5'):
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