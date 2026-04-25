import google.generativeai as genai
import os

# We will load our API key from a .env file later for security
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# We'll use the flash model because it's fast and cheap!
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_interview_questions(role_name, skills_needed):
    """
    Takes a job role and skills, and asks Gemini to generate 3 interview questions.
    """
    prompt = f"""
    You are an expert technical interviewer. 
    I am a candidate applying for the role of {role_name}. 
    The skills required are: {skills_needed}.
    
    Please generate 3 specific interview questions for me. 
    Make one behavioral, one technical, and one about past experience.
    Return ONLY the questions, separated by a new line. No intro, no outro.
    """
    
    response = model.generate_content(prompt)
    
    # Gemini returns a text block, we'll split it by newlines into a python list
    questions = response.text.strip().split('\n')
    
    # Clean up any empty lines
    return [q.strip() for q in questions if q.strip()]

def evaluate_answer(question_text, user_answer):
    """
    Takes a question and a user's answer, and asks Gemini to score it out of 10 and provide feedback.
    """
    prompt = f"""
    You are an expert technical interviewer.
    I was asked this question: "{question_text}"
    My answer was: "{user_answer}"
    
    Please evaluate my answer. 
    1. Give me a score out of 10.
    2. Give me 2-3 sentences of actionable feedback on how I can improve.
    
    Return your response strictly in this format:
    Score: [number]
    Feedback: [your feedback]
    """
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    # Simple logic to parse the 'Score: 8\nFeedback: great job' format
    score = None
    feedback = response_text
    
    try:
        lines = response_text.split('\n')
        for line in lines:
            if line.startswith("Score:"):
                # Extract just the number
                score = int(''.join(filter(str.isdigit, line)))
            elif line.startswith("Feedback:"):
                feedback = line.replace("Feedback:", "").strip()
    except Exception as e:
        print("Parsing error:", e)
        
    return score, feedback
