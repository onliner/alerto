# 🚨 Graylog → Telegram Alerts

A lightweight webhook service that receives alert payloads from Graylog,  
formats them into structured Telegram messages, and sends them via the Telegram Bot API.  
It respects API rate limits and is easy to configure and deploy with Docker.

[![Python][python-badge]][python-link]
[![Docker][docker-badge]][docker-link]
[![License][license-badge]][license-link]

---

## 🧑‍💻 Run Locally

### 1. Clone the repository

```bash
git clone git@github.com:onlinerby/alerto.git
cd alerto
```

### 2. Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install requirements

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### 4. Configure environment

Create a local `.env` file:

```bash
cp .env.example .env
```

Then edit it and set the following variables:

- `AUTH_TOKEN` — Bearer token required for incoming webhook requests
- `GRAYLOG_URL` — Web URL of the Graylog dashboard (admin panel)
- `TELEGRAM_TOKEN` — API token from [@BotFather](https://t.me/botfather)
- `CHAT_ID` — ID of the chat where bug reports should be delivered
- `MAX_MESSAGES_PER_MINUTE` — Telegram rate limit (messages per minute)

> [!TIP]  
> If `AUTH_TOKEN` is not set, authentication is disabled, and anyone can POST alerts to your endpoint.  
> **For production, it’s strongly recommended to define a secure token.**

> [!CAUTION]  
> **Keep your tokens and API keys safe** — they grant full control over your bot.

### 5. Start the service (development)

```
python app.py
```

This command starts the built-in aiohttp development server.  
By default, it listens on http://localhost:8080.

## 🐳 Run in Docker

### 1. Clone the repository

```bash
git clone git@github.com:onlinerby/alerto.git
cd alerto
```

### 2. Configure environment

```bash
cp .env.example .env  
# Fill in your TELEGRAM_TOKEN, CHAT_ID, and optionally AUTH_TOKEN
```

### 3. Build and run the container

```bash
docker build -t alerto .
docker run --rm -p 8080:8080 --env-file .env alerto
```

> [!NOTE]  
> To create a bot and get your API token, message [@BotFather](https://t.me/botfather) and follow the instructions:    
> [**Telegram Bot Guide →**](https://core.telegram.org/bots#6-botfather)

## 🧾 Graylog Test Event

An example payload is available in [graylog.json](graylog.json).  
You can use it to test the service locally:

```bash
curl -X POST http://localhost:8080 \
     -H "Authorization: Bearer <auth token>" \
     --data @graylog.json
```

## 🧩 Integration Guide

For a full setup walkthrough — including Graylog stream, pipeline, and event definition —
see the detailed documentation:  
 [**Integration Guide →**](docs/graylog.md)

## 📜 License

Released under the [MIT License](LICENSE).


[python-badge]: https://img.shields.io/badge/python-3.9+-brightgreen.svg
[python-link]: https://www.python.org
[docker-badge]: https://img.shields.io/badge/docker-ready-blue
[docker-link]: https://www.docker.com
[license-badge]: https://img.shields.io/badge/license-MIT-green  
[license-link]: LICENSE
