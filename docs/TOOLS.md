### 🛠️ Manual de Ferramentas (Tools)

O servidor disponibiliza as seguintes capacidades para a IA:

## 👤 Gestão de Clientes
* `cadastrar_cliente`: Registra nome, CPF (obrigatório) e notas Ex:.(E-mail, Telefone ou algum valor extrar).
* `editar_cliente`: Modifica dados de um cliente existente usando o CPF.
* `atualizar_endereco_pelo_cpf_e_cep`: Ferramenta automática que consulta a **BrasilAPI** e salva o endereço completo via CPF.
* `atualizar_endereco_direto`: Permite digitar o endereço manualmente (útil para complementos ou áreas sem CEP).
* `buscar_cliente_por_cep_ou_cpf`: Localiza registros e exibe o endereço completo salvo.

## 📦 Gestão de Produtos
* `cadastrar_produto`: Adiciona itens ao inventário com nome, preço e estoque.
* `editar_produto`: Atualiza valores ou quantidades.
* `remover_produto`: Exclui um item pelo ID ou nome.

## 📋 Geral
* `listar_tudo`: Gera um relatório completo de todos os clientes e produtos no banco.