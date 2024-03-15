FROM python:3.10

WORKDIR /service
COPY requirements.txt ./

# Встановлення необхідних пакетів
RUN apt-get update && \
    apt-get install -y \
    wget \
    ca-certificates \
    fonts-noto \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
    xdg-utils \
    gnupg

# Завантаження та встановлення Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Встановлення шляху до виконуваного файлу Google Chrome
ENV CHROME_BIN=/usr/bin/google-chrome-stable

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
