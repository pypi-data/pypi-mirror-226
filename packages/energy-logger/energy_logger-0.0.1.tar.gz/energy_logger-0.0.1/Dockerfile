FROM python:3.11-slim-bookworm
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN python3 -m pip install energy-logger

EXPOSE 5000

CMD ["python3", "-m", "energy-logger"]

