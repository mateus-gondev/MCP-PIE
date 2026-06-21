# Regras da Camada de Persistência (SQLite)

## 🗃️ Estrutura do Banco (`gestao.db`)
O banco possui duas tabelas criadas no método `init_db()`:
- **`clientes`**: campos (`id` INTEGER, `nome` TEXT, `cpf` TEXT, `info` TEXT, `endereco` TEXT)
- **`produtos`**: campos (`id` INTEGER, `nome` TEXT, `preco` REAL, `estoque` INTEGER)

## ⚠️ Padrão de Abstração Genérica (Crucial)
O `database.py` utiliza manipulação dinâmica de colunas por `**kwargs`. A IA deve seguir este padrão estritamente:
- **Inserções**: Utilize `database.salvar_novo("nome_da_tabela", campo1=valor1, campo2=valor2)`
- **Atualizações**: Utilize `database.atualizar_registro("nome_da_tabela", registro_id, campo1=valor1)`
- **Buscas**: Utilize `database.buscar_registros("nome_da_tabela", "campo_filtro", valor_filtro)` para filtros com `LIKE %valor%`, ou sem parâmetros adicionais para listar tudo.

## 🔒 Segurança em Banco de Dados
- **SQL Injection**: Ao dar manutenção nas funções internas do `database.py`, mantenha o uso estrito de placeholders `?` para queries parametrizadas.
- **Conexões**: Todas as funções do `database.py` abrem e fecham a conexão local do SQLite em cada operação. Respeite essa arquitetura de sessões curtas sem manter conexões globais persistentes abertas.
