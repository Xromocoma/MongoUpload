FROM python:latest
ENV DEBIAN_FRONTEND="noninteractive"

ENV PYTHONPATH=.
RUN apt-get install -y git \
    && mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan bitbucket.org > /root/.ssh/known_hosts

RUN echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa
WORKDIR /code
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code

CMD ["python", "main.py"]