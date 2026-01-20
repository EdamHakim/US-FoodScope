---
title: US FoodScope Inference API
emoji: 🥗
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# US FoodScope Inference API

This is a FastAPI-based inference server for the US FoodScope project. It provides endpoints for health risk prediction and a Retrieval-Augmented Generation (RAG) assistant focused on U.S. food environment data.

## Features

- **Health Prediction**: Predicts obesity and diabetes risk based on demographic and food environment features.
- **RAG Assistant**: Answer questions about food access, health outcomes, and socioeconomic factors using grounded U.S. county data.
- **Clustering Data**: Serve high-risk county clustering data for visualization.

## Endpoints

- `GET /`: Health check and status.
- `GET /clustering-data`: Returns high-risk county records.
- `POST /predict`: Predicts health outcomes.
- `POST /ask`: Queries the RAG assistant (requires `GROQ_API_KEY`).

## Deployment

This Space is configured to run via Docker. Ensure all ML artifacts (`.joblib`, `encoders/`) and RAG assets (`faiss_index.bin`, `chunks.pkl`) are included in the repository.

### Environment Variables

- `GROQ_API_KEY`: Required for the `/ask` endpoint to function.
