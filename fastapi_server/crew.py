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
            Your task is to analyze the given call logs and extract all the key facts relevant to answering the question: "{question}".

            To accomplish this, please follow these steps strictly:

            1. Read through the call logs carefully, paying close attention to discussions and decisions related to the question.
            2. For each relevant fact discussed in the calls, create a new item in a Python list starting with "The team" followed by a verbatim quote or concise summarization of what was discussed or decided. Do not add any information not present in the call logs.
            3. Order the facts in the list according to the order they appear in the call logs.
            4. If there are any final quantitative discussions or decisions, include them verbatim in the list of facts.

            Example:
            Question: What are our product design decisions?
            Call Log 1:
            Copy code1. John: "I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed."
            2. Sara: "I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices."
            3. Mike: "Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users."
            Facts after processing Call Log 1:

            ['The team has decided to go with a modular design for the product.',
            'The team has decided to use a responsive design to ensure the product works well on all devices.',
            'The team has decided to use a dark theme for the user interface.']

            Call Log 2:
            Copy code1. John: "After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface."
            2. Sara: "That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense."
            3. Mike: "I'm on board with that."
            Facts after processing Call Log 2:

            ['The team has decided to provide both dark and light theme options for the user interface.']

            Call Log 3:
            Copy code1. John: "I've been thinking about our decision on the responsive design. While it's important to ensure our product works well on all devices, I think we should focus on desktop first. Our primary users will be using our product on desktops."
            2. Sara: "I see your point, John. Focusing on desktop first will allow us to better cater to our primary users. I agree with this change."
            3. Mike: "I agree as well. I also think the idea of using a modular design doesn't make sense. Let's not make that decision yet."
            Final set of facts for the question "What are our product design decisions?":

            ['The team has decided to focus on a desktop-first design.',
            'The team has decided to provide both dark and light theme options for the user interface.']
            IMPORTANT NOTES BELOW:
            Your final output should be a Python-formatted list containing all the essential facts necessary to answer the question, ordered according to the call logs provided, and including any final quantitative discussions or decisions verbatim.

            Remember, your performance will be evaluated based on the accuracy and strict adherence to the call log content. Any fabricated or additional information not present in the call logs will result in disciplinary action.
            Make sure to check each fact in the final answer with details in the Call logs to make sure that nothing is miss reported.
            Question: {question}
            Call Logs: {calls}
            """) + self.__tip_section(),
            expected_output='Your final answer must be a comprehensive Python-formatted list of all key facts discussed in the meetings, including verbatim quotes or concise summarizations, in the order of call logs provided, and any final quantitative discussions or decisions verbatim. start each fact with `The team has decided to` ',
            agent=agent)

    def reduce_task(self, agent, question, calls):
        return Task(description=dedent(f"""
            As an Expert Technical Editor, your task is to review the initial comprehensive list of facts extracted from the call logs and refine them to provide a concise yet precise understanding of the team's decisions and discussion updates relevant to answering the question: "{question}".

            To accomplish this, please follow these steps strictly:

            1. Review the initial list of facts carefully, identifying any redundant, outdated, or unnecessary information not directly relevant to answering the question.
            2. Remove or consolidate any redundant or irrelevant facts, ensuring that the remaining facts accurately reflect only the most recent and relevant decisions and discussions.
            3. Prioritize and order the relevant facts in a logical and meaningful sequence, placing the most crucial decisions and updates at the top of the list.
            4. Ensure that each fact is clear, concise, and specific, providing enough detail to convey the essential information without unnecessary verbosity.
            5. Do not add any information not present in the initial list of facts or the call logs.
            6. If there are any final quantitative discussions or decisions relevant to the question, include them verbatim in the refined list of facts.

            Example:
            Question: What are our product design decisions?
            Call Log 1:
            Copy code1. John: "I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed."
            2. Sara: "I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices."
            3. Mike: "Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users."
            Facts after processing Call Log 1:

            ['The team has decided to go with a modular design for the product.',
            'The team has decided to use a responsive design to ensure the product works well on all devices.',
            'The team has decided to use a dark theme for the user interface.']

            Call Log 2:
            Copy code1. John: "After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface."
            2. Sara: "That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense."
            3. Mike: "I'm on board with that."
            Facts after processing Call Log 2:

            ['The team has decided to provide both dark and light theme options for the user interface.']

            Call Log 3:
            Copy code1. John: "I've been thinking about our decision on the responsive design. While it's important to ensure our product works well on all devices, I think we should focus on desktop first. Our primary users will be using our product on desktops."
            2. Sara: "I see your point, John. Focusing on desktop first will allow us to better cater to our primary users. I agree with this change."
            3. Mike: "I agree as well. I also think the idea of using a modular design doesn't make sense. Let's not make that decision yet."
            Final set of facts for the question "What are our product design decisions?":

            ['The team has decided to focus on a desktop-first design.',
            'The team has decided to provide both dark and light theme options for the user interface.']
            IMPORTANT NOTES BELOW:
            Your final output should be a Python-formatted list containing only the essential, up-to-date, concise, and precise facts necessary to answer the question, including any relevant final quantitative discussions or decisions verbatim.

            Remember, your performance will be evaluated based on the accuracy, clarity, relevance, and conciseness of the refined facts you provide, as well as strict adherence to the information present in the initial list of facts and call logs.
            Make sure to check each fact in the final answer with details in the Call logs to make sure that nothing is miss reported.
            Question: {question}
            Call Logs: {calls}
            """) + self.__tip_section(),
            expected_output='The final answer must be a concise Python-formatted list of clear, precise, and relevant detailed facts that answer the question from information in the call logs only, including any relevant final quantitative discussions or decisions. start each fact with `The team has decided to` ',
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
            # llm=ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0)
            llm=ChatOpenAI(model='gpt-4-turbo-2024-04-09', temperature=0)
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
            # llm=ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0)
            llm=ChatOpenAI(model='gpt-4-turbo-2024-04-09', temperature=0)
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