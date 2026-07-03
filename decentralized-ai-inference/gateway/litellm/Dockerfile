FROM python:3.11-slim
WORKDIR /app
COPY billing.py s7g_client.py proxy.py setup_gateway.py ./
RUN pip install --no-cache-dir fastapi uvicorn httpx
RUN python setup_gateway.py
CMD ["uvicorn", "proxy:app", "--host", "0.0.0.0", "--port", "1317"]
