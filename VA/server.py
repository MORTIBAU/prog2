from fastapi import FastAPI, HTTPException, Request, Cookie
from fastapi.responses import PlainTextResponse
from typing import Dict, Optional
import math
import json
from tokenize import TokenError


from MA4 import statement, assignment, expression, term, factor
from MA4 import TokenizeWrapper, CalculatorSyntaxError, EvaluationError

app = FastAPI(title="MA4 Calculator Web Server")

def initialize_vars(variables: Dict[str, float]) -> Dict[str, float]:
    if "PI" not in variables:
        variables["PI"] = math.pi
    if "E" not in variables:
        variables["E"] = math.e
    if "ans" not in variables:
        variables["ans"] = 0.0
    return variables

async def process_math_request(request: Request, calc_session: Optional[str], math_function):
    body_bytes = await request.body()
    data = body_bytes.decode("utf-8")
    
    cookie_vars = json.loads(calc_session) if calc_session else {}
    variables = initialize_vars(cookie_vars)
    wtok = TokenizeWrapper(data)
    
    try:
        result = math_function(wtok, variables)
        if math_function == statement:
            variables['ans'] = result

        resp = PlainTextResponse(str(result) + "\n")
        resp.set_cookie(key="cookiefile", value=json.dumps(variables))
        
        return resp
        
    except CalculatorSyntaxError as se:
        raise HTTPException(status_code=400, detail=f"Syntax Error: {str(se)}")
    except EvaluationError as ee:
        raise HTTPException(status_code=400, detail=f"Evaluation Error: {str(ee)}")
    except TokenError:
        raise HTTPException(status_code=400, detail="Syntax Error: Unbalanced parentheses")

@app.post("/statement")
async def calculate_statement(request: Request, cookiefile: Optional[str] = Cookie(default=None)):
    return await process_math_request(request, cookiefile, statement)

@app.post("/assignment")
async def calculate_assignment(request: Request, cookiefile: Optional[str] = Cookie(default=None)):
    return await process_math_request(request, cookiefile, assignment)

@app.post("/expression")
async def calculate_expression(request: Request, cookiefile: Optional[str] = Cookie(default=None)):
    return await process_math_request(request, cookiefile, expression)

@app.post("/factor")
async def calculate_factor(request: Request, cookiefile: Optional[str] = Cookie(default=None)):
    return await process_math_request(request, cookiefile, factor)

@app.post("/term")
async def calculate_term(request: Request, cookiefile: Optional[str] = Cookie(default=None)):
    return await process_math_request(request, cookiefile, term)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4998)