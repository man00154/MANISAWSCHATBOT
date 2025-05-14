from flask import Flask, request, jsonify, render_template_string
import boto3

app = Flask(__name__)

# AWS Credentials and Configuration
aws_access_key = "YOUR_AWS_ACCESS_KEY"
aws_secret_key = "YOUR_AWS_SECRET_KEY"
aws_region = "us-east-1"

# Initialize Boto3 Client
client = boto3.client('lexv2-runtime',
                      aws_access_key_id=aws_access_key,
                      aws_secret_access_key=aws_secret_key,
                      region_name=aws_region)

@app.route('/')
def home():
    # Render a simple HTML page with chatbot UI
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AWS Chatbot by Manish Singh</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
            }
            h1 {
                color: #2e6cb7;
                margin-top: 50px;
            }
            #chat-container {
                margin: 20px auto;
                width: 60%;
                max-width: 600px;
            }
            textarea, input {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                background-color: #2e6cb7;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
            }
            button:hover {
                background-color: #1f4d99;
            }
            .response {
                background-color: #e8f4ff;
                border: 1px solid #ccc;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <h1>AWS CHATBOT BY MANISH SINGH</h1>
        <div id="chat-container">
            <textarea id="user-input" placeholder="Type your message here..."></textarea>
            <button onclick="sendMessage()">Send</button>
            <div id="response-container"></div>
        </div>
        <script>
            async function sendMessage() {
                const userInput = document.getElementById('user-input').value;
                const responseContainer = document.getElementById('response-container');
                responseContainer.innerHTML = "<p>Loading...</p>";

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: userInput, session_id: 'user-session' })
                });

                const data = await response.json();

                if (response.ok) {
                    responseContainer.innerHTML = `
                        <div class="response"><strong>Chatbot:</strong> ${data.messages[0].content}</div>
                    `;
                } else {
                    responseContainer.innerHTML = `
                        <div class="response"><strong>Error:</strong> ${data.error}</div>
                    `;
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    session_id = request.json.get('session_id', 'default')

    try:
        # Call AWS Lex Chatbot
        response = client.recognize_text(
            botId='YOUR_BOT_ID',
            botAliasId='YOUR_BOT_ALIAS_ID',
            localeId='en_US',
            sessionId=session_id,
            text=user_input
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
