# AvianClassifier
Yet another Streamlit app to help identify birds by their song


### HOW TO ###

1. Run the app locally:
Use Docker. Docker allows running the app in a standardized isolated environment on your local machine or deployed on cloud


 - make sure [Docker](https://docs.docker.com/desktop/) is installed and running
 - make sure [GIT](https://git-scm.com/download/mac) is installed and running
 - navigate to any folder in Terminal
 - clone the repository - ```git clone https://github.com/eigennerd/AvianClassifier.git```
 - navigate to the folder - ```cd AvianClassifier```  
 - build the container - ```docker build -t avianclassifier .``` Mind the . dot at the end! wait until the build is complete.
 - run the app  - ```docker run -p 8501:8501 avianclassifier```
 - Open your [browser](http://localhost:8501/) @ localhost:8501

Don't forget to turn off the container after no longer in use. Use the Docker UI or via Terminal:  
 - ```docker ps -a``` to see all containers  
 - ```docker kill <<<id>>>``` to kill the working container
 - ```docker rm <<<id>>>``` to remove the container

2. [Observe the app Online](https://share.streamlit.io/eigennerd/avianclassifier/main/main.py). <- Follow the link


### DISCLAIMER ###

The app is inspired by the model found on the Kaggle competition page:
 - https://www.kaggle.com/frlemarchand/bird-song-classification-using-an-efficientnet

And the TDS page by WiMLDS
- https://towardsdatascience.com/sound-based-bird-classification-965d0ecacb2b

