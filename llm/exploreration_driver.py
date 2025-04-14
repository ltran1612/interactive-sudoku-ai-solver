import dspy

class Intepretor:
    def __init__(self):
        self.explanation = ""
    
    def answer(self, question: str):
        # todo
        pass


if __name__ == "__main__":
    lm = dspy.LM(
        model="ollama_chat/llama3.2",  # Changed to include provider prefix
        api_base="http://localhost:11434",
        max_tokens=20000,
    )
    dspy.settings.configure(lm=lm)
    state = "cell(1,1,7) cell(1,2,9) cell(1,3,8) cell(1,4,6) cell(1,5,5) cell(1,6,4) cell(1,7,3) cell(1,8,2) cell(1,9,1)"
    explanation = "cell(X, Y, Z) represents the value Z of the cell at X row and Y column. List all cells in plain English."
    interpretor = dspy.ChainOfThought("explanation, state -> description")
    print(interpretor(state=state, explanation=explanation).description)