FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir litellm
COPY proxy_config.yaml /app/proxy_config.yaml
CMD ["litellm", "--config", "/app/proxy_config.yaml", "--port", "1317"]
