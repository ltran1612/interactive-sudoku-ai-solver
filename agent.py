import time
from typing import Literal
import dspy

from symbolic.world import SudokuWorld

lm = dspy.LM(
    model="ollama_chat/deepseek-r1:8b",  # Changed to include provider prefix
    api_base="http://localhost:11434",
    max_tokens=20000,
)

lm = dspy.LM('openai/gpt-4o-mini', api_key='<API-KEY-HERE>')
dspy.settings.configure(lm=lm)

model = SudokuWorld()
def search_available_values(rowIndex: int, columnIndex: int) -> str:
    answer = model.available_values(int(rowIndex), int(columnIndex))
    answer = f"The available values are: {",".join(map(lambda x: str(x), answer))}"
    return answer
def set_row(rowIndex: int, values: list[int]) -> str:
    try:
        time.sleep(1)
        for idx, value in enumerate(values):
            model.set_state(rowIndex, idx, None if value == 0 else value)
        state = model.see_state()
        values = "\n".join(map(lambda x: f"Row {x[0]-1}, Column {x[1]-1}, Has Value {x[2]}", state))
        return f'''
Set the value successfully.
The current state of the model after setting is:
{values}
        '''
    except Exception as e:
        return f"Failed to set the value for the cell, the reason is {str(e)}"
def reset_model(*args) -> None:
    model.reset()
def find_solution() -> str:
    time.sleep(1)
    state = model.available_solution(count=1)
    if (len(state) == 0):
        return "There's no solution for this Sudoku problem"
    values = "\n".join(map(lambda x: f"Row {x[0]-1}, Column {x[1]-1}, Has Value {x[2]}", state))
    return f'''
    The solution is:
    {values}
    '''
def see_model() -> str:
    state = model.see_state()
    values = "\n".join(map(lambda x: f"Row {x[0]-1}, Column {x[1]-1}, Has Value {x[2]}", state))
    return f'''
The current state of the model is:
{values}
        '''
steps = []
def add_a_plan_step(step_info: str):
    steps.append(step_info) 
    time.sleep(1)
def get_next_step() -> str|None:
    try:
        time.sleep(1)
        return steps.pop(0)
    except:
        return None
def none_action():
    pass

setgrid_tool = dspy.Tool(
    set_row, 
    desc="Set the the value for the grid cell in the Sudoku model. Users need to provide the row index, the column index, and the value to set it with.", 
    arg_desc={"rowIndex": "The index of the row of concern. Required.", "values": "The list of values to set the cell in that row. Required one for each column in the row."},
)
search_cellvalue_tool = dspy.Tool(
    search_available_values, 
    desc="Get the available values that the grid cell can have given the current state of the Sudoku model.", 
    arg_desc={"rowIndex": "A number for the row index of the cell to check. Required.", "columnIndex": "A number for the column index of the cell to check. Required."},
)
find_solution_tool = dspy.Tool(
    find_solution, 
    desc="Find the solution of the model based on the values set in the model.", 
)

instructions=f'''
You'll be give 2 tools:
1. A Sudoku modeling tool. The model is initially empty; that is, no cells are set. There are 3 functions to use in this tool:
a. Use `set_row` to set the value for each row in the model. 
b. Use `find_solution` to find a solution for the set model of the Sudoku problem.
c. Use `see_model` to see the set model.
2. A memorizer tool to help memorize a list of steps to do. Please use this because you tend to forget to properly do the last 2 rows (row 7 and row 8). There are 2 functions to use:
a. Use `add_a_plan_step` to save the required information needed to complete a next step.
b. Use `get_next_step` to retrieve the information about the next step to complete.

Create a plan first that uses the Sudoku modeling tool to sovle the task requested.
Then, uses the memorizer tool to memorize the list of steps.
After that, complete each step as outlined in the memorizer tool.
'''
signature = dspy.Signature("question -> answer", instructions=instructions)
tools=[setgrid_tool, see_model, find_solution_tool]
# tools=[]
react = dspy.ReAct(signature, tools=tools, max_iters=100)

question=''''
Row 1: 5 3 0 0 7 0 0 0 9
Row 2: 6 0 0 1 9 5 0 0 0
Row 3: 0 9 8 0 0 0 4 0 0
Row 4: 3 0 0 0 2 0 0 5 0
Row 5: 9 0 0 0 3 0 0 0 8
Row 6: 0 0 0 9 0 8 0 0 0
Row 7: 0 5 0 0 0 0 3 0 0
Row 8: 0 0 0 4 5 0 0 2 0
Row 9: 0 0 0 0 0 9 8 0 0
''' 
question=''''
Row 1: 0 0 3 0 0 7 0 0 0
Row 2: 0 8 2 0 3 6 0 7 0
Row 3: 0 0 4 0 1 8 0 0 9
Row 4: 0 0 0 0 0 2 5 3 0
Row 5: 0 0 0 0 0 0 0 0 8
Row 6: 0 0 0 0 5 0 9 4 0
Row 7: 0 7 0 0 0 0 0 0 0
Row 8: 0 2 0 0 4 0 8 6 0
Row 9: 5 0 0 1 6 0 0 0 0
''' 
answer = react(question=f"Help me solve this sudoku problem and show me the final sudoku. {question}")
# answer = react(question=f"Set row 1 and column 1 to 2.")

# def evaluate_math(expression: str):
#     return dspy.PythonInterpreter({}).execute(expression)

# def search_wikipedia(query: str):
#     results = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
#     return [x['text'] for x in results]

# react = dspy.ReAct("question -> answer: float", tools=[evaluate_math, search_wikipedia])

# answer = react(question="What is 9362158 divided by the year of birth of David Gregory of Kinnairdy castle?")

for key, value in answer.trajectory.items():
    print(key, value)
print(answer.answer)
# print(model.see_state())
