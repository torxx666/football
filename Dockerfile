FROM python:3.10.2
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./ /app
WORKDIR /app


RUN apt update
RUN apt install -y libc-dev

RUN apt-get install -y gcc  libgeos-dev   python3-dev 

COPY requirements.txt ./

RUN python -m pip install -U --force-reinstall pip

RUN pip install  -r requirements.txt
