from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from fastapi import Request
import database
import httpx
import json
import uvicorn


mcp = FastMCP("Gestao_MCP")
database.init_db()

from fastapi import FastAPI
app = FastAPI()
app.mount("/mcp", mcp.sse_app)

@app.get("/llm-config")
def get_llm_config():
    return {
        "modelos_disponiveis": [
            "gemini",
            "gpt-4o",
            "claude-sonnet"
        ]
    }
    
    
class RequestData(BaseModel):
    mensagem: str
    modelo: str

# AGENTES MOCKADOS
def executar_gemini(msg: str) -> str:
    return f" [Gemini] respondeu: {msg}"

def executar_gpt(msg: str) -> str:
    return f" [GPT-4o] respondeu: {msg}"

def executar_claude(msg: str) -> str:
    return f" [Claude Sonnet] respondeu: {msg}"


# Crud Produtos e Clientes
@mcp.tool()
def executar_operacao_crud(tabela: str, acao: str, dados: str = "{}") -> str:
    """
    Ferramenta generativa para realizar operações de CRUD (Criar, Ler, Atualizar e Deletar)
    nas tabelas de 'clientes' e 'produtos'.
    
    Parâmetros:
    - tabela: A tabela que sofrerá a ação ('clientes' ou 'produtos').
    - acao: O tipo de operação a ser realizada.
    - dados: Uma string JSON contendo os campos necessários para a operação.
      * Para 'cadastrar': envie todos os campos obrigatórios.
      * Para 'editar' ou 'remover': DEVE incluir o campo "id".
      * Para 'listar': pode incluir chaves como "campo_filtro" e "valor_filtro" para buscas.
    """
    try:
        payload = json.loads(dados)
    except json.JSONDecodeError:
        return "Erro: O parâmetro 'dados' precisa ser uma string JSON válida."

    # CADASTRAR 
    if acao == "cadastrar":
        if tabela == "clientes" and "endereco" not in payload:
            payload["endereco"] = ""
        return database.salvar_novo(tabela, **payload)

    #  EDITAR 
    elif acao == "editar":
        if "id" not in payload:
            return "Erro: Para editar, você deve fornecer o ID do registro dentro do JSON de dados."
        registro_id = payload.pop("id")
        return database.atualizar_registro(tabela, registro_id, **payload)

    # REMOVER 
    elif acao == "remover":
        if "id" not in payload:
            return "Erro: Para remover, você deve fornecer o ID do registro dentro do JSON de dados."
        return database.deletar_registro(tabela, payload["id"])

    # LISTAR 
    elif acao == "listar":
        campo = payload.get("campo_filtro")
        valor = payload.get("valor_filtro")
        resultados = database.buscar_registros(tabela, campo, valor)
        
        if not resultados:
            return f"Nenhum registro encontrado na tabela '{tabela}'."
        
        output = [f"--- LISTAGEM DE {tabela.upper()} ---"]
        for r in resultados:
            if tabela == "clientes":
                item = f"ID: {r[0]} | Nome: {r[1]} | CPF: {r[2]} | Notas: {r[3]} | Endereço: {r[4] or 'Não cadastrado'}"
            else: 
                item = f"ID: {r[0]} | Nome: {r[1]} | Preço: R${r[2]:.2f} | Estoque: {r[3]}"
            output.append(item)
            
        return "\n".join(output)

    return "Erro: Ação não reconhecida."

# (API CEP)
@mcp.tool()
async def atualizar_endereco_pelo_cpf_e_cep(cpf: str, cep: str) -> str:
    """
    Busca o endereço automaticamente pelo CEP usando a BrasilAPI e o vincula 
    ao cliente identificado pelo CPF informado.
    """
    clientes = database.buscar_registros("clientes", "cpf", cpf)
    if not clientes:
        return f"Erro: não encontrei nenhum cliente cadastrado com o CPF {cpf}."
    
    id_cliente = clientes[0][0] 
    cep_limpo = cep.replace("-", "").replace(" ", "")
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"https://brasilapi.com.br/api/cep/v1/{cep_limpo}")
            if resp.status_code == 200:
                d = resp.json()
                endereco = f"{d['street']}, {d['neighborhood']}, {d['city']}-{d['state']}"
                return database.atualizar_registro("clientes", id_cliente, endereco=endereco)
            return f"CEP {cep} não encontrado na base de dados nacional."
        except Exception as e:
            return f"Erro na conexão com a API: {str(e)}"

def executar_llm(mensagem: str, modelo: str):
    
    if modelo == "gemini":
        return executar_gemini(mensagem)

    elif modelo == "gpt-4o":
        return executar_gpt(mensagem)

    elif modelo == "claude-sonnet":
        return executar_claude(mensagem)

    else:
        return "Modelo não suportado."



# ROTEADOR DE MODELO
def executar_llm(mensagem: str, modelo: str) -> str:

    if modelo == "gemini":
        return executar_gemini(mensagem)

    elif modelo == "gpt-4o":
        return executar_gpt(mensagem)

    elif modelo == "claude-sonnet":
        return executar_claude(mensagem)

    else:
        return "Modelo não suportado."


# EXECUÇÃO PRINCIPAL
@app.post("/executar")
def executar(request: RequestData):
    resposta = executar_llm(request.mensagem, request.modelo)
    return {"resposta": resposta}


@app.get("/")
def root():
    return {"status": "Servidor MCP rodando 🚀"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)