import streamlit as st
from openai import OpenAI

# ================= Config =================
MODEL = "gpt-4o-mini"
API_KEY = st.secrets["HKUST_API_KEY"]
CUSTOM_HEADERS = {"api-key": API_KEY}

client = OpenAI(
    base_url="https://hkust.azure-api.net/hkust-genai/v1",
    api_key=API_KEY,
    default_headers=CUSTOM_HEADERS
)

# ================= Page Setup =================
st.title("HKUST Course Chatbot")
st.caption("Powered by HKUST GenAI")

# ================= Session State Init =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= Display History =================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ================= Handle Input =================
if prompt := st.chat_input("Ask me anything about the course..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=False
            )
            full_response = response.choices[0].message.content
        except Exception as e:
            full_response = f"Error: {str(e)}"
        
        message_placeholder.write(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    