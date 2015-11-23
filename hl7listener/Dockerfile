FROM python:3
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "python", "./server.py" ]
