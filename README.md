---
title: OpenPronounce Engine
emoji: 🎤
colorFrom: blue
colorTo: cyan
sdk: docker
app_port: 7860
pinned: false
---

# OpenPronounce Engine (for Oxford 5000 Pronunciation Lab)

Self-hosted OpenPronounce (Wav2Vec2 + DTW + phone model) used by the GAS web app.
Exposes `POST /pronunciation` and `GET /health`.

Optional env var: `OPENPRONOUNCE_API_KEY` — if set, requests must send `X-Api-Key`.
