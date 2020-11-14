# FROMで指定したDockerイメージをベースに、これから記述するコマンドを実施します
FROM python:3.8
# コンテナ内の環境変数
ENV PYTHONUNBUFFERED 1
# RUN: Dockerイメージを作成する際にコンテナ内でコマンドを実行する命令
# ルートディレクトリの下にcodeというディレクトリを作成
RUN mkdir /code
# 作業ディレクトリを設定
WORKDIR /code
# COPY HOST GUEST. 指定したファイル・ディレクトリをコンテナ内にコピー
COPY requirements.txt /code/
# -r: read
RUN pip install -r requirements.txt 
COPY . /code/