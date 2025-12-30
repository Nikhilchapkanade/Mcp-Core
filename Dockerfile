FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD ["uvicorn", "main:mcp.handle_sse", "--host", "0.0.0.0", "--port", "8000"]