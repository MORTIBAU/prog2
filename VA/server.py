from fastapi import FastAPI, HTTPException, Response, Cookie
from pydantic import BaseModel
from typing import Dict, Optional
import math
import json

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

@app.post("/statement")
def calculate_statement(
    req: CalcRequest, 
    response: Response, 
    calc_session: Optional[str] = Cookie(default=None)
):
    # 1. Load variables from the cookie if it exists
    cookie_vars = {}
    if calc_session:
        try:
            cookie_vars = json.loads(calc_session)
        except json.JSONDecodeError:
            pass  # If the cookie is corrupted, just start fresh

    # 2. Merge cookie variables with any variables explicitly sent in the JSON payload
    merged_vars = {**cookie_vars, **req.vars}
    
    # 3. Ensure PI, E, and ans exist
    variables = initialize_vars(merged_vars)
    wtok = TokenizeWrapper(req.data)
    
    try:
        # 4. Run the math logic from MA4
        result = statement(wtok, variables)
        variables['ans'] = result
        
        # 5. Serialize the updated variables to a JSON string and save it to the cookie
        vars_json = json.dumps(variables)
        response.set_cookie(key="calc_session", value=vars_json)
        
        # 6. Return the result
        return {"value": result, "vars": variables}
        
    except CalculatorSyntaxError as se:
        raise HTTPException(status_code=400, detail=f"Syntax Error: {str(se)}")
        
    except EvaluationError as ee:
        raise HTTPException(status_code=400, detail=f"Evaluation Error: {str(ee)}")



if __name__ == "__main__":
    import uvicorn
    # Start the server on port 5000 as requested
    uvicorn.run(app, host="127.0.0.1", port=5000)