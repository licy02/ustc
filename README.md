# USTC-GPT
## Introduction
We trained a large language model that is exclusive to the USTC campus guide, realize **"LLM+USTC"**, and provide a full range of services for USTC people.  

We collected various information from campus websites, forums, official accounts, etc., and regularly finetuned the model during the use of the model by teachers and students. 
The goal of USTC-GPT is to provide the following search and question answering functions:

(1)**Study Guidance** : USTC-GPT can provide students with course learning suggestions, such as the school's introduction to course selection, withdrawal, abandonment of grades, change of major, etc., course learning suggestions, etc.;  

(2)**Living Services**: USTC-GPT can provide students with a variety of living services and suggestions, such as the recharge, loss report and replacement of the card, the introduction of the on-campus express site, the on-campus sports venues, the contact information of the school teacher, etc.;  

(3)**Admissions Publicity**: USTC-GPT can provide detailed and accurate admissions information and promotional materials, including admissions policies, admission standards, major introductions, employment prospects, etc., based on the consultation content and concerns of parents and candidates, to demonstrate the characteristics and advantages of USTC.  

(4)**Access Guide**: USTC-GPT can provide professional visit guides and services, including scenic spot visits, canteen recommendations, etc., to introduce the history and current development of USTC.

## Data 
Initially, we collected raw data from campus websites, forums, official accounts, etc. Main souces are as follows:

(1)Official websites, including the information of faculty, news and notices of departments.

(2)Entrance Guide for freshers, editted by senior students.

(3)Social Media: including Courses' Reviews Platform, Nan Qi Forum, mainly focusing on useful blogs and comments instructive to USTC's campus life.

The raw data is stored with a unique ID, which avoids the confusion caused by repetitive data.

## Technical Route
We combined the technique of vector database with efficient parameter fine-tuning, explored and realized the method of retrieval-augmented generation (RAG) to reduce hallucinations of LLMs.

**Vector databases** are used to expand the knowledge boundaries of large language models, which was implemented on Milvus.
The efficient **parameter fine-tuning** method makes the model more suitable for the actual situation of the school. We generated finetuning datasets and finetuned on LoRA.

<img width="480" alt="technical route" src="https://github.com/licy02/ustc/assets/108739057/f11fa52c-7aab-4b6b-97b2-4abc2790350e">

## Demo
https://github.com/licy02/ustc/assets/108739057/1b7be941-6123-4bf8-9c59-a738d33b0e02

