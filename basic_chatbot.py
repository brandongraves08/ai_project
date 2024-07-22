import json
from difflib import get_close_matches

class SimpleChatbot:
    def __init__(self, filename):
        self.questions = []
        self.load_data(filename)

    def load_data(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.questions = data['questions']

    def get_response(self, user_question):
        # Get the closest matching question
        matches = get_close_matches(user_question.lower(), [q['question'].lower() for q in self.questions], n=1, cutoff=0.6)
        
        if matches:
            for q in self.questions:
                if q['question'].lower() == matches[0]:
                    return q['answer']
        
        return "I'm sorry, I don't have an answer for that question. Can you please rephrase or ask something else?"

# Usage
if __name__ == "__main__":
    chatbot = SimpleChatbot('qa_data.json')
    
    while True:
        user_input = input("Ask a question (or type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        response = chatbot.get_response(user_input)
        print(f"Chatbot: {response}")