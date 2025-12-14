FROM python:3.13-slim

RUN pip install uv

WORKDIR /app

COPY . .

RUN uv sync

EXPOSE 8001

CMD [ "uv", "run", "fastapi", "run", "app/main.py", "--port", "8001" ]