#-------------------------------------------------------------------------------
# Name:        YoButler.py
# Purpose: a birthday gift to my cousin and an experiment inspired by the autovicunabutler but better in every way
#
# Author:      Niaschim
#
# Created:     07/05/2023
# Copyright:   (c) alexa 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
import os
import shutil
import webbrowser
import textwrap
import subprocess
import ast
import traceback
from transformers import pipeline


# Create text loader objects for each file
loader1 = TextLoader('Program.txt')
loader2 = TextLoader('Python.txt')
loader3 = TextLoader('Leon.txt')

# Load documents from each loader
docs1 = loader1.load()
docs2 = loader2.load()
docs3 = loader3.load()

# Combine documents from all loaders
docs = docs1 + docs2 + docs3

# Create index from combined documents
index = VectorstoreIndexCreator().from_documents(docs)


# Define question answering chain
llm = "mpt-7b-storywriter-4bit-128g"
qa_chain = pipeline("question-answering", model="mosaicml/mpt-7b-storywriter", tokenizer="EleutherAI/gpt-neox-20b", trust_remote_code=True)


# Define variables
working_folder = "bot_working_folder"
max_iterations = 10
tried_solutions = set()

# Create working folder if it does not exist
if not os.path.exists(working_folder):
    os.mkdir(working_folder)

# Define function to summarize web content
def summarize_web_content():
    # get web content using web scraping library of your choice
    content = "some web content"
    # summarize content using summarization library of your choice
    summary = "summary of web content"
    return summary

# Define function to handle file operations
def handle_file_operations():
    # read files in any part of the file system using file paths
    file_path = "/path/to/file"
    with open(file_path, 'r') as f:
        content = f.read()
    # write files in the bot's special working folder
    output_file_path = os.path.join(working_folder, "output.txt")
    with open(output_file_path, 'w') as f:
        f.write(content)
    # delete files using os.remove() or shutil.rmtree()
    folder_to_delete = "/path/to/folder"
    shutil.rmtree(folder_to_delete)

# Define function to check for repeated solutions and search for alternatives
def check_and_search_solution(directions):
    if directions in tried_solutions:
        query = "alternative solutions for " + directions
        webbrowser.open("https://www.google.com/search?q=" + query)
        return True
    else:
        tried_solutions.add(directions)
        return False

# Define function to test code snippet
def test_code_snippet(code_snippet):
    # Test code snippet
    try:
        query = "Does this code compile?\n" + code_snippet
        response = qa_chain(query)
        if "Yes" in response['answer']:
            return True
        else:
            return False
    except:
        traceback.print_exc()
        return False


# Define CLI interface
while True:
    # Prompt user for programming task
    print("="*80)
    print("Active text:")
    print("="*80)
    prompt = "Please enter a programming task: "
    task = input(prompt)

    # Wrap long prompt text
    wrapper = textwrap.TextWrapper(width=80)
    wrapped_prompt = wrapper.fill(prompt)

    # Define program flowchart
    for i in range(max_iterations):
        # Jump back to branch point if necessary
        if i > 0:
            handle_file_operations()
            if check_and_search_solution(directions):
                continue

        # Ask LangChain for compiling code matching the task
        query = "compiling code for " + task
        response = qa_chain({"input_documents": docs, "question": query}, return_only_outputs=True)
        code_snippet = response[0]['answer']

        # If LangChain returns a valid response, write it to a file and test it
        if code_snippet:
            file_path = os.path.join(working_folder, "compiled_code.py")
            with open(file_path, 'w') as f:
                f.write(code_snippet)
            print("Found compiling code for task:", task)
            if test_code_snippet(code_snippet):
                print("Code snippet is valid!")
                break
            else:
                print("Code snippet is not valid. Trying again...")
                continue

        # If LangChain does not return a valid response after the final iteration, print an error message and exit the loop
        if i == max_iterations - 1:
            print("Error: Unable to find compiling code for task:", task)
            break
