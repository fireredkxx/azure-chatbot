from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# REPLACE with your own details
CLU_ENDPOINT = "https://t6.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview"
CLU_KEY = "bf109202055945f5a39c3613d0fcad62"
PROJECT_NAME = "HealthcareAssistantBot"
DEPLOYMENT_NAME = "HealthcareAssistantDeployment"

@app.route("/", methods=["GET", "POST"])
def chatbot():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        headers = {
            "Ocp-Apim-Subscription-Key": CLU_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "id": "1",
                    "participantId": "user",
                    "text": user_input
                }
            },
            "parameters": {
                "projectName": PROJECT_NAME,
                "deploymentName": DEPLOYMENT_NAME,
                "stringIndexType": "TextElement_V8"
            }
        }

        r = requests.post(CLU_ENDPOINT, headers=headers, json=payload)
        result = r.json()
        try:
            top_intent = result["result"]["prediction"]["topIntent"]
            response_text = f"Top intent: {top_intent}"
        except:
            response_text = "Sorry, I couldn't understand that."

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
