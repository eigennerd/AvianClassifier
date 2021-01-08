#from engine.read_data import *
#from engine.model import *
import streamlit as st
import json
with open('engine/config.json') as conf_file: # load JSON config file
    configGlobal = json.load(conf_file)
    texts = configGlobal['demo']

header = st.header(texts['header_1'])
header_text = st.write(texts['intro_1'])

if st.sidebar.checkbox("Press to Begin"):
    st.write(st.__version__)
    st.write(st.__version__)
    header_text = st.empty()