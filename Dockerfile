FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install python3.10 curl cron && \
    apt update && apt install python3-pip -y

# Method1 - installing LibreOffice and java
RUN apt-get --no-install-recommends install libreoffice -y
RUN apt-get install -y libreoffice-java-common

# Method2 - additionally installing unoconv
RUN apt-get install unoconv

ARG CACHEBUST=1


WORKDIR /app
COPY . .
RUN pip install -r /app/requirements.txt
RUN chmod +x download-document.sh
RUN chmod +x start-document.sh
RUN chmod +x restart-document.sh

# Copy hello-cron file to the cron.d directory
COPY document-cron /etc/cron.d/document-cron
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/document-cron

# Apply cron job
RUN crontab /etc/cron.d/document-cron
 
# Create the log file to be able to run tail
RUN touch /var/log/cron.log
CMD ./start-document.sh & cron && tail -f /var/log/cron.log