FROM python:3.13

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl \
    libglib2.0-0 libgl1 libglx-mesa0 libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    python3 -m pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu118 && \
    python3 -m pip install --no-cache-dir fastapi[all] pillow

RUN git clone https://github.com/darsa-group/flat-bug.git /flat-bug && \
    python3 -m pip install --no-cache-dir -e /flat-bug

RUN python3 -m pip install pybioclip==2.1.3

COPY . .

ENV TORCH_FORCE_WEIGHTS_ONLY_LOAD=0

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]