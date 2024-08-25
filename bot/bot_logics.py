from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch

model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

health_tips = {
    "general": "Remember to maintain a balanced diet, exercise regularly, and get enough sleep.",
    "headache": "For headaches, try resting in a dark, quiet room and stay hydrated. Over-the-counter pain relievers may help.",
    "cold": "For colds, get plenty of rest, drink warm fluids, and use over-the-counter cold medications as needed.",
    "fever": "For fever, stay hydrated and consider using over-the-counter fever reducers. Seek medical attention if fever persists or is very high.",
    "stress": "To manage stress, try deep breathing exercises, meditation, or regular physical activity.",
    "diet": "A healthy diet should include plenty of fruits, vegetables, whole grains, lean proteins, and healthy fats.",
    "exercise": "Aim for at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous aerobic activity per week.",
}

mental_health_resources = {
    "anxiety": "Practice deep breathing exercises, try mindfulness meditation, or consider talking to a therapist.",
    "depression": "Reach out to loved ones, establish a routine, and consider professional help. Remember, it's okay to ask for support.",
    "stress": "Practice time management, set realistic goals, and make time for relaxation and hobbies.",
    "sleep": "Establish a regular sleep schedule, create a relaxing bedtime routine, and avoid screens before bed.",
    "self_care": "Make time for activities you enjoy, practice self-compassion, and prioritize your physical and mental health.",
}

def get_bot_response(user_input):
    lower_input = user_input.lower()
    
    # Check for mental health keywords
    for keyword, resource in mental_health_resources.items():
        if keyword in lower_input:
            return f"Here's a tip for {keyword}: {resource}\n\nIf you need professional support, please contact preciouse@proffessional.com."

    # Check for general health keywords
    for keyword, tip in health_tips.items():
        if keyword in lower_input:
            return f"Here's a health tip about {keyword}: {tip}"

    # If no specific keyword is found, use the model for a general response
    inputs = tokenizer(user_input, return_tensors="pt")
    reply_ids = model.generate(**inputs, max_length=100)
    bot_response = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]

    # If the response doesn't seem health-related, add a general health or mental health tip
    if not any(keyword in bot_response.lower() for keyword in health_tips.keys() + list(mental_health_resources.keys())):
        bot_response += f"\n\nHere's a general health tip: {health_tips['general']}\n\nRemember, mental health is just as important as physical health. If you're feeling overwhelmed, don't hesitate to seek support."

    # Check for emergency keywords
    emergency_keywords = ["emergency", "severe pain", "unconscious", "bleeding heavily", "suicidal", "crisis"]
    if any(keyword in lower_input for keyword in emergency_keywords):
        bot_response += "\n\nIf this is a medical or mental health emergency, please call your local emergency number (e.g., 911 in the US) immediately. For mental health crisis support, you can also contact a helpline."

    return bot_response

# Add a disclaimer to be used in the chat interface
medical_disclaimer = ("I'm an AI assistant and can provide general health information and resources, but I'm not a substitute for "
                      "professional medical or mental health advice. Always consult with a qualified healthcare provider for "
                      "personalized advice, diagnosis, or treatment. If you're experiencing a medical or mental health emergency, "
                      "please call your local emergency number or seek immediate professional help.")