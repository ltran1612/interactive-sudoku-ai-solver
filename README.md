# Interactive AI Sudoku Solver
Learn LLM, ReAct agent, and AI in general by building an interactive Sudoku solver.

There will be a Sudoku modeling tool/solver built using Cling (Answer Set Programming) and Python.
Then we will use a ReAct agent through `dspy` to use the tools to solve a problem through prompts.

## Lesson Learned
LLM seems to be "forgetting" things  when following a long chain of actions (at least with the ReAct implementation of `dspy` framework). For example, when inputting the models, chatgpt 4o seems to always forget to input the last row of the Sudoku when input each cell per action. Changing to input the entire row per action solved this problem.
Also, once getting the right solution, the LLM currently does n't seem to be able to show the final solution appropriately.

## Goals
Being able to solve a more diverse task with just prompts instead  of just 1 right now, which is to solve the entire sudoku problem.
Being able to interactively solve it on paper and pen using a ca mera (stretch goal).
