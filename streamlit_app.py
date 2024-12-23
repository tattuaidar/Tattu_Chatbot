import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot created by Tattu Aidar")
st.write(
    "This is a simple chatbot that helps you to learn English grammar as a non-eglish speaker."
    "To use this app, you need to provide an OpenAI API key, which you can find in email. "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        # Initialize the session with a system message to provide instructions.
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that specializes in teaching English language grammar as a non-eglish speaker "
                    "You provide clear, friendly, "
                    "and accurate responses to user queries about grammaticle rules, writing sentences, "
                    "and other related topics."
                ),
            }
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
