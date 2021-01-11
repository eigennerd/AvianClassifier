from engine.read_data import *
from engine.model import *
import pydot_ng as pydot
import os
import streamlit as st
import json
# config.json has page content
with open('engine/config.json') as conf_file: # load JSON config file
    configGlobal = json.load(conf_file)
    texts = configGlobal['demo']
# declare placeholders
header = st.empty()         # placeholder for 1st header
header_text = st.empty()    # placeholder for 1st textbox
show_bird_1 = st.empty()    # this will show prediction picture     (bird_1)
show_bird_2 = st.empty()    # this will show 2nd prediction picture (bird_2)
show_bird_3 = st.empty()    # this will show 3rd prediction picture (bird_3)
# declare headers
header.header(texts['header_1'])
header_text.write(texts['intro_1'])

model = load_model()

test_dir = os.path.join(# todo: change this
                        os.path.dirname(os.path.realpath(__file__)), # where am i?
                        'test_audio')

audiofiles = get_audio_files_in_dir(test_dir)

if len(audiofiles) == 0:
    st.write("Put some audio files in your test directory (%s) to activate this player."   % test_dir)
else:
    filename = st.sidebar.selectbox("Select mp3 from test directory (%s)" % test_dir, audiofiles, 0)
    audiopath = os.path.join(test_dir, filename)

if os.path.exists(audiopath):
    st.sidebar.audio(audiopath)
    samples_db, spectrogram = read_mp3(audiopath, model=model)
    st.write(samples_db)
    st.image(Image.fromarray(spectrogram))


