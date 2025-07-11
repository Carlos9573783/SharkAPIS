from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import asyncio
from telegram import Bot
import os

# ========== CONFIG ==========
TOKEN = "8056037997:AAEHBdeTwOPHLUImNLibxCG6dvb9YD8XmQU"
GRUPO_DESTINO = "@DBSPUXADASVIP"
CAMINHO_PERMISSOES = "permissoes.json"
bot = Bot(token=TOKEN)
# ============================

app = FastAPI()

# Modelo de entrada
class Consulta(BaseModel):
    user_id: int
    tipo: str  # cpf, telefone, placa, etc
    valor: str

# Carrega JSON com permissões
def carregar_permissoes():
    if not os.path.exists(CAMINHO_PERMISSOES):
        return {}
    with open(CAMINHO_PERMISSOES, "r", encoding="utf-8") as f:
        return json.load(f)

# Aguarda resposta no grupo (por padrão 30s)
async def aguardar_resposta(mensagem_id, timeout=30):
    for _ in range(timeout * 2):
        await asyncio.sleep(0.5)
        mensagens = await bot.get_chat(GRUPO_DESTINO).get_history(limit=3)
        for m in mensagens:
            if m.reply_to_message and m.reply_to_message.message_id == mensagem_id:
                return m.text
    return None

# Rota raiz
@app.get("/")
def home():
    return {"mensagem": "🦈 API SharkBuscas online!"}

# Rota de consulta
@app.post("/consultar")
async def consultar(dados: Consulta):
    permissoes = carregar_permissoes()
    user = str(dados.user_id)

    if user not in permissoes:
        raise HTTPException(status_code=403, detail="Usuário sem permissão")

    if dados.tipo not in permissoes[user]:
        raise HTTPException(status_code=403, detail=f"Você não tem permissão para consultar '{dados.tipo}'")

    comando = f"/{dados.tipo} {dados.valor}"
    mensagem = await bot.send_message(GRUPO_DESTINO, comando)

    resposta = await aguardar_resposta(mensagem.message_id)

    if resposta:
        return {"status": "ok", "resposta": resposta}
    else:
        raise HTTPException(status_code=504, detail="Tempo de resposta esgotado")
