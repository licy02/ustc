# USTC-GPT
## Introduction
We trained a large language model that is exclusive to the USTC campus guide, realize **"LLM+USTC"**, and provide a full range of services for USTC people.  

We collected a large amount of information that exists on campus websites, forums, official accounts, etc., and regularly optimized the model during the use of the model by teachers and students. 
The goal of the research is that USTC-GPT can become an intelligent assistant and loyal partner of USTC people, and provide the following search and question answering functions:

(1)**Study Guidance** : USTC-GPT can provide students with course learning suggestions, such as the school's introduction to course selection, withdrawal, abandonment of grades, change of major, etc., course learning suggestions, etc.;  

(2)**Living Services**: USTC-GPT can provide students with a variety of living services and suggestions, such as the recharge, loss report and replacement of the card, the introduction of the on-campus express site, the on-campus sports venues, the contact information of the school teacher, etc.;  

(3)**Admissions Publicity**: USTC-GPT can provide detailed and accurate admissions information and promotional materials, including admissions policies, admission standards, major introductions, employment prospects, etc., based on the consultation content and concerns of parents and candidates, to demonstrate the characteristics and advantages of USTC.  

(4)**Access Guide**: USTC-GPT can provide professional visit guides and services, including scenic spot visits, canteen recommendations, etc., to introduce the history and current development of USTC.

## Data 
(1)**Official websites**, including the website of every department, the Academic Affairs Office, Treasury Division etc., mainly focusing on the introduction, faculty, news and notices.

(2)**Entrance Guide** for fresh students, editted by several senior students.

(3)**Social Media**: including Courses' Reviews Platform(评课社区)，Nan Qi Teapot(南七茶馆), zhihu, mainly focusing on useful blogs and comments related to USTC's campus life.

## Technical Route
Combined with vector database and efficient parameter fine-tuning, explored and realized the method of retrieval-augmented generation (RAG) to reduce hallucinations of LLMs.

**Vector databases** (Milvus) are used to expand the knowledge boundaries of large language models.
The efficient **parameter fine-tuning** method is used to make the model more suitable for the actual situation of the school.

<img width="480" alt="technical route" src="https://github.com/licy02/ustc/assets/108739057/f11fa52c-7aab-4b6b-97b2-4abc2790350e">

## Demo
https://github.com/licy02/ustc/assets/108739057/1b7be941-6123-4bf8-9c59-a738d33b0e02

