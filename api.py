from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

# Simulação de usuários e permissões (em memória)
USUARIOS = {
    "user1": {"senha": "1234", "permissoes": ["cpf", "telefone", "nome"]},
    "user2": {"senha": "4321", "permissoes": ["cpf", "telefone", "nome", "cnpj", "placa"]},
    "user3": {"senha": "9999", "permissoes": ["cpf", "telefone", "nome", "cnpj", "placa", "endereco"]},
}

class ConsultaRequest(BaseModel):
    usuario: str
    senha: str
    tipo: str  # cpf, telefone, nome, cnpj, placa, endereco
    valor: str

def autenticar_usuario(req: ConsultaRequest):
    user = USUARIOS.get(req.usuario)
    if not user or user["senha"] != req.senha:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    if req.tipo not in user["permissoes"]:
        raise HTTPException(status_code=403, detail="Permissão negada para essa consulta")
    return True

@app.post("/consulta")
async def consulta(req: ConsultaRequest):
    autenticar_usuario(req)

    # Aqui você chamaria a lógica para consultar o grupo Telegram
    # Vou simular uma resposta genérica
    resultado_simulado = f"Resultado simulado para {req.tipo} = {req.valor}"

    return {"status": "sucesso", "resultado": resultado_simulado}
