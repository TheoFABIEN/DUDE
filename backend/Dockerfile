FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git python3.11 python3.11-dev python3-pip build-essential \
    libglib2.0-0 libgl1-mesa-glx libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

WORKDIR /workspace

RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    python3 -m pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu118 && \
    python3 -m pip install --no-cache-dir fastapi[all] pillow

RUN git clone https://github.com/darsa-group/flat-bug.git /flat-bug && \
    python3 -m pip install --no-cache-dir -e /flat-bug

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]