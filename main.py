import streamlit as st
st.set_page_config(layout='wide')
from engine.config import *
from engine.read_data import *
from engine.model import *
import os
from PIL import Image

####
## CONFIG BLOCK
####

local_css("engine/style.css")

lang = st.sidebar.radio(label='Language options:', options=['en', 'uk', 'ru', 'pl'], key='1')
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

texts = config_json()[lang]
# declare placeholders
header = st.empty()  # placeholder for 1st header
header_text = st.empty()  # placeholder for 1st textbox
show_bird_1 = st.empty()  # this will show prediction picture     (bird_1)
show_bird_2 = st.empty()  # this will show 2nd prediction picture (bird_2)
show_bird_3 = st.empty()  # this will show 3rd prediction picture (bird_3)
# declare headers
header.header(texts['header_1'])
header_text.markdown(texts['intro_1'])
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
    filename = st.sidebar.selectbox(texts['select_mp3'], audiofiles, 0)
    audiopath = os.path.join(test_dir, filename)

#####
## SIDEBAR UPLOAD BLOCK
#####
uploaded = st.sidebar.file_uploader(texts['upload_mp3'])  # supposed to be an mp3 uploaded file
if uploaded:
    audiopath = handle_uploaded(uploaded)

#####
## MAINBAR INIT BLOCK
#####
if os.path.exists(audiopath):
    header_text.empty()
    st.sidebar.audio(audiopath)
    table_of_predictions, spectrogram, bird_url, bird_scientific_name, preds, credit = read_mp3(audiopath)
    idx=0

    if 'test_audio' in audiopath:
        for idx, row in table_of_predictions.nlargest(5, columns='certainty').reset_index().iterrows():
            if compare(f"{row.gen} {row.sp}", audiopath):
                idx+=1
                predicted_name = f"{row.gen} {row.sp}"
                break
            else:
                idx=0

        if idx==1:
            pred_msg = f"<div> <span class='highlight blue'>{texts['success_msg']} {get_vernacular(predicted_name, lang=lang)} ! </span></div>"
        else:
            pred_msg = f"<div> <span class='highlight red'>{texts['not_guessed_msg']} {birds_df[birds_df['ind'] == int(audiopath.split('.')[0][-2:])]['en'].values[0]}</span></div>"
    else:
            pred_msg = f"<div> <span class='highlight blue'>{texts['uploaded_msg']}</span></div>"

    col1, col2, col3 = st.beta_columns([1, 1, 2])  # names and translation
    with col1:
        st.write(f"{texts['top_guess']} [{bird_scientific_name}](http://en.wikipedia.org/wiki/{re.sub(' ', '_', bird_scientific_name)})")
        st.image(bird_url, width=400)
        st.write(f'(c) Photo Credit: {credit}')

    with col2:
        st.write(
              f"[{get_vernacular(bird_scientific_name, lang=lang)}](http://{lang}.wikipedia.org/wiki/{re.sub(' ', '_', bird_scientific_name)})")

    with col3:
        st.markdown(pred_msg, unsafe_allow_html=True)
        st.subheader('Top 5 guesses:')
        st.write(table_of_predictions[['en', 'certainty']]. \
                   nlargest(5, columns='certainty'). \
                   style.format({"certainty": '{:,.2%}'.format})
                   )
        if max(table_of_predictions['certainty'])<0.05:
            st.markdown(f"""<span class='small-font'>{texts['low_certainty_msg']}</span>""", unsafe_allow_html=True)


    with st.sidebar.beta_expander('Download By-Frame Prediction'):
        st.markdown(download_data(
                                    pd.DataFrame(preds,
                                                 columns=sorted(table_of_predictions.gen +' '+ table_of_predictions.sp))),
                    unsafe_allow_html=True)

    with st.beta_expander('Spectrogram', False):
        st.image(Image.fromarray(np.rot90(spectrogram)), use_column_width=True)

    with st.beta_expander('Historical Sightings', False):
        try:
            map_pydeck = form_pydeck(audiopath)  # requires fixing (test_csv updated)
            st.pydeck_chart(map_pydeck)
        except:
            pass
#


