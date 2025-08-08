from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers.pipelines.text_generation import TextGenerationPipeline
from torch import torch
import os

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
    # ? loading model directly

    # """
    # model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="autio", trust_remote_code=True, device_map=device).to(device)
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # """

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
        {chunk}
        ```
        
        **Only return the tasks in this structured format:**
        
        | Task Name | Task Percentage | Description | Deadline | Type |
        |-----------|-----------------|-------------|----------|------|
        | Example Task | 10% | Write a report | March 5 | Task 


        """
        
        messages = [
            [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": """ 
        You are an AI assistant that extracts tasks from documents. Identify all tasks, task percentages, descriptions, and deadlines from the document below.
        
        - If a task does not have a percentage, deadline, or description, return 'N/A'.
        - List any milestones or deliverables associated with each task.
        - If there is a list of labs, put each one seperately
        - Make sure to add Tasks, Labs, Tests, Quizzes, Midterms, and Exams seperately
                                
        **Only return the tasks in this structured format:**
        
        | Task Name | Task Percentage | Description | Deadline | Type |
        |-----------|-----------------|-------------|----------|------|
        | Example Task | 10% | Write a report | March 5 | Task """},]
                },
                
                {
                    "role": "user",
                    "content": [{"type": "text", "text": content},]
                },
            ],
        ]


        # prompt = pipe.tokenizer.apply_chat_template(messages, add_generation_prompt=False)
        
        results = pipe(messages, max_new_tokens=256)


        # print(content)
        # results = pipe(content, max_new_tokens=1024, do_sample=False)


        # print(results)
        
        total_results.append(results[0][0]["generated_text"][2]["content"])
        # total_results += (results[0]["generated_text"]) # returns output from the model
    
    return "\n".join(total_results)


# result = generate_tasks("""
#   "**APS360** **Applied Fundamentals of Deep Learning** **Summer 2024**\n\n\n**Overview**\n\n\nThis course is a hands-on introduction to deep learning. By the end of the course, you will be able to\nimplement deep neural networks to classify images, text, graphs, and other types of data. You will also be\nable to implement deep neural network to generate images and text. Moreover, you will learn how to apply\ntricks to train deep models efficiently, how to debug them, how to train your models without having access\nto human annotations, and how to train your deep models on small data. We will focus on implementing\ndeep neural networks in Python, using Numpy and PyTorch libraries.\n\n\n**Course Material**\n\n\n[You will need to log into Quercus with your UTORid to gain access to course material, and obtain regular](https://q.utoronto.ca)\ncourse information (e.g., downloading lecture materials, lab handouts, project information, etc.), submit\nwork, receive grade/feedback and email announcements.\n\n\n**Course Sections**\n\n\nStudents are expected to fully participate and attend all lectures and practical sessions for the duration of\nthe course. Lectures, tutorials, and labs will be online (see Zoom Meeting Links Section).\n\n\n**Section** **Instructor** **Lecture** 2 **Tutorial** 2 **Lab** 3 **Office Hours**\n\n\n**LEC101** Kaveh Mon 6–8pm Wed 6–7pm Wed 7–8pm Mon 11am–12pm\nHassani (by appointment)\n**LEC102** Justin Mon 6–8pm Wed 6–7pm Wed 7–8pm Mon 10am–11am\nBeland (by appointment)\n\n\n3\nOffice hours are **by prior appointment only** . 2 Tutorials and Labs will be taught by TAs.\n\n\n**Course Staff**\n\n\n**Instructors** Kaveh Hassani – `kaveh.hassani@utoronto.ca`\n\nJustin Beland – `justin.beland@mail.utoronto.ca`\n\n\n**Contact** For non-personal, course-related questions, please use our posted\noffice hours, or ask your TAs and peers on Piazza. Otherwise, email the instructor and use “[APS360]:” as the prefix of the subject.\n\n\n**Head Teaching Assistants** Gianluca Villani – `gianluca.villani@mail.utoronto.ca`\nMustafa Ammous – `mustafa.ammous@mail.utoronto.ca`\n\n\n**Teaching Assistants** Pedram Mouseli – `pedram.mouseli@mail.utoronto.ca`\nVida Adeli Mosabbeb – `vida.adeli@mail.utoronto.ca`\n\nSrinath Dama – `srinath.dama@mail.utoronto.ca`\n\nShiva Akbari – `shiva.akbari@mail.utoronto.ca`\n\nLoghman Moradi – `loghman.moradi@mail.utoronto.ca`\nAli Tohidifar – `ali.tohidifar@mail.utoronto.ca`\n\nSaeede Hasanpoor – `saeede.hasanpoor@utoronto.ca`\nEnsieh Khazaei – `ensieh.khazaei@mail.utoronto.ca`\n\nMojgan Faramarzi – `mozhgan.faramarzi@mail.utoronto.ca`\nSaba Ale Ebrahim – `saba.aleebrahim@mail.utoronto.ca`\n\n\nUniversity of Toronto Faculty of Applied Science and Engineering Page 1 of 5\n\n\n**APS360** **Applied Fundamentals of Deep Learning** **Summer 2024**\n\n\n**Textbook and Supplementary Materials**\n\n\nThere is no textbook required for the course. If you wish to refer to a textbook, the following publicly\navailable books are recommended:\n\n\n_•_ [Dive into Deep Learning by Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola](https://d2l.ai/)\n\n_•_ [Deep Learning by Ian Goodfellow and Yoshua Bengio and Aaron Courville](https://www.deeplearningbook.org)\n\n_•_ Course notes for the topic of _Ethics and Fairness_ [will be provided on the course website.](https://q.utoronto.ca)\n\n\n**Communication**\n\n\n_•_ Use Piazza for non-personal, course-related questions. This allows your peers to also learn from your\nanswers, and avoids us answering the same questions several times.\n\n_•_ Piazza questions will be answered by instructors or TAs on Monday-Friday between 9:00am-5:00pm.\nQuestions asked over the weekends, holidays, or after hours will be answered the following regular day.\n\n_•_ Lecture slides will be released on the same week of the lecture. This may be early or late that week,\ndepending on the required modifications.\n\n\n**Schedule**\n\n\nAll lectures, toturials, and labs will be over Zoom. You need to use licensed Zoom for University of Toronto\n[and login with your UTORid and password. For detailed instructions how to use Zoom see this link.](https://utm.library.utoronto.ca/students/canvas/zoom)\n\n\n**Weeks** **Lecture** **Tutorial** **Lab**\n\n\nMay 6 Introduction **No Tutorial** **No Lab**\n\n\nMay 13 Artificial Neural Networks - Data Visualization **No Lab**\nPart I\n\n\nMay 20 **No Lecture (Victoria Day)** **No Tutorial** **No Lab**\n\n\nMay 27 Artificial Neural Networks - Forward-Pass Lab 1: Introduction to Pytorch\nPart II\n\n\nJune 3 Convolutional Neural Networks MNIST Classification **No Lab**\n\n      - Part I\n\n\nJune 10 Convolutional Neural Networks CNN Kernels Lab 2: Cats/Dogs Classification\n\n      - Part II\n\n\nJune 17 **No Lecture (Course Break)** **No Tutorial** **No Lab**\n\n\nJune 24 Unsupervised Learning Transfer Learning Lab 3: Hand Gesture Recognition\n\n\nJuly 1 **No Lecture (Canada Day)** **No Tutorial** **No Lab**\n\n\nJuly 8 Recurrent Neural Networks - **No Tutorial** Lab 4: Data Imputation\nPart I\n\n\nJuly 15 Recurrent Neural Networks - Autoencoders **No Lab**\nPart II\n\n\nJuly 22 Generative Adversarial Recurrent Neural Networks Lab 5: Spam Detection\nNetworks\n\n\nJuly 29 Transformers Generative Recurrent Neural Project Support\nNetworks\n\n\nAug 5 **No Lecture (Civic Holiday)** **No Tutorial** Project Support\n\n\nAug 12 Graph Neural Networks Generative Adversarial Project Support\nNetworks\n\n\nUniversity of Toronto Faculty of Applied Science and Engineering Page 2 of 5\n\n\n**APS360** **Applied Fundamentals of Deep Learning** **Summer 2024**\n\n\n**Zoom Meeting Links**\n\n\n**Lectures, Tutorials and Labs**\n[LEC101 – LEC101 Zoom Link – Meeting ID: 859 8103 1378 – Passcode: @PS360@DL](https://utoronto.zoom.us/j/85981031378 )\n[LEC102 – LEC102 Zoom Link – Meeting ID: 811 1011 1553 – Passcode: 207399](https://utoronto.zoom.us/j/81110111553)\n\n\n**Evaluation**\n\n\nThe evaluation for this course is as follows. Note that exams are **Type X Open book** . Students may bring\nand use any books, notes, or printed or written material, without restriction. That means you are allowed\nto bring in anything you want on paper but the only digital device allowed is non-programmable calculator.\n\n\n**Work** **Weight**\n\n\nLab Assignments 10%\nMidterm (open book) 15%\nProject 40%\nFinal Examination [1] (open book) 35%\n\n\n1 Note that the Final Examination is mandatory and will result in an **F** on your transcript if not attempted.\n\n\n**Lab**\n\n\nA key part of the learning in this course is the hands-on programming labs. The scheduled lab time will\nprovide time to work on and receive TA help on the lab exercises. There are 5 labs which must be completed\nindividually. The weighting of the labs are as follows:\n\n\n**Lab** **Weight** **Deadline**\n\n\nLab 1 1% Thursday, May 30 at 11:59 PM\nLab 2 2% Thursday, June 13 at 11:59 PM\nLab 3 3% Thursday, June 27 at 11:59 PM\nLab 4 2% Thursday, July 11 at 11:59 PM\nLab 5 2% Thursday, July 25 at 11:59 PM\n\n\n**Project**\n\n\nThe project in this course will require students to implement a major piece of software that makes use of\nthe material of the course to develop a deep learning application. It is a substantial focus of the second half\nof this course. The project will be done in **teams of four**, and will account for **40%** of your final grade.\nThere are several phases and specific deadlines of the project, with several interim deliverable due dates, a\npreliminary schedule follows:\n\n\n**Deliverable** **Weight** **Deadline**\n\n\nTeam Formation 0% Thursday, May 23 at 11:59 PM\nProject Proposal 5% Thursday, June 6 at 11:59 PM\nProgress Report 5% Thursday, July 4 at 11:59 PM\nProject Presentation 10% Thursday, Aug 15 at 11:59 PM\nFinal Deliverable 20% Thursday, Aug 15 at 11:59 PM\n\n\n**Late Work Policy**\n\n\nLate submissions will be accepted up to 24 hours past the deadline with a **20%** grade deduction. Quercus\nsubmission time will be used, not your local computer time. You can submit your labs as many times as you\nwant before the deadline, so please submit often and early. No other late work will be accepted, however,\nwe will consider exceptional cases on a case-by-case basis, such as with a doctor’s note in the case of illness.\n\n\nUniversity of Toronto Faculty of Applied Science and Engineering Page 3 of 5\n\n\n**APS360** **Applied Fundamentals of Deep Learning** **Summer 2024**\n\n\n**Valid Petitions**\n\n\nThe weight of valid petitions will be moved to the final exam without any exceptions. Please do not request\ndeadline extensions for petitions as it will not be considered.\n\n\n**Midterm**\n\n\nThe midterm will take place on June 25 from 12:01 am to 11:59pm. You will have a period of 24 hours in\nwhich you can start the exam, but once it started you will need to complete it in 2 hours. The exam will be\n[through CrowdMark.](https://crowdmark.com/)\n\n\n**Use of TurnItIn**\n\n\nTurnitin.com will be used to assist in the evaluation of the originality of some of the term work. Turnitin.com\nis only a tool which will assist in detecting plagiarism. Normally, students will be required to submit their\ncourse essays to Turnitin.com for a review of textual similarity and detection of possible plagiarism. In\ndoing so, students will allow their essays to be included as source documents in the Turnitin.com reference\ndatabase, where they will be used solely for the purpose of detecting plagiarism. The terms that apply to the\nUniversity’s use of the Turnitin.com service are described on the Turnitin.com web site - http://turnitin.com/.\n\n\n**Accessibility**\n\n\nThe University of Toronto and your instructors are committed to accessibility. If you require accommodations, or there is anything course-related we can do to help, please get in touch.\n\n\n**Academic Offenses**\n\n\nThe University of Toronto expects you to be a full member of the academic community and to observe the\nrules and conventions of academic discourse. In particular, all of the work you submit must be your own\nand your work must not be submitted by someone else. Plagiarism is a form of academic fraud, and the\ndepartment uses software that compares submissions for evidence of similarity. The full text of the policy\nthat governs Academic Integrity at U of T (the “Code of Behaviour on Academic Matters”) can be found\n\nat:\n\n```\n       https://www.governingcouncil.utoronto.ca/policies/behaveac.htm\n\n```\n\nPlease don’t cheat. It is unpleasant for everyone involved, including us. Here are a couple of general\nguidelines to help you avoid plagiarism:\n\n\n_•_ Never look at another student’s homework. Never show another student your solution. This applies to\nall drafts of a solution and to incomplete and even incorrect solutions.\n\n_•_ Keep discussions with other students focused on _concepts_ and _examples_ . Any code or solutions that you\nsubmit should be your alone.\n\n_•_ Do not post any of your assignment questions in a private or public online discussion forum or website\nin order to solicit solutions from others.\n\n\nNote that, under the University of Toronto code of conduct, a person who supplies an assignment to be\ncopied will be penalized in the same way as the one who makes the copy. We will use software to detect\ncopying that is quite sophisticated and so is difficult to defeat.\n\n\n**Some Frequent Questions**\n\n\n**1– My teammate(s) dropped the course last minute, can we get an extension?**\n**No**, the goal is simulate real-world industrial experience where your colleagues may resign before the\ndelivery date!\n**2– While uploading my answers to CrowdMark I faced a technical issue, can I email my answers**\n**to you? No**, out of 120 minutes, 90 minutes is for answering questions and 30 minutes for uploading your\n\n\nUniversity of Toronto Faculty of Applied Science and Engineering Page 4 of 5\n\n\n**APS360** **Applied Fundamentals of Deep Learning** **Summer 2024**\n\n\nanswers. You should be able to fix the issue.\n**3– After uploading my answers to CrowdMark I realized I had uploaded wrong files, can I**\n**email my answers to you? No**, out of 120 minutes, 90 minutes is for answering questions and 30 minutes\nfor uploading your answers. You should double check your submission in that 30 minutes.\n**2– I have two midterms next week, can I extend the deadline for lab submission?**\n**No**, the schedule is announced at the start of semester to let you plan in advance.\n**3– I uploaded my assignment on-time, however I realized that the link to my code is bro-**\n**ken/private so TA couldn’t access it. Can I update the link if I can prove it hasn’t changed**\n**since the deadline?**\n\n**No**, you are responsible to double-check that everything is working before the deadline.\n**4– Can a team have members across sections?**\n\n**Yes** .\n\n\nUniversity of Toronto Faculty of Applied Science and Engineering Page 5 of 5\n\n\n"
# """)

# print(result)