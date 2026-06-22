# INTERFACE DO CHAT (HOST MCP)
import streamlit as st
import requests

# URL do backend
BACKEND_URL = "http://localhost:8000"

# Configuração da página
st.set_page_config(page_title="Gestão MCP Chat", layout="centered")

st.title("🤖 Gestão MCP Chat")

# Sidebar (configuração da LLM)
with st.sidebar:
    st.header("⚙️ Configurações")

    try:
        response = requests.get(f"{BACKEND_URL}/llm-config", timeout=3)
        modelos = response.json().get("modelos_disponiveis", ["gemini"])
        st.success("Backend conectado ✅")
    except Exception:
        modelos = ["gemini", "gpt-4o", "claude-sonnet"]
        st.error("Backend offline ❌")

    selected_model = st.selectbox("Escolha sua LLM:", modelos)
    st.write(f"Modelo ativo: **{selected_model}**")

# Estado do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Como posso ajudar com seus clientes ou produtos?"):
    
    # Salva mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do backend
    with st.chat_message("assistant"):
        with st.spinner("Processando..."):

            try:
                # 🔥 CHAMADA REAL PARA O BACKEND
                response = requests.post(
                    f"{BACKEND_URL}/executar",
                    json={
                        "mensagem": prompt,
                        "modelo": selected_model
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("resposta", "Sem resposta do servidor.")
                else:
                    response_text = f"Erro {response.status_code}: backend falhou."

            except requests.exceptions.ConnectionError:
                response_text = "❌ Não consegui conectar ao backend."
            except requests.exceptions.Timeout:
                response_text = "⏳ O backend demorou para responder."
            except Exception as e:
                response_text = f"Erro inesperado: {str(e)}"

            st.markdown(response_text)

    # Salva resposta
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })