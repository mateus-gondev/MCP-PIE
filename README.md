# 🚀 Sistema de Gestão MCP com SQLite

Este projeto é um servidor de gerenciamento de clientes e produtos baseado no protocolo MCP (Model Context Protocol).

## 🛠️ Pré-requisitos
- [Python 3.10+](https://www.python.org/)
- [uv](https://astral.sh/uv/) (Gerenciador de pacotes)
- [Claude Desktop](https://claude.com/download)

<br>

## 📦 Instalação
1. Clone o repositório:
   ```bash
   git clone ([Repositorio](https://github.com/mateus-gondev/MCP-PIE.git))
   cd MCP-PIE
   ```
2. Instale as dependências:
    ```bash
    uv sync
    ```

<br>

## ⚙️ Configuração no Claude Desktop

1. Instalação do Claude Desktop
Acesse o site oficial da Anthropic([Clade Desktop Download](https://claude.com/download)) e baixe a versão para Windows. Instale o aplicativo e faça login com sua conta gratuita.

2. Localização do Arquivo de Configuração
O Claude Desktop utiliza um arquivo JSON para saber quais servidores MCP ele deve iniciar.

**Passo a Passo:**

**Windows:** Pressione **Win + R** e cole: **%APPDATA%\Claude\claude_desktop_config.json**<br>
ou<br> 
**Procure no Claude Desktop** Var em -> 3 barraras -> Arquivos -> Configurações -> Desenvolvedor -> Editar Config

Abra o arquivo claude_desktop_config.json e adicione a configuração abaixo. Atenção: Substitua o caminho pelo local onde você salvou este projeto.

```bash
{
  "mcpServers": {
    "Gestao-MCP": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/CAMINHO/PARA/SEU/PROJETO",
        "run",
        "server.py"
      ]
    }
  }
}
```

NOTA: Clicando com botão direito na raiz do projeto "Copia Caminho" ou copiando URL das pastas. **Importante** substituir a barra contraria "\" por "/" "//".

---
<br>

## 📖 Documentação Adicional
* **([🔌 Guia de Testes](https://github.com/mateus-gondev/MCP-PIE/blob/main/docs/TOOLS.md))

<br>

Projeto ainda em **Desenvolvimento**