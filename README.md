# ChatBot-EITR

**Django Chatbot Deployed on Azure for Pre-Interview Simulation**

## 🧠 Overview

ChatBot-EITR is a Django application deployed on **Azure App Service**, simulating chatbot conversations to determine users’ food preferences and whether they are vegetarian or vegan. All endpoints and features are accessible via the live Azure URL.

**Live App URL:** [https://eito-chatbot.azurewebsites.net](https://eito-chatbot-fnfjhyhtcwd4a2gx.westeurope-01.azurewebsites.net)

## ✨ Key Features

### Simulated Chat Conversations
- ChatGPT A asks users for their three favorite foods.
- ChatGPT B responds with dynamic/randomized answers.
- A third ChatGPT instance analyzes the responses to classify users as vegetarian or vegan.
- 30% probability is applied for vegan responses to introduce variability.

### Django REST API
All endpoints are accessible from Azure and protected with **Basic Authentication** (demo credentials only – must be changed in production):

- **`/api/vegans/`**: Retrieves users classified as vegetarian or vegan. *(Requires authentication)*
- **`/api/simulate/`**: Run a new simulation of users and their responses.
- **`/api/statistics/`**: Aggregated statistics showing veg vs non-veg counts and top foods.
- **`/api/chat/`**: Real-time chat endpoint powered by OpenAI GPT-3.5.

### Frontend
- Basic HTML/CSS/JS interface for interacting with the chat API.
- Dashboard page shows simulation results in a simple interface.
- Separate pages for Home, Chat, and Dashboard.

### Security (Demo)
- All secrets, including `OPENAI_API_KEY` and `DJANGO_SECRET_KEY`, are stored securely in Azure App Settings.
- API endpoints are protected via **Basic Authentication** or Django login.
- Demo credentials (must be changed for a real production proyect):
  - Admin: `admin` / `admin123`
  - User: `user` / `user123`

### OpenAI Integration
- Uses ChatGPT 3.5 to generate realistic chat responses.
- API usage optimized to reduce costs.

## 📁 Project Structure (Relevant for Azure Deployment)

ChatBot-EITR/
│
├─ app/ # Django app: views, models, serializers, API endpoints
├─ templates/ # HTML templates
├─ project/ # Django project settings
├─ Dockerfile # Docker image built and deployed on Azure
├─ entrypoint.sh # Entrypoint for migrations, user creation, and starting Gunicorn
├─ requirements.txt # Python dependencies
└─ README.md


## ☁️ Azure Deployment

1. Docker image pushed to Docker Hub:

```bash
docker build -t <dockerhub-username>/chatbot-eito:latest .
docker tag chatbot-eito:latest <dockerhub-username>/chatbot-eito:latest
docker push <dockerhub-username>/chatbot-eito:latest
```

## ☁️ Azure Web App Configuration

- Azure Web App (Linux, Docker) created and configured to pull the image.

### 🔧 Environment Variables (Azure App Settings)

```env
OPENAI_API_KEY
DJANGO_SECRET_KEY
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
```
## 🚀 App Launch & Setup

App started successfully at [https://eito-chatbot.azurewebsites.net](https://eito-chatbot-fnfjhyhtcwd4a2gx.westeurope-01.azurewebsites.net)

> ℹ️ **Note:** The app automatically runs migrations and creates demo users on startup via `entrypoint.sh`.

## 🎯 New Functionalities / Updates

- **Statistics API**: `/api/statistics/` – Shows veg vs non-veg counts and most popular foods.
- **Simulation API**: `/api/simulate/` – Generate simulated users dynamically.
- **Chat API**: `/api/chat/` – Interact with the bot using OpenAI GPT-3.5.
- **Authentication-secured endpoints**: Ensures demo credentials are required to access sensitive data.
- **Frontend updated** with separate pages for dashboard, chat, and home.

## 🔐 Security Disclaimer

- All credentials are for demo purposes only.
- Must change admin/user passwords and API keys in production deployments.
- `.env` files are never committed; all secrets are stored securely in Azure App Settings.

## 💡 Notes

- Designed for Azure-first deployment, no local setup required.
- Docker-based deployment ensures consistency across environments.
- ChatGPT classification logic is simplified for demonstration purposes.
- Frontend is minimal; can be enhanced with separate HTML, CSS, and JS for production dashboards.
