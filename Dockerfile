FROM python:3.9.16-slim

WORKDIR /opt/app-root/src

COPY requirements.txt /opt/app-root/src/

## NOTE - rhel enforces user container permissions stronger ##
USER root

RUN pip3 install --upgrade pip==21.3.1

RUN pip3 install -r requirements.txt

USER 1001

COPY . /opt/app-root/src
ENV FLASK_APP=app
ENV PORT 3000

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]