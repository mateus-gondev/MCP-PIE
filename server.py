from mcp.server.fastmcp import FastMCP
import database
import httpx

# Inicializa o FastMCP 
mcp = FastMCP("Gestao_MCP")
database.init_db() # Inicializa o banco de dados

# CLIENTE

@mcp.tool()
def cadastrar_cliente(nome: str, cpf: str, info: str, endereco: str = "") -> str:
    """
    Cadastra um novo cliente no sistema. 
    O campo CPF é obrigatório. Se o usuário não fornecer, solicite um CPF 
    (pode ser um gerado para testes).
    """
    return database.salvar_novo("clientes", nome=nome, cpf=cpf, info=info, endereco=endereco)

@mcp.tool()
def editar_cliente(id_cliente: int, nome: str = None, cpf: str = None, info: str = None) -> str:
    """Edita os dados básicos de um cliente já existente pelo ID."""
    dados = {k: v for k, v in {"nome": nome, "cpf": cpf, "info": info}.items() if v is not None}
    return database.atualizar_registro("clientes", id_cliente, **dados)

@mcp.tool()
async def atualizar_endereco_pelo_cpf_e_cep(cpf: str, cep: str) -> str:
    """
    Busca o endereço pelo CEP e o vincula automaticamente ao cliente 
    identificado pelo CPF informado.
    """
    
    clientes = database.buscar_registros("clientes", "cpf", cpf)
    
    if not clientes:
        return f"Erro não encontrei nenhum cliente cadastrado com o CPF {cpf}."
    
    id_cliente = clientes[0][0] 
    
    # Busca o endereço na BrasilAPI
    cep_limpo = cep.replace("-", "").replace(" ", "")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"https://brasilapi.com.br/api/cep/v1/{cep_limpo}")
            if resp.status_code == 200:
                d = resp.json()
                endereco = f"{d['street']}, {d['neighborhood']}, {d['city']}-{d['state']}"
                
                return database.atualizar_registro("clientes", id_cliente, endereco=endereco)
            else:
                return f"CEP {cep} não encontrado na base de dados nacional."
        except Exception as e:
            return f"Erro na conexão com a API: {str(e)}"

@mcp.tool()
def buscar_cliente_por_cep_ou_cpf(termo: str) -> str:
    """Busca clientes por parte do endereço (como CEP) ou pelo CPF exato."""
    
    resultados = database.buscar_registros("clientes", "endereco", termo)
    if not resultados:
        resultados = database.buscar_registros("clientes", "cpf", termo)
    
    if not resultados: 
        return "Nenhum cliente encontrado com esse termo."
    
    output = []
    for r in resultados:
        detalhe = (
            f"ID: {r[0]}\n"
            f"Nome: {r[1]}\n"
            f"CPF: {r[2]}\n"
            f"Notas: {r[3]}\n"
            f"Endereço Completo: {r[4] if r[4] else 'Não cadastrado'}\n"
            "-------------------"
        )
        output.append(detalhe)
    
    return "\n".join(output)

@mcp.tool()
def atualizar_endereco_direto(cpf: str, novo_endereco: str) -> str:
    """
    Atualiza o endereço de um cliente informando o CPF e o texto do endereço 
    por extenso (Rua, Número, Bairro, etc). Use esta ferramenta quando 
    o usuário não quiser usar o CEP.
    """
    
    clientes = database.buscar_registros("clientes", "cpf", cpf)
    
    if not clientes:
        return f"Cliente com CPF {cpf} não encontrado."
    
    id_cliente = clientes[0][0]
    
    return database.atualizar_registro("clientes", id_cliente, endereco=novo_endereco)

# PRODUTOS

@mcp.tool()
def cadastrar_produto(nome: str, preco: float, estoque: int) -> str:
    """Cadastra um novo produto no inventário."""
    return database.salvar_novo("produtos", nome=nome, preco=preco, estoque=estoque)

@mcp.tool()
def editar_produto(id_produto: int, nome: str = None, preco: float = None, estoque: int = None) -> str:
    """Atualiza dados de um produto existente."""
    dados = {k: v for k, v in {"nome": nome, "preco": preco, "estoque": estoque}.items() if v is not None}
    return database.atualizar_registro("produtos", id_produto, **dados)

@mcp.tool()
def remover_produto(id_produto: int) -> str:
    """Exclui permanentemente um produto pelo ID."""
    return database.deletar_registro("produtos", id_produto)

@mcp.tool()
def listar_tudo() -> str:
    """Lista todos os clientes e produtos cadastrados."""
    c = database.buscar_registros("clientes")
    p = database.buscar_registros("produtos")
    res = "--- CLIENTES ---\n" + "\n".join([f"{x[0]}: {x[1]} (CPF: {x[2]})" for x in c])
    res += "\n\n--- PRODUTOS ---\n" + "\n".join([f"{y[0]}: {y[1]} - R${y[2]}" for y in p])
    return res

if __name__ == "__main__":
    mcp.run()