FROM python:3.8
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt \
 && apt-get update \
 && apt-get upgrade -y \
 && apt-get install libsndfile1 -y \
 && apt-get install ffmpeg -y
RUN pip install tensorflow --no-cache-dir
COPY . /app
WORKDIR /app
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
