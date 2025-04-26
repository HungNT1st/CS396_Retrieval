from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from vectorDB import query
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "UMass RSO Checker is working :D"}

@app.post('/check')
async def check(request: Request):
    """
    Validates the request data and performs a query based on the provided fields.
    Args:
        request (Request): The incoming HTTP request containing JSON data with the following fields:
            - name (str): The name of the entity.
            - categories (str): Categories associated with the entity.
            - summary (str): A brief summary of the entity.
            - description (str): A detailed description of the entity.
    Raises:
        HTTPException: If any of the required fields are missing.
    Returns:
        dict: The result of the context query based on the provided data.
    """
    data = await request.json()
    name = data.get("name")
    categories = data.get("categories")
    summary = data.get("summary")
    description = data.get("description")

    if not all([name, categories, summary, description]):
        raise HTTPException(status_code=400, detail="All fields are required")

    # Assuming the query function processes the data and returns a result
    query_text = f"NAME: {name} CATEGORIES: {categories} SUMMARY: {summary} DESCRIPTION: {description}"
    res = query.check(query_text, 3)
    print(res)
    
    return res
    # res = query.check(query_text, 10)
    # matches = []
    # for rso in res['matches']:
    #     text = rso['metadata']['text']
    #     score = rso['score']
    #     start = text.find("NAME: ") + len("NAME: ")
    #     end = text.find(".", start)
    #     name = text[start:end].strip()
    #     matches.append({ "name": name, "score": score })
    # return matches
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)