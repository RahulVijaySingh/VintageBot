from flask import Flask, request, render_template, jsonify
from chatbot_logic import filter_properties
from flask_cors import CORS
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").lower()
    session = request.json.get("session", {})   

    step = session.get("step", 0)
    context = session.get("context", {})

    response = ""
    session["step"] = step
    session["context"] = context

    if step == 0:
        response = "👋 Are you looking for a flat, plot, or villa?"
        session["step"] = 1

    elif step == 1:
        context["type"] = user_input
        response = "📍 Great! Which area are you interested in?"
        session["step"] = 2

    elif step == 2:
        context["location"] = user_input
        response = "💰 What's your budget range? "
        session["step"] = 3

    
    elif step == 3:
        context["budget"] = user_input
        properties = filter_properties(
            property_type=context.get("type"),
            location=context.get("location"),
            budget=context.get("budget")
        )
        if properties:
            listings = "\n\n".join(
                [f"{i+1}. 🏡 {p['Title']}\n📌 {p['Type & Location']}\n💰 {p['Price']}\n🧑 {p['Seller']}"
                for i, p in enumerate(properties)]
            )
            response = f"Here are some matching properties:\n\n{listings}\n\n🙏 Thank you! Would you like to restart the search? (yes/no)"
        else:
            response = "😔 Sorry, no properties found matching your preferences.\n\n🙏 Would you like to restart the search? (yes/no)"

        session["step"] = 5  # directly move to step 5 here

    



    elif step == 4:
        response = "🙏 Thank you! Would you like to restart the search? (yes/no)"
        session["step"] = 5

    elif step == 5:
        if "yes" in user_input:
            session = {"step": 0, "context": {}}
            response = "🔁 Restarting...\nAre you looking for a flat, plot, or villa?"
        else:
            response = "👋 Goodbye! Let us know if you need anything else."

    return jsonify({"response": response, "session": session})

if __name__ == "__main__":
    app.run(debug=True)
