FROM ghcr.io/berriai/litellm:main

# Remove default configs that ship with the image
RUN rm -f /app/config.yaml /app/config.template.yaml 2>/dev/null; \
    rm -f /litellm/proxy/config.yaml 2>/dev/null; \
    rm -f /usr/local/lib/python3.9/site-packages/litellm/proxy/config.yaml 2>/dev/null || true

COPY proxy_config.yaml /app/proxy_config.yaml

# Tell litellm where our config is
ENV LITELLM_CONFIG_PATH=/app/proxy_config.yaml

EXPOSE 4000
CMD ["litellm", "--config", "/app/proxy_config.yaml", "--port", "4000"]
