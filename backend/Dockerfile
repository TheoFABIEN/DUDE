FROM python:3.13

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl \
    libglib2.0-0 libgl1 libglx-mesa0 libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN python3 -m pip install --no-cache-dir --root-user-action=ignore --upgrade pip setuptools wheel

COPY requirements.txt ./requirements.txt

RUN python3 -m pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

COPY . .

ENV TORCH_FORCE_WEIGHTS_ONLY_LOAD=0

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
