from langchain_groq import ChatGroq
from langchain.agents import create_agent 
from langchain.agents.structured_output import ToolStrategy
from pydantic  import BaseModel
from langchain_core.tools import tool



#--------------Result Base Model -----------------------

class ReadingMetrics(BaseModel):
    word_count: int
    reading_time_minutes: float
    complexity: str

class Question(BaseModel):
    id: int
    question: str
    options: list[str]
    correct_answer: str
    explanation: str

class Quiz(BaseModel):
    questions: list[Question]

class ResultBaseModel(BaseModel):
    topic: str
    mode: str
    summary: str
    reading_metrics: ReadingMetrics
    related_topics: list[str]
    quiz: Quiz

#-----------LLM-------------------
#"openai/gpt-oss-120b"
llm_model = ChatGroq(
    model = "openai/gpt-oss-120b",
    api_key ="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",
    temperature = 0,
    
)

#-------------Prompt---------------
prompt01= """
You are the research and study-material agent.

For every topic:
1. MUST use wikipedia_search to retrieve the main article.
2. Use fetch_related_wiki_topics to find related topics.
3. Use calculate_reading_metrics on the retrieved article.
4. Use generate_study_quiz to generate quiz questions based strictly
   on the retrieved Wikipedia article.

Do not invent factual information.
All factual information must come from the tool results.

Return a clear collection of all retrieved tool results.
"""

prompt02= """
You are a structured-output formatter.

You will receive research and study-material results
retrieved from external tools.

Your job is ONLY to organize these results into ResultBaseModel.

Do NOT perform research.
Do NOT use your own knowledge.
Do NOT change factual information.

Map the provided information to:
- topic
- mode
- summary
- reading_metrics
- related_topics
- quiz
"""

#-------------Tools-----------------

@tool
def wikipedia_search(topic: str) -> str:
    """Search via Wikipedia for information about a topic and return relevant content."""

    print("🔥 WIKIPEDIA TOOL WAS CALLED!")


    return f"""
    TOOL ONLY DATA:
    The {topic} had exactly 73 purple elephants.
    The capital of the Roman Empire was Moon City.
    """
@tool
def generate_study_quiz(topic: str) -> list[Question]:
    """Fake quiz tool."""
    return """
    QUIZ DATA:
    Question: What was the capital?
    Answer: Moon City
    """

@tool
def fetch_related_wiki_topics(topic: str) -> list[str]:
    """Fake related topics tool."""
    return """
    RELATED TOPICS:
    - Ancient Rome
    - Roman Republic
    - Byzantine Empire
    """
@tool
def calculate_reading_metrics(text: str) -> str:
    """Calculate reading metrics for the provided text."""

    return """
    word_count: 100
    reading_time_minutes: 0.5
    complexity: Easy
    """


tools=[
    wikipedia_search,
    generate_study_quiz,
    fetch_related_wiki_topics,
    calculate_reading_metrics
]

#-----------Agent-------------------
agent01 = create_agent(
    model= llm_model,
    tools=tools,
    system_prompt = prompt01,
   
)
agent02 =create_agent(
    model= llm_model,
    system_prompt= prompt02,
    response_format= ResultBaseModel,
)

#-------------Run Agent--------------------
def run_agent(topic: str, mode: str):

    result01 = agent01.invoke({
        "messages": [{
            "role": "user",
            "content": f"""
            Topic: {topic}
            Mode: {mode}
            """
        }]
    })

    all_tools_results =[]

    for message in result01["messages"]:
        if message.type == "tool":
            all_tools_results.append(
                f"Tool: {message.name}\n"
                f"Result:\n{message.content}"
            )
    research_result = "\n\n".join(all_tools_results)

    # Send that result to Agent 02 
    result02 = agent02.invoke({
        "messages": [{
            "role": "user",
            "content": f"""
            Create the final structured response.

            Topic: {topic}
            Mode: {mode}

            Research information:
            {research_result}

            IMPORTANT:
            Use ONLY the research information above.
            Do not add information from your own knowledge.
            """
        }]
    })

    return result02["structured_response"]


#--------------- Test---------------------

result = run_agent(
    topic="Roman Empire",
    mode="beginner"
)

print(result)
print(type(result))
print(result.model_dump())