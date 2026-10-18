from fastapi import FastAPI, HTTPException, Request, Cookie
from fastapi.responses import PlainTextResponse, HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
async def calculator_frontend():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MA4 Calculator</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
            input { width: 75%; padding: 10px; font-size: 16px; }
            button { padding: 10px 15px; font-size: 16px; cursor: pointer; }
            #terminal { margin-top: 20px; padding: 15px; background: #1e1e1e; color: #00ff00; white-space: pre-wrap; font-family: monospace; border-radius: 5px; min-height: 200px;}
        </style>
    </head>
    <body>
        <h2>MA4 Calculator</h2>
        <div>
            <input type="text" id="expr" placeholder="Enter expression, e.g. ((3+5=a)+4=b)+8" onkeydown="if(event.key === 'Enter') calc()">
            <button onclick="calc()">Calculate</button>
        </div>
        <div id="terminal">Ready...</div>

        <script>
            async function calc() {
                const exprInput = document.getElementById('expr');
                const expr = exprInput.value;
                if (!expr) return;
                
                const terminal = document.getElementById('terminal');
                
                try {
                    // Send the raw text to your /statement endpoint
                    const response = await fetch('/statement', {
                        method: 'POST',
                        headers: { 'Content-Type': 'text/plain' },
                        body: expr
                    });
                    
                    const resultText = await response.text();
                    
                    if (response.ok) {
                        terminal.textContent += "\\n\\n> " + expr + "\\nResult: " + resultText.trim();
                    } else {
                        // Extract FastAPI's JSON error detail if it throws a 400 Bad Request
                        let errorMsg = resultText;
                        try {
                            errorMsg = JSON.parse(resultText).detail;
                        } catch(e) {}
                        terminal.textContent += "\\n\\n> " + expr + "\\n" + errorMsg;
                    }
                    
                    exprInput.value = '';
                    terminal.scrollTop = terminal.scrollHeight; // Auto-scroll
                    
                } catch (err) {
                    terminal.textContent += "\\n\\n> " + expr + "\\nConnection failed: " + err;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4998)