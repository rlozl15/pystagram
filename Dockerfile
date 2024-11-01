FROM python:3.11
ENV PYTHONBUFFERED 1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip &&  \
    pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000