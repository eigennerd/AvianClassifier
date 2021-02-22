import numpy as np
import pandas as pd
from scipy.special import logit
import streamlit as st
import plotly.express as px

def plot_timeline(df):
    '''
    :param result: preds dataframe
    :return: rendered plotly object
    '''


    def log_odds(set_of_predictions):
        return 1 / (1 + np.exp(-(logit(set_of_predictions)).mean(axis=0)))

    df = df. \
        rolling(3, center=True, closed='both', min_periods=1). \
        apply(log_odds). \
        assign(FrameSec=lambda x: 5*x.index). \
        melt(id_vars=['FrameSec'], var_name='sp', value_name='logit')

    df['FrameSec'] = df.FrameSec.apply(lambda x: pd.to_datetime(x, unit='s').strftime("%H:%M:%S"))

    fig = px.line(df
              , x="FrameSec"
              , y="logit"
              , color="sp"
              , hover_name="sp"
              , labels={
                     "logit": "Probability (Log Odds)",
                     "FrameSec": "Time",
                     "sp": "Species"
                 }
              , title="")
    fig.add_shape(type='line',
                  x0=min(df.FrameSec),
                  y0=0.8,
                  x1=max(df.FrameSec),
                  y1=0.8,
                  line=dict(color='Red', dash='dash'),
                  opacity=0.6
                )
    fig.update_layout(showlegend=False, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

