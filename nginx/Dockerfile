# wybór obrazu nginx
FROM nginx:1.25.3
#aktualizacja pakietu
RUN apt-get update && apt-get install -y procps
#tworzenie katalogu dla plików statycznych
RUN mkdir -p /home/app/staticfiles