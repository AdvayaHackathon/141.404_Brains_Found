# from langchain_ollama import ChatOllama
# from langchain_core.messages import HumanMessage, AIMessage

# # Simple memory
# messages = []

# # Initialize chatbot with pulled model (e.g., llama3)
# chatbot = ChatOllama(model="llama3.2")

# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("Bot: Goodbye!")
#         break

#     # Add user message
#     messages.append(HumanMessage(content=user_input))

#     # Get response
#     response = chatbot.invoke(messages)

#     # Print and store bot response
#     print("Bot:", response.content)
#     messages.append(AIMessage(content=response.content))




from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
import random

# Dictionary to store conversation histories for different users
user_chat_histories = {}

class OfflineAI:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.chatbot = ChatOllama(model=self.model_name)
        self.supported_languages = {
            "english": "en",
            "tamil": "ta",
            "telugu": "te",
            "kannada": "kn",
            "malayalam": "ml"
        }
        self.current_language = "english"
        self.responses = {
            'mathematics': [
                "Let me help you with that math problem. In elementary math, we focus on addition, subtraction, multiplication, and division.",
                "That's a good math question! Remember that numbers are our friends.",
                "In math, we learn to count, add, subtract, and solve simple problems."
            ],
            'science': [
                "Science is all about exploring the world around us. Plants, animals, and weather are all part of science!",
                "In elementary science, we learn about living things, the earth, and simple experiments.",
                "That's an interesting science question! Let's explore how things work in our world."
            ],
            'language': [
                "Reading and writing are important skills. Let's work on your language question.",
                "In language arts, we learn about letters, words, sentences, and stories.",
                "That's a great question about language! Let's explore words and their meanings."
            ],
            'history': [
                "History helps us learn about people and events from the past.",
                "In elementary history, we learn about our community, country, and important historical figures.",
                "That's an interesting history question! Let's explore what happened in the past."
            ],
            'general': [
                "I'm here to help with your educational questions.",
                "That's an interesting question. Let me explain...",
                "I understand your question. Here's what I know about that topic...",
                "Great question! The answer involves several concepts...",
                "I can help you understand this better. Let's break it down..."
            ]
        }

    def get_response(self, user_id, message):
        if user_id not in user_chat_histories:
            user_chat_histories[user_id] = []

        user_chat_histories[user_id].append(HumanMessage(content=message))

        try:
            response = self.chatbot.invoke(user_chat_histories[user_id])
            user_chat_histories[user_id].append(AIMessage(content=response.content))
            return response.content
        except Exception as e:
            return self._generate_fallback_response(message)

    def _generate_fallback_response(self, message):
        message = message.lower()
        if any(word in message for word in ['math', 'add', 'subtract', 'multiply', 'divide', 'number']):
            return random.choice(self.responses['mathematics'])
        elif any(word in message for word in ['science', 'plant', 'animal', 'earth', 'experiment']):
            return random.choice(self.responses['science'])
        elif any(word in message for word in ['read', 'write', 'word', 'sentence', 'story', 'language']):
            return random.choice(self.responses['language'])
        elif any(word in message for word in ['history', 'past', 'country', 'community']):
            return random.choice(self.responses['history'])
        else:
            return random.choice(self.responses['general'])

# Main CLI loop
if __name__ == "__main__":
    ai = OfflineAI(model_name="llama3.2")
    user_id = "user1"

    print("=" * 50)
    print("\U0001F9E0 Offline ChatBot using llama3.2 (Type 'exit' to quit)")
    print("=" * 50)

    while True:
        user_input = input("\nYou \U0001F9D1: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nBot \U0001F916: Goodbye! \U0001F44B\n")
            break

        response = ai.get_response(user_id, user_input)
        print("\nBot \U0001F916:", response)
        print("-" * 50)
