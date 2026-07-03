# syntax=docker/dockerfile:1
FROM python:3.11-slim
RUN pip install --no-cache-dir 'litellm[proxy]' uvicorn
COPY proxy_config.yaml /app/proxy_config.yaml
EXPOSE 4000
CMD ["litellm", "--config", "/app/proxy_config.yaml", "--port", "1317"]
