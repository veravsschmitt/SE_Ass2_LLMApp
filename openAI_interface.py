import json
import PyPDF2
from openai import OpenAI
import time
from datetime import datetime


# Insert your API-Key for OpenAI here
openAIkey = ""



class LLM_Interact():
    
    def __init__(self):
        
        self.questions = [""]
        
        with open('general_context.json', 'r', encoding='utf-8') as f:
            self.general_context = json.load(f)
        
        with open('question_context.json', 'r', encoding='utf-8') as f:
            self.question_context = json.load(f)
            
        with open('answer_context.json', 'r', encoding='utf-8') as f:
            self.answer_context = json.load(f)
            
        with open('hint_context.json', 'r', encoding='utf-8') as f:
            self.hint_context = json.load(f)
            
        self.client = OpenAI(api_key = openAIkey)

            
        
    def set_study_notes(self, study_notes_path):
        
        self.study_notes = extract_text_from_pdf(study_notes_path)
        
    def get_new_question(self):
        
        prompt = (
            json.dumps(self.general_context) + "\n\n" +     
            "STUDY NOTES:\n" + self.study_notes + "\n\n" + 
            json.dumps(self.question_context) + "\n\n" +    
            "PREVIOUS QUESTIONS:\n" + "\n".join(self.questions)  
        )
        
        start_time = time.time()
        start_time_readable = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"sendeing prompt for question, time: {start_time_readable}")
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        
        end_time = time.time()
        end_time_readable = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"reponse got, time: {end_time_readable}")
        
        print_metrics(start_time, end_time, response)

        new_question = response.choices[0].message.content
        self.questions.append(new_question)
        return new_question
    
        
    def check_answer(self, question, answer):
        
        prompt = (
            json.dumps(self.general_context) + "\n\n" +
            "STUDY NOTES:\n" + self.study_notes + "\n\n" +
            json.dumps(self.answer_context) + "\n\n" +
            f"QUESTION:\n{question}\n\n" +
            f"ANSWER:\n{answer}"
        )
        
        start_time = time.time()
        start_time_readable = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"sendeing prompt for answer checking, time: {start_time_readable}")
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        
        end_time = time.time()
        end_time_readable = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"reponse got, time: {end_time_readable}")
        
        print_metrics(start_time, end_time, response)
        
        checked_answer = response.choices[0].message.content
        return checked_answer
        
    def get_hint(self,question):
        
        prompt = (
            json.dumps(self.general_context) + "\n\n" +
            "STUDY NOTES:\n" + self.study_notes + "\n\n" +
            json.dumps(self.hint_context) + "\n\n" +
            f"QUESTION:\n{question}"
        )
        
        start_time = time.time()
        start_time_readable = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"sendeing prompt for hint, time: {start_time_readable}")
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        
        end_time = time.time()
        end_time_readable = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"reponse got, time: {end_time_readable}")
        print_metrics(start_time, end_time, response)
        
        hint = response.choices[0].message.content
        return hint

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text
        
def print_metrics(start_time,end_time, response):
    
    latency = end_time - start_time
    
    usage = getattr(response, "usage", None)

    if usage:
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        cost = getattr(usage, "total_cost", "N/A")  # unfortunately I couldn't get the costs
    else:
        prompt_tokens = completion_tokens = total_tokens = cost = "N/A"

    print("\n=== TELEMETRY ===")
    print(f"Latency:        {latency:.3f} s")
    print(f"Prompt tokens:  {prompt_tokens}")
    print(f"Answer tokens:  {completion_tokens}")
    print(f"Total tokens:   {total_tokens}")
    print(f"Cost:           {cost}")
    print("=================\n")
