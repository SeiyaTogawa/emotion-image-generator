# ベースイメージとして公式のPythonイメージを使用
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# `requirements.txt` をコピーして依存関係をインストール
COPY  ./ ./
RUN pip install --upgrade pip
RUN pip install -r main/requirements.txt

# アプリケーションのコードをコピー
#COPY main/miraihon_streamlit.py ./


EXPOSE 80

# アプリケーションの起動コマンド
CMD ["streamlit", "run", "main/emo_img_streamlit.py"]
