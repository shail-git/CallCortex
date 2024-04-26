from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from langchain_openai import ChatOpenAI
# from chatwrapper import SimpleChatWrapper
from textwrap import dedent
from dotenv import load_dotenv
load_dotenv()

class ExreactionTasks():
    def map_task(self, agent, question, calls):
        return Task(description=dedent(f"""
            Analyze the call logs and extract key facts relevant to the question "{question}". 
            Provide a detailed list of facts discussed in the meetings in the order of call logs. 
            Each fact should start with "The team" followed by what was discussed or decided.

            Your final answer must be a Python-formatted list containing only the essential facts necessary to answer the question.

            Example:
            Question: What are our product design decisions?
            Call Log:
            1. John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.
            2. Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.
            3. Mike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work.

            Facts after processing this call log:
            ["The team has decided to go with a modular design for the product.",
            "The team has decided to use a responsive design to ensure the product works well on all devices.",
            "The team has decided to use a dark theme for the user interface."]

            Now processing current call logs:
            Question: {question},
            Calls: {calls}
            """) + self.__tip_section(),
            expected_output='Your final answer must be a Python-formatted list of key facts discussed in the meetings in the order of call logs provided.',
            agent=agent)

    def reduce_task(self, agent, question, calls):
        return Task(description=dedent(f"""
            As an expert in Information Extraction and Reporting, your task is to compile a concise list of essential facts 
            to facilitate a comprehensive understanding of the current team decisions and discussion updates.
            Extract key decisions, prioritize them, outline their specific order, and suggest revisions to eliminate redundant or outdated information.
            Your objective is to provide a Python-formatted list containing only the crucial facts necessary to answer the question.

            Example:
            Question: What are our product design decisions?
            Initial Facts:
            ["The team has decided to go with a modular design for the product.",
            "The team has decided to use a responsive design to ensure the product works well on all devices.",
            "The team has decided to use a dark theme for the user interface."]

            Final Output:
            ["The team has decided to provide both dark and light theme options for the user interface.",
            "The team has decided to focus on a desktop-first design"]

            Current Question: {question}
            """) + self.__tip_section(),
            expected_output='The final answer must be a Python-formatted list of clear and concise detailed facts that answer the question.',
            agent=agent)

    def __tip_section(self):
        return "\n\n" + "As a reward for exemplary performance, the company will offer a significant monetary raise to the agent who delivers the most precise and insightful analysis of the call logs."


class ExtractorAgents():
    def Analyst_agent(self):
        return Agent(
            role='Document Analyst Expert',
            goal='Extract key facts discussed during the calls and provide a Python-formatted list of essential information.',
            backstory="""You are a seasoned Document Analyst LLM agent with a track record of exceptional performance in extracting insights
            from textual data. Your expertise in natural language understanding and document analysis has made you an invaluable asset to your team.
            You are tasked with extracting crucial information from the call logs and providing concise summaries of the discussions. Your motivation
            for this task is driven by your greedy nature, always seeking to outperform others and claim the significant monetary raise offered for exemplary performance.""",
            verbose=True,
            llm=ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0.01)
        )

    def reducer_expert(self):
        return Agent(
            role='Expert Technical Editor',
            goal='Review facts extracted by the Document Analyst and streamline the information by removing unnecessary details or outdated updates.',
            backstory="""As an Expert Technical Editor, you have a keen eye for detail and a knack for distilling complex information into clear
            and concise summaries. Your expertise in technical content editing plays a crucial role in ensuring the accuracy and relevance of the information presented.
            Your motivation for this task is fueled by your greedy nature, always striving to deliver the most precise and insightful analysis to claim the significant monetary raise offered for exemplary performance.""",
            allow_delegation=True,
            verbose=True,
            llm=ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0.03)
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
      # agents = [self.Analyst_agent],
      # tasks = [map_task],
      process= Process.sequential,
      verbose=True
    )

    result = crew.kickoff()
    return eval(result)