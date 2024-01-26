from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recipe = ''
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        recipe = get_vegan_recipe(ingredients)
    return render_template('index.html', recipe=recipe)

logging.basicConfig(level=logging.INFO)

def get_vegan_recipe(ingredients):
    headers = {
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'
    }

    prompt_text = f"Create a detailed vegan recipe that includes the following ingredients: {ingredients}. The recipe should be easy to follow and include steps for preparation and cooking."

    data = {
        'model': 'text-davinci-003',
        'prompt': prompt_text,
        'temperature': 0.7,
        'max_tokens': 500
    }

    response = requests.post('https://api.openai.com/v1/engines/davinci/completions', headers=headers, json=data)
    logging.info(f"Request data: {data}")
    logging.info(f"Response status code: {response.status_code}")
    logging.info(f"Response data: {response.json()}")

    if response.status_code == 200:
        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0:
            return response_json['choices'][0].get('text', 'Recipe not found.')
        else:
            return 'Recipe not found.'
    else:
        return 'Unable to generate a recipe at this time.'


if __name__ == '__main__':
    app.run(debug=True)
