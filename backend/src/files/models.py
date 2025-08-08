from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers.pipelines.text_generation import TextGenerationPipeline
from torch import torch
import os
from dotenv import load_dotenv
import time


# gets the HUGGING_FACE API key
load_dotenv()
login(token=os.getenv("HUGGING_FACE"))

model_name = "google/gemma-3-1b-it" # can use gpt2 as well
device = "mps" # use auto for ideal performance
# mps, cpu, gpu are also options


def chunk_text(text: str, max_tokens: int = 1024) -> list[str]:
    # this function breaks down the full pdf into chunks to be used by the model and then re
    words = text.split() 
    chunks: list[str] = []
    
    for i in range (0, len(words), max_tokens):
        chunk = " ".join(words[i:i+max_tokens])
        chunks.append(chunk)
    return chunks
    


def generate_tasks(document_text: str) -> str:
    
    start_time = time.time()
    
    # # ? pipeline
    pipe: TextGenerationPipeline = pipeline("text-generation", model=model_name, device=device, torch_dtype=torch.bfloat16)



    chunks = chunk_text(document_text, 800)
    
    total_results = []
    for chunk in chunks:
            
        # create prompt
        content: str = f"""
		You are an AI assistant that extracts tasks from documents. 
		Identify all tasks, task percentages, descriptions, and deadlines from the document below.
		
		- If a task does not have a percentage, deadline, or description, return 'N/A'.
		- List any milestones or deliverables associated with each task.
        - If there is a list of labs, put each one seperately
        - Make sure to add Tasks, Labs, Tests, Quizzes, Midterms, and Exams seperately
		
		Document:
		```
		{document_text}
		```
		
		**Return in this structured format:**
		
		| Task Name | Task Percentage | Description | Deadline | Type |
		|-----------|-----------------|-------------|----------|------|
		| Example Task | 10% | Write a report | March 5 | Task 

		**DO NOT RETURN ANYTHING ELSE**

		"""
        
        messages = [
            [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": """
				You are an AI assistant that extracts tasks from documents. 
		Identify all tasks, task percentages, descriptions, and deadlines from the document below.
		
		- If a task does not have a percentage, deadline, or description, return 'N/A'.
		- List any milestones or deliverables associated with each task.
        - If there is a list of labs, put each one seperately
        - Make sure to add Tasks, Labs, Tests, Quizzes, Midterms, and Exams seperately
		

		**Return in this structured format:**
		
		| Task Name | Task Percentage | Description | Deadline | Type |
		|-----------|-----------------|-------------|----------|------|
		| Example Task | 10% | Write a report | March 5 | Task 
  
		**DO NOT RETURN ANYTHING ELSE**
  
		"""}]
                },
                
                {
                    "role": "user",
                    "content": [{"type": "text", "text": content}]
                },
            ],
        ]

        
        results = pipe(messages)

        # print(results)

        # gets only the generated text from the AI
        """
            Gemma model returns the response as an array of objects
            0: system prompt
            1: user prompt
            2: generated text
        """
        total_results.append(results[0][0]["generated_text"][2]["content"]) # returns output from the model
    
    end_time = time.time()
        
    elapsed_time = end_time - start_time
    
    print(f"Elapsed time of Hugging Face: {elapsed_time:.4f} seconds")

    return "\n".join(total_results)


textDoc = """
Evaluation
The evaluation for this course is as follows. Note that exams are Type X Open book. Students may bring
and use any books, notes, or printed or written material, without restriction. That means you are allowed
to bring in anything you want on paper but the only digital device allowed is non-programmable calculator.
Work
Weight
Lab Assignments
10%
Midterm (open book)
15%
Project
40%
Final Examination1 (open book)
35%
1Note that the Final Examination is mandatory and will result in an F on your transcript if not attempted.
Lab
A key part of the learning in this course is the hands-on programming labs. The scheduled lab time will
provide time to work on and receive TA help on the lab exercises. There are 5 labs which must be completed
individually. The weighting of the labs are as follows:
Lab
Weight
Deadline
Lab 1
1%
Thursday, May 30 at 11:59 PM
Lab 2
2%
Thursday, June 13 at 11:59 PM
Lab 3
3%
Thursday, June 27 at 11:59 PM
Lab 4
2%
Thursday, July 11 at 11:59 PM
Lab 5
2%
Thursday, July 25 at 11:59 PM
Project
The project in this course will require students to implement a major piece of software that makes use of
the material of the course to develop a deep learning application. It is a substantial focus of the second half
of this course. The project will be done in teams of four, and will account for 40% of your final grade.
There are several phases and specific deadlines of the project, with several interim deliverable due dates, a
preliminary schedule follows:
Deliverable
Weight
Deadline
Team Formation
0%
Thursday, May 23 at 11:59 PM
Project Proposal
5%
Thursday, June 6 at 11:59 PM
Progress Report
5%
Thursday, July 4 at 11:59 PM
Project Presentation
10%
Thursday, Aug 15 at 11:59 PM
Final Deliverable
20%
Thursday, Aug 15 at 11:59 PM
Late Work Policy
Late submissions will be accepted up to 24 hours past the deadline with a 20% grade deduction. Quercus
submission time will be used, not your local computer time. You can submit your labs as many times as you
want before the deadline, so please submit often and early. No other late work will be accepted, however,
we will consider exceptional cases on a case-by-case basis, such as with a doctor’s note in the case of illness.
University of Toronto
Faculty of Applied Science and Engineering
Page 3 of 5
"""

generate_tasks(textDoc)