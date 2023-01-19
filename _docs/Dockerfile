FROM ubuntu:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-venv \
    python3-pip \
    python3-dev \
    wget \
    git \
    build-essential \
    cmake

WORKDIR /venv/

RUN python3 -m venv .env && \
    /bin/bash -c "source .env/bin/activate && \
        pip install --upgrade pip && \
        pip install lazydocs flake8 \
            build setuptools \
            cffi pytest pytest-cov \
            datestamp cmake_build_extension"

WORKDIR /workspace/