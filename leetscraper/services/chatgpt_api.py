from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)


def get_feedback(leetcode_question, user_code, leetcode_question_topics):
    prompt = f"""
        Analyze the following LeetCode problem the user is trying to solve: {leetcode_question}.
        Evaluate the user's code for the problem: {user_code}.

        If the code has no relevance to the LeetCode problem, respond with: 
        "Nice code, but it seems unrelated to the question." 
        (Skip the remaining steps if this is the case. Continue only if the code seems relevant to the problem.)

        Indicate whether the user's code correctly answers the problem. Respond with: 
        "Answered question correctly: yes/no."

        Based on the problem's topics (e.g., strings, linked lists, recursion, array, two pointers), identify common challenges users face with these topics. Highlight the areas where the user may need more practice. Here are the topics: {leetcode_question_topics}.

        Provide a rating between 1 and 10 based on how well the code addresses the problem. Explicitly return this number at the end as "Rating: X".

        Offer detailed feedback on the code, pointing out strengths and areas for improvement. Include any common mistakes that users typically make on this particular problem, and highlight if the user shows these issues in their code.

        Structure the response into two sections: 
        - A paragraph with the feedback
        - A separate line for the rating in the format: "Rating: X"
    """

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that reviews code."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=300)

    chatgpt_response = response.choices[0].message.content.split("Rating:")
    feedback = chatgpt_response[0].strip()
    rating = chatgpt_response[1].strip() if len(chatgpt_response) > 1 else "" 

    return feedback, rating
