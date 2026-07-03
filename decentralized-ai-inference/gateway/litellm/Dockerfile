FROM python:3.11-slim
RUN echo "S7G-GATEWAY-v2"
COPY --chmod=644 billing.py s7g_client.py proxy.py setup_gateway.py /app/
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn httpx && python setup_gateway.py
CMD ["uvicorn", "proxy:app", "--host", "0.0.0.0", "--port", "1317"]
