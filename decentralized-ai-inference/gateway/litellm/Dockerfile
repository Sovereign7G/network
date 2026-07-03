FROM ghcr.io/berriai/litellm:main-latest
COPY proxy_config.yaml /app/proxy_config.yaml
ENV DATABASE_URL=sqlite:///litellm.db
CMD ["litellm", "--config", "/app/proxy_config.yaml", "--port", "1317"]
