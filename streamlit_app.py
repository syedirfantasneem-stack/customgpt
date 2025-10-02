import streamlit as st
from openai import OpenAI
import time

# Initialize client (make sure your OPENAI_API_KEY is set in environment)

client = OpenAI(
    api_key="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",
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

print(openai.__version__) 

# Demo Assistant
ASSISTANT_ID = "asst_SRCRvmDX03cKACsoqaAykdwH"

st.set_page_config(page_title="Testing Custom Calls...", page_icon="💬", layout="centered")

st.title("💬 Testing")
st.write("Enter your problem below to get instant quote.")

# Text input
query = st.text_area("Describe your issue:", height=150)

if st.button("Submit Query"):
    if not query.strip():
        st.warning("Please enter a description of your problem.")
    else:
        # Step 1: Create a thread
        thread = client.threads.create()

        # Step 2: Add the user message to the thread
        client.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )

        # Step 3: Run the assistant on this thread
        run = client.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Step 4: Poll until run completes
        with st.spinner("Thinking..."):
            while True:
                run_status = client.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    st.error(f"Run ended with status: {run_status.status}")
                    st.stop()
                time.sleep(2)

        # Step 5: Retrieve messages
        messages = client.threads.messages.list(thread_id=thread.id)

        # Find the assistant's last reply
        answer = None
        for msg in messages.data:
            if msg.role == "assistant":
                if msg.content and msg.content[0].type == "text":
                    answer = msg.content[0].text.value
                break

        if answer:
            st.subheader("Assistant's Response:")
            st.write(answer)
        else:
            st.warning("No response received from assistant.")
