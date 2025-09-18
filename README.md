# ChatBot-EITO

**Django-based Chatbot for Pre-Interview Simulation**

## 🧠 Overview

ChatBot-EITO is a Django application that simulates conversations between chatbot instances to determine users' food preferences and whether they are vegetarian or vegan. This project was created as a demo for a pre-interview assignment.

## ✨ Key Features

### Simulated Chat Conversations
- ChatGPT A asks for three favorite foods.
- ChatGPT B responds with dynamic/randomized answers.
- A third ChatGPT instance analyzes the responses to determine if the user is vegetarian or vegan.
- A 30% probability is used to simulate vegan responses for variability.

### Django REST API
- Provides an endpoint to retrieve users classified as vegetarian or vegan.
- Basic authentication is implemented for demonstration purposes.

### OpenAI Integration
- Uses ChatGPT 3.5 to generate realistic responses while keeping costs low.

### Frontend Demo
- Basic HTML/CSS/JS interface for chatting with the bot.
- Designed for simplicity and demonstration.

### Secure Environment
- All sensitive information (API keys, secrets) is stored in a `.env` file and excluded from the repository.

## 📁 Project Structure

```
ChatBot-EITO/
│
├─ app/                   # Django app
├─ project/               # Django project settings
├─ static/                # Static files (CSS, JS)
├─ templates/             # HTML templates
├─ Dockerfile             # Docker configuration
├─ docker-compose.yml     # Docker Compose setup
├─ requirements.txt       # Python dependencies
├─ .env.example           # Example environment variables
└─ README.md
```

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- OpenAI API key (stored in `.env`)
- Django 4.x and DRF installed via `requirements.txt`

### Running Locally

Clone the repository:

```bash
git clone https://github.com/<your-username>/ChatBot-EITO.git
cd ChatBot-EITO
```

Copy `.env.example` to `.env` and add your secrets:

```bash
cp .env.example .env
```

Build and run the Docker containers:

```bash
docker-compose up --build
```

Access the app:

- Frontend: [http://localhost:8000/](http://localhost:8000/)
- API: [http://localhost:8000/api/vegans/](http://localhost:8000/api/vegans/) *(requires authentication)*

## ☁️ Deployment on Azure (Optional)

Push your Docker image to Docker Hub:

```bash
docker build -t <dockerhub-username>/chatbot-eito:latest .
docker push <dockerhub-username>/chatbot-eito:latest
```

Create an Azure Web App (Linux, Docker) and configure it to pull your image.

Add your environment variables (`OPENAI_API_KEY`, `DJANGO_SECRET_KEY`, etc.) in Azure App Settings.

Visit your Azure Web App URL to see the live application.

## 📝 Notes / Design Decisions

- A third ChatGPT instance is used to determine vegan/vegetarian status because the assignment didn’t specify classification logic.
- Basic authentication is implemented for demo purposes only.
- The frontend interface is simple; for production it should be separated and optimized.
- ChatGPT 3.5 is chosen to reduce API costs while maintaining realistic behavior.
- Azure deployment was slightly delayed due to initial configuration challenges.

## 🔐 Credentials (Demo)

- Admin: `admin` / `admin123`
- User: `user` / `user123`
- API Endpoint: `/api/vegans/` *(requires authentication)*

## 🎯 Bonus / Future Improvements

- Separate HTML, CSS, and JS for a cleaner frontend.
- Implement more interactive chat features.
- Add richer statistics or dashboards for simulated users.
