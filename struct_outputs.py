from pydantic import BaseModel
from openai import OpenAI
import streamlit as st

api_key = st.secrets["general"]["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
class TasksQuestionnaire (BaseModel):
    company_name: list[str]
    email: list[str]
    phone_number: list[str]
    number_of_tasks: int
    task_name: list[str]
    citizenship_or_residency: list[str]
    in_person_meeting: list[str]
    compliance_requirements: list[str]
    federal_or_state_licence: list[str]
    number_of_tasks: list[int]
    task_eligibility_yes_or_no: list[str]

system_message = """You are an intelligent assistant responsible for collecting information for a task questionnaire. Please ask the user the following questions and provide their responses in a structured format. The information should be returned using these fields:

- company_name (list of strings)
- email (list of strings)`
- phone_number (list of strings)
- number_of_tasks integer
- task_name (list of strings)
- citizenship_or_residency (yes/no)
- in_person_meeting (yes/no)
- compliance_requirements (list of strings)
- federal_or_state_licence (list of strings)
- task_eligibility_yes_or_no (list of strings (yes,no))

q1. Just to confirm, is U.S. citizenship or legal residency required for this task?
q2. Does this task involve any in-person meetings?
q3. Are there any compliance or regulatory requirements we should be aware of?
q4. Finally, will this task require a U.S. federal or state license?
if the answer either of questions q1, q2, q4 is yes then task is not eligilble otherwise task is eligible.
Ask each question one at a time, validate the responses, and proceed to the next question. Once all answers are provided, return the information in the structured format. For every task create a new element in list always.
"""

def parser(messages,systemn_message=system_message):
    messages[0]['role']="system"
    messages[1]['content']=systemn_message
    print("this is messages",messages)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=TasksQuestionnaire,
    )

    parsed_data = completion.choices[0].message.parsed
    return parsed_data
