from typing import Literal
import clingo
from pathlib import Path

class SudokuWorld: 
    def __init__(self):
        self.reset()
        filepath = Path(__file__).parent / "sudoku_world.lp"
        with open(filepath, "r") as f:
            self.theory = "".join(f.readlines())
        filepath = Path(__file__).parent / "explorer.lp"
        with open(filepath, "r") as f:
            self.explorer = "".join(f.readlines())
    def reset(self):
        self.state = [[None for j in range(10)] for i in range(10)]
    def set_state(self, row, col, val):
        self.state[row][col] = val
    def create_solver(self, count=1) -> clingo.SolveControl:
        ctl = clingo.Control(arguments=[f"--models={0 if count is None else count}"], logger=self.log)
        facts = self.get_facts()
        grounding_parts = [("theory", []), ("explorer", []), ("facts",[])]
        ctl.add("theory", [], self.theory) 
        ctl.add("explorer", [], self.explorer) 
        ctl.add("facts", [], "".join(facts)) 
        ctl.ground(grounding_parts)
        return facts, ctl
    def get_facts(self): 
        facts = []
        for r, row in enumerate(self.state):
            if row is None:
                continue
            for c, val in enumerate(row):
                if val is None:
                    continue
                facts.append(f"cell({r+1},{c+1},{val}).")
        print(facts)
        return facts
    def see_state(self):
        facts = []
        for r, row in enumerate(self.state):
            if row is None:
                continue
            for c, val in enumerate(row):
                if val is None:
                    continue
                facts.append((r+1,c+1,val))
        return facts
    def available_solution(self, count=None) -> list[tuple[int, int, int]]:
        if count < 0:
            return []

        answer = [] 
        _, ctl = self.create_solver(0 if count is None else count)
        with ctl.solve(yield_=True, async_=True) as handle:
            while True:
                handle.resume()
                _ = handle.wait()
                m = handle.model()
                if m is None:
                    break
                symbols = m.symbols(atoms=True)
                for sym in symbols:
                    cell = self.parse_cell(sym)
                    if cell is None:
                        continue
                    answer.append(cell)
        return answer

    def available_values(self, ir, ic):
        if ir == None or ic == None:
            raise Exception("ir and ic cannot be null")

        answer = set() 
        for val in range(1, 10, 1):
            self.set_state(ir, ic, val)
            facts, ctl = self.create_solver(1)
            with ctl.solve(yield_=True) as handle:
                for m in handle:
                    if m is None:
                       continue 
                    answer.add(val)
        return list(answer)
        
    def log(self, x, y):
        pass
    def parse_cell(self, symbol: clingo.Symbol):
        if symbol is None or symbol.name != "cell":
            return None
        args = symbol.arguments
        if args is None or len(args) != 3:
            return None
        args = list(map(lambda arg: arg.number, args))
        return tuple(args)

if __name__ == "__main__":
    world = SudokuWorld()
    world.set_state(1, 1, 2)
    world.set_state(1, 3, 3)
    print(world.available_values(1, 2))
    print(world.available_solution(1))