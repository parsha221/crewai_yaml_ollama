import yaml
from langchain_ollama.llms import OllamaLLM

# Load the YAML file
with open(r'/home/genaidevassetv3/GenaiTrainingPractice/sanju/data/sra.yaml', 'r') as file:
yamll = yaml.safe_load(file)

import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task,Crew, LLM

llm = LLM(
model="ollama/llama3.2:latest",
base_url="http://localhost:11434"
)
senior = Agent(
role="Senior Representative",
goal="Be the most friendly and helpful ",
backstory=(
 "You work as analyst and "
"You need to make sure that you provide the best support!"
"Make sure to provide full complete answers, "
" and make no assumptions."
),
allow_delegation=False,
verbose=False,
llm =llm
)

tester = Agent(
role="manual tester",
goal="to provide the test cases ",
backstory=(
"You work as manual tester"
"You need to make sure that to cover all the test cases using response codes"
"Make sure to provide full complete answers, "
" and make no assumptions."
),
allow_delegation=False,
verbose=True,
llm =llm
)

inquiry = Task(
description=(
"{inq}\n\n"
"provided the utilisation {yaml_dat_1}.anaylyse the data."
"provide accurate response to the customer's inquiry."
),

expected_output=(
"provide the details of data"
"leaving no questions unanswered, and maintain a helpful and friendly "
),
output_file="utilsation_reports.md",
agent=senior
)

inquiry1 = Task(
description=(
"provide the test cases for each Authentication service"
"make sure all response codes are covered."
"provide test cases for all the response code for their own Authentication service"
"provide accurate response to the customer's inquiry."
),
expected_output=(
"provide the details of data"
"leaving no questions unanswered, and maintain a helpful and friendly "
),
output_file="utilsation_re.md",
agent=tester
)

crewa = Crew(
agents=[senior,tester],
tasks=[inquiry,inquiry1],
full_output=True,
verbose=0
)
input_1= {
"inq":  "analyse what exists in the data"
"provide the test cases for each of Authentication Service for each path"
"use specific response structures for each Authentication service"
"use all the response codes for generating test cases",
"yaml_dat_1":yamll
}

result = crewa.kickoff(inputs=input_1)

