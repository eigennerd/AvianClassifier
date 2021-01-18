FROM python:3
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get -y install c
&& pip install -r requirements.txt
COPY . /app
CMD streamlit run ./main.py
EXPOSE 8501
