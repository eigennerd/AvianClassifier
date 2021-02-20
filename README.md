# AvianClassifier
Yet another Streamlit app to help identify birds by their song


### HOW TO ###

1. Run the app locally:
Use Docker. Docker allows running the app in a standardized isolated environment on your local machine or deployed on cloud


 - Make sure [Docker](https://docs.docker.com/desktop/) is installed and running
 - Ensure [GIT](https://git-scm.com/download/mac) is installed and running
 - navigate to any folder in Terminal
 - to clone the repository - ```git clone https://github.com/eigennerd/AvianClassifier.git```
 - navigate to the folder - ```cd AvianClassifier```  
 - to build the container - ```docker build -t avianclassifier .``` wait until the build is complete
 - to run the app  - ```docker run -p 8501:8501 avianclassifier```
 - Open your [browser](http://localhost:8501/) @ localhost:8501

2. [Observe the app Online](https://share.streamlit.io/eigennerd/avianclassifier/main/main.py)


### DISCLAIMER ###

The app is inspired by the model found on the Kaggle competition page:
 - https://www.kaggle.com/frlemarchand/bird-song-classification-using-an-efficientnet

And the TDS page by WiMLDS
- https://towardsdatascience.com/sound-based-bird-classification-965d0ecacb2b

