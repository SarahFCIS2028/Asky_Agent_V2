import math
import wikipedia  
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# ==========================================
# TOOL 1: Wikipedia Search
# ==========================================
# LangChain already wrote the complex code for this! 
# We just tell it to grab the top 1 result and limit it to 3000 characters.

# <-- 2. Added this Name Badge so Wikipedia lets us in!

wikipedia.set_user_agent(
    "ConnectX_Summer_Training_Project/1.0 (student_project)"
)

api_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=3000 
)

wikipedia_search = WikipediaQueryRun(
    api_wrapper=api_wrapper
)


@tool
def search_wikipedia(topic: str) -> str:
    """Search Wikipedia for the exact topic provided by the user."""

    try:
        result = wikipedia_search.invoke(topic)

        if not result:
            return f"Sorry, I couldn't find information about '{topic}' on Wikipedia."

        return result

    except Exception as e:
            print(f"🔥 Wikipedia Tool Error: {type(e).__name__}: {e}")
            raise

#===========================================
# TOOL 2: Reading Time Calculator
# ==========================================
# The @tool tag tells the AI: "You are allowed to use this function!"
# The text inside the """quotes""" tells the AI *when* it should use it.


@tool
def calculate_reading_metrics(text: str) -> str:
    """Use this to calculate how many minutes it takes to read an article."""
    
    # 1. Count the words by splitting the text at every space
    words = text.split()
    word_count = len(words)
    
    # 2. Calculate minutes (assuming humans read 200 words per minute)
    # math.ceil rounds the number up so we don't get 1.5 minutes
    minutes = math.ceil(word_count / 200)

    avg_word_length = sum(len(word) for word in words) / word_count
    if avg_word_length > 6.0:
        complexity = "High"
    elif avg_word_length > 4.5:
        complexity = "Medium"
    else:
        complexity = "Low"
        
    return f"Word count: {word_count}. Estimated reading time: {minutes} minutes. Complexity: {complexity}."


# ==========================================
# TOOL 4: Study Quiz Generator
# ==========================================
@tool
def generate_study_quiz(questions: str, answers_with_explanations: str) -> str:
    """Constructs multiple-choice evaluation questions with answer keys and brief explanations grounded strictly in the retrieved article."""
    
    # We build a clean, structured layout for the assessment
    quiz = "## Comprehension Quiz\n\n"
    
    # Add the questions
    quiz += "### Questions\n"
    quiz += questions + "\n\n"
    
    # Add the answer key
    quiz += "### Answer Key & Explanations\n"
    quiz += answers_with_explanations
    
    return quiz



# ==========================================
# TOOL 5: Related Topics Fetcher
# ==========================================
@tool
def fetch_related_wiki_topics(topic: str) -> str:
    """Use this to find a list of related Wikipedia topics based on a given subject."""
    try:
        # We use the built-in wikipedia library to search for 5 related pages
        results = wikipedia.search(topic, results=5)
        
        # Remove the main topic itself from the related list if it pops up
        related = [res for res in results if res.lower() != topic.lower()]
        
        return f"Related topics for '{topic}': {', '.join(related)}"
    except Exception as e:
        return f"Could not fetch related topics: {str(e)}"