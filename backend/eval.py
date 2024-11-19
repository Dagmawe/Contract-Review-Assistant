import pandas as pd 
import re
import model
from google.cloud import storage
from io import BytesIO
from PyPDF2 import PdfReader
import utlis
from vertexai.generative_models import GenerationConfig
import os
import argparse
import datetime


def get_rubric_data():
    BUCKET_NAME = "sowupload-testing-project-440118" 
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob("rubric.csv")
    rubric = blob.download_as_text(encoding="Latin-1")
    return rubric


def getContract(filename, local:bool = False):
    if local:
        with open(filename, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            contract = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                contract += page.extract_text()
        return contract
    
    BUCKET_NAME = "sowupload-testing-project-440118" 
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    blob = bucket.blob(filename)
    contract = blob.download_as_bytes()

    pdf_file_obj = BytesIO(contract)
    pdf_reader = PdfReader(pdf_file_obj)

    contract = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        contract += page.extract_text()
    
    return contract


def getScore(contract, config: GenerationConfig = None):
    rubric = get_rubric_data()
    prompt = utlis.prompts.one_shot_prompt(rubric, contract)
    LLM_response = model.model(prompt, config)
    pattern = r"## Score (\d+)"   
    match = re.search(pattern, LLM_response)
    if match:
        score = match.group(1)
        score = int(score)
    else:
        score = None
    return score



def eval(filename: str, expected_score: int, local: bool = False, config: GenerationConfig = None):
    contract = getContract(filename, local)
    score = getScore(contract, config)
    error_rate = 5
    res = abs(expected_score - score) <= error_rate
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "Filename": [filename],
        "local": [local],
        "LLM Score": [score],
        "Expected Score": [expected_score],
        "Passed": [res],
        "Datetime": [timestamp]
    }
    new_df = pd.DataFrame(data)
    results_path = os.path.abspath("eval_results/results.csv")
    try:
        existing_df = pd.read_csv(results_path)  
        df = pd.concat([existing_df, new_df], ignore_index=True) 
    except FileNotFoundError:
        df = new_df  
    df.to_csv(results_path, index=False)
    print(pd.read_csv(results_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate Contract review tool')
    parser.add_argument(
        'path',  
        type=str,
        help='Input filepath/filename.',
    )
    parser.add_argument(
        'score',  
        type=int,
        help='Input contract expected score (out of 100).',
    )
    parser.add_argument(
        '--local', 
        action='store_true',  
        help='Specify if the contract is stored locally.',
    )

    args = parser.parse_args()
    print("Evaluating...")
    eval(args.path, args.score, args.local) 
    print("Sucessfully evaluated")






