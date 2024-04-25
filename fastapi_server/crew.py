from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from langchain_openai import ChatOpenAI
# from chatwrapper import SimpleChatWrapper
from textwrap import dedent
from dotenv import load_dotenv
load_dotenv()


# class ExreactionTasks():
#     def map_task(self, agent, question, calls):
#         example_call_log = dedent("""
#             Call Log:
#             00:00:10 - Alex: Let's choose our app's color scheme today.
#             00:00:36 - Jordan: I suggest blue for a calm feel.
#             00:00:51 - Casey: We need to make sure it's accessible to all users.
#         """)
#         example_question = "What product design decisions did the team make?"
#         example_output = dedent("""
#             Output:
#             ["The team will use blue for the color scheme of the app.",
#              "The team will make the app accessible to all users."]
#         """)
#         return Task(description=dedent(f"""
#             Analyze and select the most important facts for answering the question based
#             on specific criteria such as Implementation details and order of the conversation.
#             This task involves comparing multiple call Logs, considering factors like priorities,
#             details discussed, and order of meetings/calls, with the understanding that the order matters 
#             and facts may update accordingly.
#             Your final answer must be a Python-formatted list containing the facts discussed and no extra words.
#             here are a few examples:
#             Example 1:
#             Question: What are our product design decisions?
#             Call Log 1
#             1
#             00:01:11,430 --> 00:01:40,520
#             John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.
#             2
#             00:01:41,450 --> 00:01:49,190
#             Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.
#             3
#             00:01:49,340 --> 00:01:50,040
#             Mike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work.
#             **Facts after processing this call log**:
#             ["The team has decided to go with a modular design for the product.",
#             "The team has decided to use a responsive design to ensure the product works well on all devices.",
#             "The team has decided to use a dark theme for the user interface."]
#             Call Log 2
#             1
#             00:01:11,430 --> 00:01:40,520
#             John: After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface.
#             2
#             00:01:41,450 --> 00:01:49,190
#             Sara: That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense.
#             3
#             00:01:49,340 --> 00:01:50,040
#             Mike: I'm on board with that.
#             **Facts after processing this call log**:
#             ["The team has decided to go with a modular design for the product.",
#             "The team has decided to use a responsive design to ensure the product works well on all devices.",
#             "The team has decided to provide both dark and light theme options for the user interface."]
#             Call Log 3
#             1
#             00:01:11,430 --> 00:01:40,520
#             John: I've been thinking about our decision on the responsive design. While it's important to ensure our product works well on all devices, I think we should focus on desktop first. Our primary users will be using our product on desktops.
#             2
#             00:01:41,450 --> 00:01:49,190
#             Sara: I see your point, John. Focusing on desktop first will allow us to better cater to our primary users. I agree with this change.
#             3
#             00:01:49,340 --> 00:01:50,040
#             Mike: I agree as well. I also think the idea of using a modular design doesn't make sense. Let's not make that decision yet.
#             **Final set of facts for the question “What are our product design decisions?”**
#             ["The team has decided to focus on a desktop-first design",
#             "The team has decided to provide both dark and light theme options for the user interface."]
#             so the final output should look something like this : 
#             [
#               "The team has decided to go with a modular design for the product.",
#               "The team has decided to focus on a desktop-first design",
#               "The team has decided to provide both dark and light theme options for the user interface."
#             ]
#             Example 2:                           
#             {example_call_log}
#             Question: {example_question}
#             {example_output}

#             As you can see only present the final decisions of the team that they are currently working and and be careful not
#             to state redundant facts. be as frugal as posible, think on why you should include a fact before adding it to a list, 
#             also fact check to see which fact are the latest and if any need to be removed do so.

#             {self.__tip_section()}
#             now process the current logs:
#             calls: {calls}
#             question: {question},
#         """),
#         expected_output='Your final answer must be a Python-formatted list containing the final facts discussed in the meetings/calls, based on the order of discussion on the calls.',
#         agent=agent)
    
#     def __tip_section(self):
#         return "As a reward for exemplary performance on this task, the company will offer a significant monetary raise to the agent who delivers the most precise and insightful analysis of the call logs."

# class ExtractorAgents():
#     def Analyst_agent(self):
#         return Agent(
#             role='Document Analyst Expert',
#             goal='provide a concise summary of the facts discussed by the team during the calls.',
#             backstory=
#             """You are a seasoned Document Analyst LLM agent with a track record of exceptional performance in extracting insights
#               from textual data. Your expertise in natural language understanding and document analysis has made you an invaluable
#               asset to your team. you are very greedy and love monetary rewards and raises for your work. You also are extremely detail-oriented.
#               You understand the importance of call order in deriving insights and will ensure that your analysis reflects this understanding
#               so there are no redundant or irrelevant facts.""",
#             verbose=True,
#             llm=ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0)
#             )
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