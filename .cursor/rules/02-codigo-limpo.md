# Padrões de Código Limpo e Qualidade

## 🐍 Estilo Python Moderno
- **Ambiente**: O projeto gerencia dependências usando `uv` (`pyproject.toml` e `uv.lock`). Nunca use comandos `pip` diretamente.
- **Tipagem**: É obrigatório usar *Type Hints* nativos do Python nos argumentos e retornos das ferramentas MCP (ex: `nome: str, preco: float -> str`).
- **Programação Assíncrona**: Sempre que houver requisições de rede ou E/S demoradas, declare a ferramenta como assíncrona (`async def`) e utilize o cliente assíncrono do `httpx` (`async with httpx.AsyncClient() as client:`).

## 🛑 Tratamento de Exceções
- Funções do `server.py` que realizam chamadas de rede ou banco devem ser envelopadas em blocos `try/except`.
- Em caso de falha, retorne uma string descritiva clara iniciando com `"Erro: [detalhe]"` em vez de deixar estourar um Traceback cru para o agente MCP.
