FROM nvcr.io/nvidia/pytorch:23.10-py3

RUN apt update

ENV DEBIAN_FRONTEND=noninteractive
RUN apt install -y ffmpeg python3-tk netcat

RUN pip install ttkthemes ttkwidgets yt_dlp