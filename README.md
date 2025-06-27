# D&D 5e API Wrapper

Projeto em Python + FastAPI que consome a API pública do D&D 5e (https://www.dnd5eapi.co/)  
Armazena os dados em MongoDB e fornece uma API local.

## Requisitos

- Python 3.11+
- FastAPI
- MongoDB local
- httpx
- motor (MongoDB async driver)

## Rodando localmente

```bash
uvicorn app.main:app --reload
