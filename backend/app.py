from flask import Flask, request
from flask_cors import CORS
import model
from google.cloud import storage
from io import BytesIO
from PyPDF2 import PdfReader
import markdown
import utlis
from flask_caching import Cache
import logging
from google.cloud import logging
import time 

logging_client = logging.Client()
logging_client.setup_logging() 

app = Flask(__name__)

# CORS(app, resources={r"/eval/*": {"origins": "https://frontend-dot-testing-project-440118.ue.r.appspot.com"}}, supports_credentials=True)

CORS(app, resources={r"/eval/*": {"origins": "*"}}, supports_credentials=True)

cache = Cache(app, config={'CACHE_TYPE': 'simple'}) 

BUCKET_NAME = "sowupload-testing-project-440118" 
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)



@cache.cached(timeout=3600, key_prefix='rubric_data')  # Cache for 1 hour
def get_rubric_data():
    blob = bucket.blob("rubric.csv")
    rubric = blob.download_as_text(encoding="Latin-1")
    return rubric


@app.route("/")
def test():
    return "Hello World!"

@app.route("/chat/<prompt>")
def chat(prompt):
    response = model.model(prompt)
    return response

@app.route('/eval', methods=['POST'])
def upload_file():
        if 'file' not in request.files:
            app.logger.info("Failed to upload fail part")
            return "No file part. Please upload a valid pdf file and try again..."  
        file = request.files['file']
        if file.filename == '':
            app.logger.info("Failed to find filename: No selected file")
            return "No selected file. Please upload a valid pdf file try again..." 
        try: 
            start_time = time.time()
            # Save the DAF into cloud storage
            storage_client = storage.Client()
            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file)
            # dowload the DAF from cloudstorage 
            blob = bucket.blob(file.filename)
            contract = blob.download_as_bytes()

            pdf_file_obj = BytesIO(contract)
            pdf_reader = PdfReader(pdf_file_obj)

            contract = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                contract += page.extract_text()
            contract_exec_time = time.time() - start_time
            
            start_time = time.time()
            rubric = get_rubric_data()
            rubric_exec_time = time.time() - start_time
            
            if len(contract) > 0 and len(rubric) > 0:
                app.logger.info(f"Contract successfully created!: {len(contract)}")
                app.logger.info(f"Rubric successfully created!: {len(rubric)}")
            else:
                app.logger.info(f"Contract creation failed!: {len(contract)}")
                app.logger.info(f"Rubric creation failed!: {len(rubric)}")

            prompt = utlis.prompts.one_shot_prompt(rubric, contract)
            start_time = time.time()
            review = model.model(prompt)
            model_exec_time = time.time() - start_time
            if review == "error":
                app.logger.info(f"Model execution failed, trying again...")
                #try one more time
                start_time = time.time()
                review = model.model(prompt)
                model_exec_time = time.time() - start_time
                if review == "error": review =  "Sorry something went wrong, please try again..."
            app.logger.info(f"Model execution time: {model_exec_time}; Contract execution time: {contract_exec_time}; Rubric execution time: {rubric_exec_time}")
            # Convert to markdown
            review =  markdown.markdown(review)
            return review 
        except Exception as e:
            return f"Error fetching: {e}" 
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')