FROM python:3.8-slim-buster
WORKDIR /workspace
COPY requirements.txt /workspace/requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 9000
ENV FLASK_DEBUG 1
COPY . .

CMD [ "flask", "run"]