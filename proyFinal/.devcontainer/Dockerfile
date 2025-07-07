FROM python:3.13

RUN useradd -ms /bin/bash vscode

# Lugar donde va a vivir el código
WORKDIR /workspace

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .