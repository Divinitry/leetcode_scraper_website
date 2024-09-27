from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def get_feedback(leetcode_question, user_code, leetcode_question_topics):
    prompt = f"""
        Analyze the following LeetCode problem the user is trying to solve: "{leetcode_question}".
        Evaluate the user's code: "{user_code}".

        If the code has no relevance to the LeetCode problem, respond with: 
        "Nice code, but it seems unrelated to the question." 
        (Skip the remaining steps if this is the case. Continue only if the code seems relevant to the problem.)

        Indicate whether the user's code correctly answers the problem. Respond with: 
        "Answered question correctly: yes/no."

        Based on the problem's topics (e.g., strings, linked lists, recursion, array, two pointers), identify specific areas in the user's code related to these topics where improvement is needed. Here are the topics: {leetcode_question_topics}.

        Focus on the user's implementation, including the efficiency of the algorithm, the use of data structures, and whether they applied the correct approach for solving the problem. Highlight key aspects like time complexity, space complexity, and common mistakes users make when implementing the solution.

        Provide a rating between 1 and 10 based on how well the code addresses the problem. Explicitly return this number at the end as "Rating: X".

        Structure the response into two sections: 
        - A paragraph focused on feedback related to the user's coding approach and performance on the problem.
        - A separate line for the rating in the format: "Rating: X"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that reviews code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        print("Full response from OpenAI:", response)

        chatgpt_response = response.choices[0].message.content

        feedback = chatgpt_response.split("Rating:")[0].strip()
        rating = chatgpt_response.split("Rating:")[1].strip() if "Rating:" in chatgpt_response else "No rating provided"

        if rating == "N/A":
            rating = 0

        return feedback, rating

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def get_start_code(code_body):
    prompt = f"""
        You are given a coding problem statement. Based on this problem, generate function signatures with placeholders for the solution code and example test cases. Each language should follow the standard signature format for that language (e.g., including docstrings for Python, public methods for Java, etc.). The output should include:

        - The function signature, tailored to the specific language.
        - A placeholder comment ('// Your code here', '# Your code here', etc.) appropriate for each language.
        - Example test cases with inputs and expected outputs.

        Please generate this for the following languages: JavaScript, TypeScript, Python, Java, and C#.

        Here is the coding problem:

        {code_body}

        Please ensure the following:
        - Do not include the name of the language anywhere in the output.
        - Do not include headings or additional explanations, just the code.
        - Separate each language block with "***", so I can easily split them later.
        - Ensure function signatures and example test cases are formatted as executable code in each respective language.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that reviews code."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000  
    )

    chatgpt_response = response.choices[0].message.content
    
    sections = chatgpt_response.split('***')

    javascript_startercode = sections[0].strip()
    typescript_startercode = sections[1].strip()
    python_startercode = sections[2].strip()
    java_startercode = sections[3].strip()
    csharp_startercode = sections[4].strip()

    return javascript_startercode, typescript_startercode, python_startercode, java_startercode, csharp_startercode