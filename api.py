from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Simula um "banco" de permissões, chave: user_id (int), valor: lista dos módulos liberados
# Você vai controlar quem pode consultar o quê aqui
permissoes = {
    1: ["cpf", "telefone", "nome", "cnpj", "placa"],  # usuário 1 pode tudo
    2: ["cpf", "telefone"],                            # usuário 2 pode só cpf e telefone
    # adicione outros conforme quiser
}

# Simula dados das consultas (em produção, você consultaria o grupo do Telegram ou banco real)
dados_cpf = {"12345678900": {"nome": "João Silva", "idade": 30}}
dados_telefone = {"11999999999": {"nome": "Maria Souza", "operadora": "Claro"}}

# Modelo para resposta das consultas
class ConsultaResponse(BaseModel):
    consulta: str
    resultado: Optional[dict]

# Rota raiz para teste
@app.get("/")
async def root():
    return {"mensagem": "🦈 API SharkBuscas Online!"}

# Endpoint para liberar permissões para usuário (simples, para teste)
@app.post("/liberar/")
async def liberar_consultas(user_id: int, modulos: List[str]):
    permissoes[user_id] = modulos
    return {"status": "ok", "user_id": user_id, "modulos_liberados": modulos}

# Endpoint para consultar CPF
@app.get("/cpf", response_model=ConsultaResponse)
async def consultar_cpf(user_id: int = Query(...), cpf: str = Query(...)):
    # Verifica se usuário tem permissão para cpf
    if user_id not in permissoes or "cpf" not in permissoes[user_id]:
        raise HTTPException(status_code=403, detail="Você não tem permissão para consultar CPF")

    resultado = dados_cpf.get(cpf)
    return ConsultaResponse(consulta=cpf, resultado=resultado)

# Endpoint para consultar Telefone
@app.get("/telefone", response_model=ConsultaResponse)
async def consultar_telefone(user_id: int = Query(...), telefone: str = Query(...)):
    # Verifica permissão para telefone
    if user_id not in permissoes or "telefone" not in permissoes[user_id]:
        raise HTTPException(status_code=403, detail="Você não tem permissão para consultar Telefone")

    resultado = dados_telefone.get(telefone)
    return ConsultaResponse(consulta=telefone, resultado=resultado)

# Você pode criar outras rotas como /nome, /cnpj, /placa, seguindo o mesmo padrão

# Endpoint painel para ver permissões atuais
@app.get("/painel/{user_id}")
async def painel(user_id: int):
    modulos = permissoes.get(user_id)
    if not modulos:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"user_id": user_id, "modulos_liberados": modulos}
