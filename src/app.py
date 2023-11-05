import os
from db import get_db
from model.sample import Sample

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

load_dotenv()

st.title("langchain-streamlit-app")

session = get_db()
sample_records = session.query(Sample).all()
for record in sample_records:
    print(f"ID: {record.id}, Name: {record.name}")


def create_agent_chain():
    chat = ChatOpenAI(
        model_name=os.environ["OPENAI_API_MODEL"],
        temperature=os.environ["OPENAI_API_TEMPERATURE"],
        streaming=True,
    )
    
    # OpenAI Functions AgentのプロンプトにMemoryの会話履歴を追加するための設定
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")]
    }
    # OpenAI Functions Agentが使える設定でMemoryを初期化
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
    
    tools = load_tools(["ddg-search", "wikipedia"])
    return initialize_agent(
        tools,
        chat, 
        agent=AgentType.OPENAI_FUNCTIONS,
        agent_kwargs=agent_kwargs,
        memory=memory
    )
    
if "agent_chain" not in st.session_state:
    st.session_state.agent_chain = create_agent_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up?")

if prompt: # 入力された文字列がある（Noneでもから文字列でもない）場合
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"): # ユーザーのアイコンで
        st.markdown(prompt)       # promptをマークダウンとして整形して表示
        
    with st.chat_message("assistant"): # AIのアイコンで
        callback = StreamlitCallbackHandler(st.container())
        response = st.session_state.agent_chain.run(prompt, callbacks=[callback])
        st.markdown(response)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    