from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Create a simple Python Flask app that serves a web page with an input box and sends user input to your CLU (Conversational Language Understanding) model.
CLU_ENDPOINT = "https://t6.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview"
CLU_KEY = "bf109202055945f5a39c3613d0fcad62"
PROJECT_NAME = "HealthcareAssistantBot"
DEPLOYMENT_NAME = "HealthcareAssistantDeployment"

#Intent-Response Mapping
intent_responses = {
    "GetClinicHours": "Our clinic is open Monday to Friday from 8 AM to 5 PM.",
    "BookAppointment": "You can book an appointment online through our website.",
    "AcceptInsurance": "Yes, we accept most major health insurance providers.",
    "Greet": "Hello! How can I help you today?",
    "None": "I'm not sure I understood that. Can you please rephrase?"
}

@app.route("/", methods=["GET", "POST"])
def chatbot():
    user_input = ""
    response_text = ""

    if request.method == "POST":
        user_input = request.form.get("user_input")

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

        try:
            response = requests.post(CLU_ENDPOINT, headers=headers, json=payload)
            result = response.json()
            top_intent = result["result"]["prediction"]["topIntent"]
            response_text = intent_responses.get(top_intent, "I'm not trained to answer that yet.")
        except Exception as e:
            response_text = "Sorry, something went wrong while processing your request."

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)