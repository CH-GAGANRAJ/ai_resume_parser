import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import json
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash',google_api_key=GOOGLE_API_KEY)

# The Function which takes resume as text and give LLM Suggestions and return json responce
def llm_suggestion(text):
    response = llm.invoke("""I will provide you with the plain text of a resume. Your task is to extract specific information , Give resume rating , Give Improvements areas and upskill suggestions and present it in a structured JSON format.\n Here is the resume text: %s \n Please provide the output in the following JSON format. If a field cannot be extracted, use an empty string for string fields, an empty list for list fields, and 0 for numerical fields.\n
```json
{
“name”: “...”,
“email”: “...”,
“core_skills”: [ “java”, “react”]
“soft_skills”: [“hardworking”, “team player” ],
“resume_rating”: 8,
“improvement_areas”: “...”,
“upskill_suggestions”: “...”
}
```
"""%(text))
    #print(response.content[7:-3])
    return json.loads(response.content[7:-3])

if __name__=='__main__':
    t="""JOHN DOE
123 Main Street, Anytown, USA | (555) 123-4567 | john.doe@email.com

SUMMARY
Highly motivated software engineer with 5+ years of experience...

EXPERIENCE
Software Engineer | Tech Solutions Inc. | Anytown, USA
Jan 2022 - Present
* Developed and maintained web applications using Python and Django.
* Implemented RESTful APIs for mobile integration.

EDUCATION
B.S. in Computer Science | University of Nowhere | 2021"""
    llm_suggestion(t)