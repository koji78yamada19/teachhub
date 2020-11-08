FROM python:3.8
ENV PYTHONUNBUFFERED 1
# RUN: コマンドを実行。ルートディレクトリの下にcodeというディレクトリを作成
RUN mkdir /code 
WORKDIR /code
# COPY HOST GUEST. 指定したファイル・ディレクトリをコンテナ内にコピー
COPY requirements.txt /code/
# -r: read
RUN pip install -r requirements.txt 
COPY . /code/