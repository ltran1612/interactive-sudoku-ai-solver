import dspy

class Intepretor:
    def __init__(self):
        self.background_information = "cell(X, Y, Z) represents the value Z of the cell at X row and Y column."
        self.interpretor = dspy.ChainOfThought("background_information, question -> answer")
    def toClingo(self, statement: str) -> str:
        question = f"{statement}. Convert this into cell(X, Y, Z) format."
        answer = self.interpretor(question=question, background_information=self.background_information).answer
        return answer
    def answer(self, state: str, question: str) -> str:
        question = f"{state}. {question}"
        return self.interpretor(question=question, background_information=self.background_information).answer


if __name__ == "__main__":
    lm = dspy.LM(
        model="ollama_chat/llama3.2",  # Changed to include provider prefix
        api_base="http://localhost:11434",
        max_tokens=20000,
    )
    dspy.settings.configure(lm=lm)
    state = "cell(1,1,7) cell(1,2,9) cell(1,3,8) cell(1,4,6) cell(1,5,5) cell(1,6,4) cell(1,7,3) cell(1,8,2) cell(1,9,1)"
    question1 = f"Give me 3 cell values? and explain them fully in plain English."
    interpretor = Intepretor()
    answer1 = interpretor.answer(state, question1)
    print(answer1)
    print("----")
    print("----")
    print(interpretor.toClingo(" A simple string of 81 characters, row-wise from top-left to bottom-right, using 0 for empty cells: 530070000600195000098000060800060003400803001700020006060000280000419005000080079"))



   