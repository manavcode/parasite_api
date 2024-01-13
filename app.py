import os
from flask import Flask, jsonify, request
import openai
from utils import *


app = Flask(__name__)
prefix = "what are the most important html elements along with element ID to highlight to complete the task:"


@app.route('/analyze_local', methods=['GET'])
def analyze_local():

    data = read_file()
    data = extract_interactive_elements(data)

    print("data: ", data)

    prompt = f"{prefix} book a flight"

    # model = openai(temperature=5, model_name="text-davinci-003")
    openai.api_key = os.environ["OPENAI_API_KEY"]
    resp = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Website code: {data}\n{prompt}",
        # prompt = "how afd you doing?",
        temperature=0,
        max_tokens=1000,
    )

    # print(resp)
    response_text = resp.choices[0].text if resp else ""

    response_data = {
        'elements': parse_gpt_response(response_text)
    }
    return jsonify(response_data)
    # return ""


@app.route('/analyze', methods=['POST'])
def analyze():
    print("here")
    data = request.get_json()
    print(request)
    url = data.get('url')
    task = data.get('task')

    print("POST", url, task)
    print("post")

    html_content = extract_interactive_elements(get_html(url))
    prompt = f"{prefix}: {task}"



    openai.api_key = os.environ["OPENAI_API_KEY"]
    resp = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Website code: {html_content}\n{prompt}",
        # prompt = "how afd you doing?",
        temperature=0,
        max_tokens=1000,
    )

    # print(resp)
    response_text = resp.choices[0].text if resp else ""

    response_data = {
        'elements': parse_gpt_response(response_text)
    }
    return jsonify(response_data)


@app.route('/test', methods=['POST'])
def test():
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # Extract values from the JSON data
        input_value = data.get('input_value')

        # Perform some processing on the input (you can replace this with your logic)
        processed_result = f"Processed input: {input_value}"

        # Return the processed result as JSON
        return jsonify({'result': processed_result})

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # configure()
    app.run(host="0.0.0.0", debug=True, port=5001)
