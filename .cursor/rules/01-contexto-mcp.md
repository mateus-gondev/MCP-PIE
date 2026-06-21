# Contexto do Servidor MCP: Gestao_MCP

## 🎯 Escopo do Projeto
Este projeto é um servidor rodando **FastMCP** chamado `"Gestao_MCP"`. Ele conecta o Claude IA a um sistema local de controle de clientes e produtos comerciais.

## ⚙️ Fluxo de Dados e Dependências
1. **Comunicação Externa**: O projeto utiliza a biblioteca `httpx` assíncrona para se comunicar com APIs externas (ex: `BrasilAPI` para consulta de CEPs).
2. **Camada de Adaptação**: O arquivo `server.py` expõe as ferramentas com `@mcp.tool()`. Elas devem focar em validar parâmetros básicos, tratar retornos visuais e acionar o módulo `database.py`.

## 🛠️ Assinatura e Docstrings Importantes
As docstrings das ferramentas devem ser **extremamente detalhadas e escritas em português**, pois o Claude lê estas descrições para deduzir as intenções do usuário.
- Exemplo a seguir: Sempre oriente o agente na docstring sobre como agir caso falte algum parâmetro (ex: pedir CPF de teste).
