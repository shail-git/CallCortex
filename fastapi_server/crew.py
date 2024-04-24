from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from langchain_openai import ChatOpenAI
from textwrap import dedent
from compressor import compress_docs
from dotenv import load_dotenv
load_dotenv()

def get_inputs(payload) -> dict:
  content = dict()
  data = payload
  question = data['question']
  content['question'] = question
  content['calls'] = compress_docs(question, data['documents'])
  return content

class ExreactionTasks():
  def map_task(self, agent, question, calls):
    return Task(description=dedent(f"""
        Analyze and select the most important facts for answering the question based
        on specific criteria such as Implementation details and order of the conversation.
        This task involves comparing multiple call Logs, considering factors like priorities,
        implementation details and order of meetings / calls and overall goal.

        Your final answer must be a detailed list of facts discussed in the meetings in the order, and everything you can infer from the call.
        {self.__tip_section()}
        question: {question},
        calls: {calls.items()}
      """),
      expected_output='Your final answer must be a detailed list of facts discussed in the meetings in the order, and everything you can infer from the call.',
      agent=agent)

  def reduce_task(self, agent, question, calls):
    return Task(description=dedent(f"""
        As an expert in Information Extraction and Reporting, your task is to compile a concise list of essential facts to facilitate a comprehensive understanding of the current team decisions and discussion updates.
        Extract key decisions, prioritize them, outline their specific order, and suggest revisions to eliminate redundant or outdated information.
        Your objective is to provide a Python-formatted list containing only the crucial facts necessary to answer the question, suitable for a Project Manager's comprehension.
        {self.__tip_section()}
        question: {question},
        calls: {calls.items()}
      """),
      expected_output = 'The final answer must be a python format list of clear and concise facts that answer the question, no extra text.',
      agent=agent)

  def __tip_section(self):
    return "As a reward for your exemplary performance, the company will offer a significant monetary raise to the agent who delivers the most precise and insightful analysis of the call logs. Your exceptional skills in document analysis will not only contribute to the success of the project but also enhance your professional reputation within the company."

class ExtractorAgents():
  # model = 'TheBloke/Llama-2-7B-GGML'
  def Analyst_agent(self):
    return Agent(
        role='Document Analyst Expert',
        goal='provide a concise summary of the decisions made by the team and identify key facts discussed during the calls. ',
        backstory=
        """You are a seasoned Document Analyst LLM agent with a track record of exceptional performance in extracting insights
         from textual data. Your expertise in natural language understanding and document analysis has made you an invaluable
          asset to your team. Recognizing your outstanding contributions, your company has decided to offer a monetary raise for
          the agent who provides the most accurate and concise summaries of the call logs, highlighting the crucial decisions and facts discussed.""",\
        # allow_delegation=True,
        verbose=True,
        llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temprature=0.3)
        )

  def reducer_expert(self):
    return Agent(
       role='Expert Technical Editor',
        goal='reviewing information extracted by the Document Analyst from call logs discussing product design decisions. Your task is to analyze the facts provided and the question posed, and then streamline the information by removing unnecessary details. Your output should be a Python list containing only the essential facts relevant to the question and call logs. starting with the string `the team has decised to `',
        backstory="""As an Expert Technical Editor, you have a keen eye for detail and a knack for distilling complex information into clear
        and concise summaries. With your expertise in technical content editing, you play a crucial role in ensuring that the information presented
        is accurate, relevant, and easily understandable. Your commitment to precision and efficiency has earned you recognition within the team,
        and your contributions are instrumental in delivering high-quality outputs.""",
        # allow_delegation=True,
        verbose=True,
        llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temprature=0.3)
        )


class FactExtractionCrew:
  def __init__(self):
    agents = ExtractorAgents()
    self.Analyst_agent = agents.Analyst_agent()
    self.reducer_expert = agents.reducer_expert()


  def run(self, question, calls):
    tasks = ExreactionTasks()
    map_task = tasks.map_task(
      self.Analyst_agent,
      question,
      calls
    )
    reduce_task = tasks.reduce_task(
      self.reducer_expert,
      question,
      calls
    )
    crew = Crew(
      agents=[self.Analyst_agent, self.reducer_expert],
      tasks=[map_task, reduce_task],
      process= Process.sequential,
      verbose=True
    )

    result = crew.kickoff()
    return result