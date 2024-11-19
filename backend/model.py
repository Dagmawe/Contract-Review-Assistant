import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)
import vertexai.generative_models
import google.cloud.logging
import logging

client = google.cloud.logging.Client()
handler = client.get_default_handler()
logging.basicConfig(level=logging.INFO, handlers=[handler])

vertexai.init(project="testing-project-440118", location="us-central1")

def model(prompt, config: GenerationConfig = None):
    logging.info('Model function triggered')
    if not config:
        config = GenerationConfig(temperature=0.8, top_p=0.8)
    model = GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=config,
    )
    logging.info('Model successfully configured')
    try:
        annotations_text = model.generate_content(prompt).text
        logging.info(f'Model execution was sucessfull: {len(annotations_text)}')
    except SystemExit as e:
        annotations_text = "error"
        logging.info(f'Model execution failed with SystemExit: {e}')
    except ValueError as e: 
        annotations_text = "error"
        logging.info(f'Model execution failed with ValueError: {e}')
    except Exception as e:
        annotations_text = "error"
        logging.info(f'Model execution failed with unknown Exception: {e}')

    return annotations_text