FROM python:3.11-slim

# Обновляем сертификаты
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && update-ca-certificates

WORKDIR /app
COPY requirements.txt .

# Устанавливаем ВСЕ пакеты ТОЛЬКО через зеркало (без pypi.org!)
RUN pip install --no-cache-dir \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    --default-timeout=300 \
    -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "demo/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
