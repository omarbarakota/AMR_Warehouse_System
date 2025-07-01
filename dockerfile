#Python version
FROM python:3.13-slim

WORKDIR /app

# Create the instance directory and set permissions
RUN mkdir -p /app/instance

#copy and install all dependencies

COPY requirments.txt ./

RUN pip install --no-cache-dir -r requirments.txt

COPY ./ ./

# Creating a user to run app not the root user
RUN useradd app

RUN chown -R app:app /app

#Expose app needed port
EXPOSE 8000

USER app

#Start the app and allow connections on all interfaces
ENTRYPOINT [ "gunicorn","-w 1","-b 0.0.0.0:8000","wsgi" ]

#for any further commands
#CMD [ "executable" ]
