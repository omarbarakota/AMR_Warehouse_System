#Python version
FROM python:3.13-slim

WORKDIR /app

#copy and install all dependencies

COPY requirments.txt ./

RUN pip install --no-cache-dir -r requirments.txt

COPY ./ ./

#Expose app needed port
EXPOSE 8000

# Creating a user to run app not the root user
RUN useradd app
USER app

ENV MQTT_BROKER=host.docker.internal
ENV MQTT_PORT=1883

#Start the app and allow connections on all interfaces
ENTRYPOINT [ "gunicorn","-w 1","-b 0.0.0.0:8000","wsgi" ]

#for any further commands
#CMD [ "executable" ]
