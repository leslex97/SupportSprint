# Wybór obrazu python 3.11.2
FROM python:3.11.2
# Ustawienie katalogu roboczego
WORKDIR /usr/src/app
#Wyłączenie buforowania 
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONNUNBUFFERED 1
#aktualizacja pip
RUN pip install --upgrade pip
# instalacja zleżności
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#kopiowanie do kontenera
COPY . .