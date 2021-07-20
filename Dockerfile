# # FROMで指定したDockerイメージをベースに、これから記述するコマンドを実施します
# FROM python:3.8
# # コンテナ内の環境変数
# ENV PYTHONUNBUFFERED 1
# # RUN: Dockerイメージを作成する際にコンテナ内でコマンドを実行する命令
# # ルートディレクトリの下にcodeというディレクトリを作成
# RUN mkdir /code
# # 作業ディレクトリを設定
# WORKDIR /code
# # COPY HOST GUEST. 指定したファイル・ディレクトリをコンテナ内にコピー
# COPY requirements.txt /code/
# # -r: read
# RUN pip install -r requirements.txt 
# COPY . /code/

FROM python:3.8

RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

COPY . /opt/services/djangoapp/src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8000