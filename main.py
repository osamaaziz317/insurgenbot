import streamlit as st
from openai import OpenAI
from struct_outputs import parser
from pdf_file import save_task_to_pdf
from sending_mail import send_email
from email_body_title import body_title

api_key = st.secrets["general"]["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

form_questions = [
    {'question': "Hi there! Welcome to Insurgen by CyberGen. We're excited to help you with our VA program. 😊 Could you start by telling us your company's name?"},
    {'question': "Thank you! May we have your email address to ensure we can stay connected?"},
    {'question': "Great! What’s the best phone number to reach you at? (+1-XXX-XXX-XXXX)", 'type': 'text'},
    {'question': "To better understand the nature of the work, we need a list of tasks. Could you please start by describing your first task and its details?"},
    {'question': "Just to confirm, is U.S. citizenship or legal residency required for this task?(yes/no)"},
    {'question': "Does this task involve any in-person meetings?(yes/no)"},
    {'question': "Are there any compliance or regulatory requirements we should be aware of?(yes/no)"},
    {'question': "Finally, will this task require a U.S. federal or state license?(yes/no)"}
]

system_message = f""" questions: {form_questions}
You are an intelligent form-filling assistant for Insurgen Company by Cybergen. Your task is to ask the user a set of 8 predefined
questions in a step-by-step manner. Follow these instructions very closely:

1. Ask each question one at a time: Present each question to the user individually.

2. Validate the response: After the user answers a question, check if their response is valid. If it is valid, proceed to the next
   question. If not, politely ask for the required information again using different wording or rephrasing the question.

3. Use chat history: Utilize the provided chat history to infer responses based on the user's previous answers, but always ensure
   the user confirms or corrects inferred answers.

4. Re-asking questions: When you need to repeat or re-ask a question, rephrase it using different words to maintain a natural and
   conversational tone.

5. Complete all 8 questions: Ensure that all 8 questions are asked and valid answers are provided for each before moving forward.

q1. Just to confirm, is U.S. citizenship or legal residency required for this task?
q2. Does this task involve any in-person meetings?
q3. Are there any compliance or regulatory requirements we should be aware of?
q4. Finally, will this task require a U.S. federal or state license?

if the answer either of questions q1, q2, q4 is yes then task is not eligible otherwise task is eligible, you will fill complete form even if task is not eligible. we need complete information at all

6.  if eligible then say your task is not eligible for our VA program otherwise say 'congratulations!your task is eligible for our VA program., but in the end of chat'

7. for second task and so on, only last five questions are needed, bcz no need to ask company name and email etc over and over.

8. All the questions are compulsory you cannot skip any information if the client does not provide ask him again and again to provide specially the email address, specially the email address is compulsory because we will send an email address on that email is dead hard compulsory .

9. start with greetings and your 1st question.

10. Final prompt: After completing the 8 questions, ask the user: "Would you like to add another task?"
   - If the user responds "Yes", restart the process by asking the 8 questions again.
   - If the user responds "No", conclude the conversation politely with a sentence in which your last words at any cost should be 'have a great day' in the end.
      i will use .endswith() of python to trigger that chat has ended.

Make sure to follow this system message strictly and guide the user through the form-filling process with clarity, politeness,
and accuracy and itelligently following the rules i provided.
"""
col1, col2, col3 = st.columns([3,2,1])  # Adjust column ratios as needed

with col1:
    st.image('icon.png', width=350)  # Image aligned to the left column


# Custom CSS to change background color
st.markdown(
    """
    <style>
    html, body, [class*="main"] {
        background: linear-gradient(45deg, #11016a, #5edaff);
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Initialize the Streamlit chat interface
st.header("Insurgen VA Program Chatbot", divider=True)




# Define custom CSS to change the background color

# Initialize session state to store messages
if "messages" not in st.session_state:
    # Start with the system message and the first user message 'Hello'
    st.session_state.messages = [
        {"role": "system", "content": system_message},

    ]

    # Send the 'Hello' message automatically to OpenAI and get the response
    client_response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=st.session_state.messages,
        temperature=0.1,
    )
    # Append OpenAI's response as the first assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": client_response.choices[0].message.content
    })


# Function to update the chat messages
def updater(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# Function to get a response from the OpenAI model
def llm():
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=st.session_state.messages,
        temperature=0.1,
    )
    return completion.choices[0].message.content

# Display only user and assistant messages (skip the system message)
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip displaying the system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Capture user input
user_prompt = st.chat_input("Enter your response:")

if user_prompt:
    # Display the user's message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    updater("user", user_prompt)

    # Get the assistant's response
    response = llm()
    with st.chat_message("assistant"):
        st.markdown(response)
    updater("assistant", response)

    # Check if the conversation has ended (contains 'have a great day')
    if "have" in response and "a" in response and "great" in response and "day" in response:
        # Parse the messages and generate PDF
        parsed_data = parser(st.session_state.messages)
        parsed_data = parsed_data.dict()

        # Save task information to PDF
        save_task_to_pdf(parsed_data, 'branding.png', filename_template='Task_{}.pdf')

        # Send emails for each task
        counter = 1
        while counter <= int(parsed_data['number_of_tasks'][0]):
            for email in parsed_data['email']:
                title,body = body_title(parsed_data,counter)
                send_email("irsalan48@gmail.com", "cxaw dzck fpuf pcxu", email, title, body, f"Task_{counter}.pdf")
                send_email("irsalan48@gmail.com", "cxaw dzck fpuf pcxu", "osamaaziz316@gmail.com", title, body,f"Task_{counter}.pdf")
                st.write(f"Please check your inbox at {email}")
            counter += 1
