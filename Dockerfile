FROM python:3.8
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
WORKDIR /app
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install libsndfile1 -y
RUN apt-get install ffmpeg -y
#&& apt-get -y install c \
COPY . /app
CMD streamlit run ./main.py
EXPOSE 8501
