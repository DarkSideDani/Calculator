from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression', '')
    try:
        result = str(eval(expression))  # Simplified evaluation, replace with safer method
        response = {'result': result}
    except Exception as e:
        response = {'result': 'ERROR', 'error': str(e)}
    
    # Log what the server is returning
    print("Returning result:", response)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
