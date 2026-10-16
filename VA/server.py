from fastapi import FastAPI, HTTPException, Response, Cookie
from pydantic import BaseModel
from typing import Dict, Optional
import math
import json
from tokenize import TokenError

# Import your completed functions and error classes from MA4
from MA4 import statement, assignment, expression, term, factor
from MA4 import TokenizeWrapper, CalculatorSyntaxError, EvaluationError

# Initialize the FastAPI app
app = FastAPI(title="MA4 Calculator Web Server")

class CalcRequest(BaseModel):
    data: str
    vars: Dict[str, float] = {}

def initialize_vars(variables: Dict[str, float]) -> Dict[str, float]:
    if "PI" not in variables:
        variables["PI"] = math.pi
    if "E" not in variables:
        variables["E"] = math.e
    if "ans" not in variables:
        variables["ans"] = 0.0
    return variables

def process_math_request(req: CalcRequest, response: Response, calc_session: Optional[str], math_function):
    # 1. Load cookie
    cookie_vars = json.loads(calc_session) if calc_session else {}
    variables = initialize_vars({**cookie_vars, **req.vars})
    wtok = TokenizeWrapper(req.data)
    
    try:
        # 2. Run whichever math function was passed in (statement, factor, etc.)
        result = math_function(wtok, variables)
        if math_function == statement:
            variables['ans'] = result
            
        # 3. Save cookie and return
        response.set_cookie(key="calc_session", value=json.dumps(variables))
        return {"value": result, "vars": variables}
        
    except CalculatorSyntaxError as se:
        raise HTTPException(status_code=400, detail=f"Syntax Error: {str(se)}")
    except EvaluationError as ee:
        raise HTTPException(status_code=400, detail=f"Evaluation Error: {str(ee)}")
    except TokenError:
        raise HTTPException(status_code=400, detail="Syntax Error: Unbalanced parentheses")

@app.post("/statement")
def calculate_statement(req: CalcRequest, response: Response, calc_session: Optional[str] = Cookie(default=None)):
    return process_math_request(req, response, calc_session, statement)

@app.post("/assignment")
def calculate_assignment(req: CalcRequest, response: Response, calc_session: Optional[str] = Cookie(default=None)):
    return process_math_request(req, response, calc_session, assignment)

@app.post("/expression")
def calculate_expression(req: CalcRequest, response: Response, calc_session: Optional[str] = Cookie(default=None)):
    return process_math_request(req, response, calc_session, expression)

@app.post("/factor")
def calculate_factor(req: CalcRequest, response: Response, calc_session: Optional[str] = Cookie(default=None)):
    return process_math_request(req, response, calc_session, factor)

@app.post("/term")
def calculate_term(req: CalcRequest, response: Response, calc_session: Optional[str] = Cookie(default=None)):
    return process_math_request(req, response, calc_session, term)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4999)