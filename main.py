import streamlit as st
from engine.read_data import *
from engine.model import *
import os
from PIL import Image

####
## CONFIG BLOCK
####

local_css("engine/style.css")

lang = st.sidebar.radio(label='Language options:', options=['en', 'ua', 'ru', 'pl'], key='1')
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# config.json has page content
with open('engine/config.json') as conf_file:  # load JSON config file
    configGlobal = json.load(conf_file)
    texts = configGlobal['demo']
# declare placeholders
header = st.empty()  # placeholder for 1st header
header_text = st.empty()  # placeholder for 1st textbox
show_bird_1 = st.empty()  # this will show prediction picture     (bird_1)
show_bird_2 = st.empty()  # this will show 2nd prediction picture (bird_2)
show_bird_3 = st.empty()  # this will show 3rd prediction picture (bird_3)
# declare headers
header.header(texts['header_1'])
header_text.write(texts['intro_1'])
test_dir = os.path.join(  # todo: change this
    os.path.dirname(os.path.realpath(__file__)),  # where am i?
    'test_audio')

audiofiles = get_audio_files_in_dir(test_dir)

####
## SIDEBAR DEMO FILES BLOCK
####
if len(audiofiles) == 0:
    st.write("Put some audio files in your test directory (%s) to activate this player." % test_dir)
else:
    filename = st.sidebar.selectbox("Select mp3 from test directory (%s)" % test_dir, audiofiles, 0)
    audiopath = os.path.join(test_dir, filename)

#####
## SIDEBAR UPLOAD BLOCK
#####
uploaded = st.sidebar.file_uploader('Upload mp3')  # supposed to be an mp3 uploaded file
if uploaded:
    audiopath = handle_uploaded(uploaded)

#####
## MAINBAR INIT BLOCK
#####
if os.path.exists(audiopath):
    st.sidebar.audio(audiopath)
    table_of_predictions, spectrogram, bird_url, bird_scientific_name = read_mp3(audiopath)

    if 'test_audio' in audiopath:
        for idx, row in table_of_predictions.nlargest(5, columns='probability').reset_index().iterrows():
            if compare(f"{row.gen} {row.sp}", audiopath):
                idx=idx+1
                predicted_name = f"{row.gen} {row.sp}"
                break
            else:
                idx=0

        if idx>0:
            pred_msg = f'<div> <span class="highlight blue">Correct name: {get_vernacular(predicted_name)} was guessed as top-{idx} </span></div>'
        else:
            pred_msg = f"<div> <span class='highlight red'>AI did not guess the birb: {birds_df[birds_df['ind'] == int(audiopath.split('.')[0][-2:])]['en'].values[0]}</span></div>"
    else:
        pred_msg = '<div> <span class="highlight blue">AI does not know the Ground Truth of uploaded files </span></div>'

    col1, col2, col3 = st.beta_columns([1, 1, 2])  # names and translation
    col1.write(f"Top guess: [{bird_scientific_name}](http://en.wikipedia.org/wiki/{re.sub(' ', '_', bird_scientific_name)})")
    col2.write(
        f"[{get_vernacular(bird_scientific_name, lang=lang)}](http://{lang}.wikipedia.org/wiki/{re.sub(' ', '_', bird_scientific_name)})")

    col1.image(bird_url, width=400)
    col3.subheader('Top 5 guesses:')
    col3.write(table_of_predictions[['en', 'probability']]. \
               nlargest(5, columns='probability'). \
               style.format({"probability": '{:,.2%}'.format})
               )
    col3.markdown(pred_msg, unsafe_allow_html=True)

    with st.beta_expander('Spectrogram', False):
        st.image(Image.fromarray(np.rot90(spectrogram)), use_column_width=True)

    with st.beta_expander('map', False):
        try:
            map_pydeck = form_pydeck(audiopath)  # requires fixing (test_csv updated)
            st.pydeck_chart(map_pydeck)
        except:
            pass



