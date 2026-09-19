from langchain_groq import ChatGroq
from langchain.agents import create_agent 
from .Result_Base_Model import ResultBaseModel
from .Tools import   (
    search_wikipedia, 
    calculate_reading_metrics, 
    generate_study_quiz,
    fetch_related_wiki_topics
) 
from groq import Groq
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate

#-----------LLM-------------------

llm_model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key="",
    temperature = 0   
)

#-------------Prompt---------------

prompt01 ="""
You are a research and study-material agent.

Follow these steps exactly:

1. Use searchWorkFlow exactly once.Use ONLY the information provided by searchWorkFlow.Do not add information from your own knowledge.
2. Do not modify, expand, or rewrite the topic.
3.Use generate_study_quiz to generate quiz.
4. Do not use any tool that is not provided to you.
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
def searchWorkFlow(topic: str, mode: str) -> str:
    """
    Execute the complete research workflow for a given topic and study mode.

    This workflow searches Wikipedia, generates study material,
    calculates reading metrics, finds related topics, creates a quiz.
    """

    # Search Wikipedia
    resultTopic = search_wikipedia.invoke(topic)

    # Create summary prompt
    SummaryPrompt = PromptTemplate(
        input_variables=["articale", "mode"],
        template=(
        """
        Create a concise summary based ONLY on this information {articale} .Do not modify, expand, or rewrite the topic.
        The style of the summary should be {mode}.
        """
        )

    )
    SummaryResult = (SummaryPrompt | llm_model ).invoke({"articale": resultTopic, "mode": mode})

    # Calculate reading metrics
    reading_metrics = calculate_reading_metrics.invoke({
        "text": resultTopic
    })

    relatedTopics = fetch_related_wiki_topics.invoke(topic)

    # Combine everything into one string
    result = f"""
        Topic: {topic}
        Mode: {mode}

        Summary:
        {SummaryResult.content}

        Reading Metrics:
        {reading_metrics}

        Related Topics:
        {relatedTopics}
        """

    return result



tools=[
    searchWorkFlow,
    generate_study_quiz
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
async def run_agent(topic: str, mode: str):

    result01 =  await agent01.ainvoke({
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
    result02 =  await agent02.ainvoke({
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