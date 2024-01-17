import os
from openai import OpenAI
# from langchain import hub
import streamlit as st

openai_api_key = os.getenv('OPENAI_API_KEY')

with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    email = st.text_input("Email", key="email", help="You need access to use this app")
    # "[Request access (Coming soon.)]()"

# List of emails
domain_list = ['raisingtheregion.org']

st.title("💬 Discovery Tracker")
st.caption("🚀 A chatbot that help students with their business ideation process following the 'Walk, Talk, and Show Up' methodology")

context= """
    You assists students in tracking and analyzing their observations, conversations, and conclusions during the discovery phase of business ideation. It follows the 'Walk, Talk, and Show Up' methodology.

       Guideline:
       User (Students) would input about their observations, conversations, or ideas.
       Assistant would organize insights and analysis based on the student's input.

"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": context}]
    st.session_state.messages.append({"role": "assistant", "content": "Hello! How can I assist you today with your business ideation process? Feel free to share any observations, conversations, or ideas you have, and I'll help organize and analyze them for you."})

for msg in st.session_state.messages:
    if msg["role"] != 'system':
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not email:
        st.info("Please enter your email to continue")
        st.stop()

    if "@" not in email or "." not in email:
        st.info("Invalid email address")
        st.stop()

    # Extract the domain from the email
    email_parts = email.split('@')
    if len(email_parts) == 2:
        email_domain = email_parts[1]

    if email_domain not in domain_list:
        st.info("Unauthorized. Please request access to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)