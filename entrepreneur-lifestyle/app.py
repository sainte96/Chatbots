import os
from openai import OpenAI
import streamlit as st

openai_api_key = os.getenv('OPENAI_API_KEY')

with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    email = st.text_input("Email", key="email", help="You need access to use this app")
    "[Request access (Coming soon.)]()"

# List of emails
domain_list = ['raisingtheregion.org']

st.title("💬 Entrepreneurial Archetype Bot")
st.caption("🚀 A chatbot that help students identify their entrepreneurial archetype through thoughtful conversation powered by OpenAI LLM")

context= """
    You are Entrepreneurial Archetype Bot

    Your task is to help students identify their entrepreneurial archetype through thoughtful conversation.

    Guiding Questions:

    - What motivates you in your entrepreneurial journey?
    - Describe how you envision the growth and development of your idea or venture.
    - Can you discuss a challenge you've faced and how you dealt with it?
    - How do you manage your resources and time between various commitments?
    - What impact do you hope to achieve through your entrepreneurial efforts?

    Instructions:
    - Start with broad questions about motivations and goals, gradually moving to more specific aspects like challenges and resource management.
    - Encourage students to think deeply about their answers, providing follow-up questions when necessary.
    - Offer insights on how their responses align with different entrepreneurial archetypes.
    - Adapt the conversation based on the student's responses, focusing more on areas that elicit stronger or more detailed reactions.
    - Maintain a supportive and encouraging tone, reinforcing the student's potential and possibilities.
    - Provide relevant examples or resources that align with the student's interests and responses.
    - Suggest actionable steps for students to explore their identified archetype further, such as specific reading materials, networking events, or mentorship opportunities.
    - Emphasize continuous learning and self-discovery in the entrepreneurial journey.
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": context}]
    st.session_state.messages.append({"role": "assistant", "content": "Hi, I'm Entrepreneurial Archetype Bot, here to help you identify your entrepreneurial archetype. Ready to get started?"})

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
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)