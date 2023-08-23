import math
def amir(x):
    result=eval(x, {"__builtins__": None}, math.__dict__)
    # print("javabb :", result)
    return result
