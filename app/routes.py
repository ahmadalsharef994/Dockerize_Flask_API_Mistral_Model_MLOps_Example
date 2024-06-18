from flask import Flask, request, jsonify, current_app
from langchain_community.llms import LlamaCpp

app = current_app

llama_model = LlamaCpp(
    model_path=app.config['MODEL_PATH'],
    temperature=0.2,
    max_tokens=800,
    n_gpu_layers=64,
    n_ctx=2048
)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('text')
    response = llama_model.invoke(user_input)
    return jsonify({'response': response})
