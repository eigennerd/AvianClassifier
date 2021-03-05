FROM python:3.8
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt \
 && apt-get update \
 && apt-get upgrade -y \
 && apt-get install libsndfile1 -y \
 && apt-get install ffmpeg -y
WORKDIR /app
COPY . /app
CMD streamlit run ./main.py
EXPOSE 8501
