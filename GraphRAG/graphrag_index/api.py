from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tiktoken
import uvicorn
import os
import subprocess
import asyncio
import logging

_ = load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/search/drift")
# async def drift_search(query: str = Query(..., description="DRIFT search query")):
#     try:
#         result = await drift_search_engine.asearch(query)
#         response_dict = {
#             "response": convert_response_to_string(result.response["nodes"][0]["answer"]),
#             "context_data": process_context_data(result.context_data),
#             "context_text": result.context_text,
#             "completion_time": result.completion_time,
#             "llm_calls": result.llm_calls,
#             "llm_calls_categories": result.llm_calls_categories,
#             "output_tokens":result.output_tokens,
#             "output_tokens_categories":result.output_tokens_categories,
#             "prompt_tokens": result.prompt_tokens,            
#             "prompt_tokens_categories": result.prompt_tokens_categories        
#         }
#         return JSONResponse(content=response_dict)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

logger = logging.getLogger("global_search")
logging.basicConfig(level=logging.DEBUG)

@app.get("/search/global")
async def global_search(query: str = Query(..., description="Search query for global context")):
    try:
        cwd = os.path.join(os.getcwd())
        
        command = [
            # "conda",
            # "run",
            # "-n",
            # "retrieval",
            "python",
            "-m",
            "graphrag",
            "query",
            # "--root",
            # ".",
            "--method",
            "global",
            "--query",
            query,
        ]
        
        logger.debug("Executing command in directory: %s", cwd)
        logger.debug("Command: %s", " ".join(command))
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd  
        )
        stdout, stderr = await process.communicate()

        stdout_decoded = stdout.decode().strip()
        stderr_decoded = stderr.decode().strip()
        
        logger.debug("Command stdout: %s", stdout_decoded)
        logger.debug("Command stderr: %s", stderr_decoded)

        if process.returncode != 0:
            logger.error("Error in global search with return code %s", process.returncode)
            raise HTTPException(status_code=500, detail=stderr_decoded)

        return JSONResponse(content={"response": stdout_decoded})
    
    except Exception as e:
        logger.exception("Exception occurred during global search")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/local")
async def local_search(query: str = Query(..., description="Search query for local context")):
    try:
        cwd = os.path.join(os.getcwd())
        
        command = [
            "python",
            "-m",
            "graphrag",
            "query",
            "--method",
            "local",
            "--query",
            query,
        ]
        
        logger.debug("Executing command in directory: %s", cwd)
        logger.debug("Command: %s", " ".join(command))
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd  
        )
        stdout, stderr = await process.communicate()

        stdout_decoded = stdout.decode().strip()
        stderr_decoded = stderr.decode().strip()
        
        logger.debug("Command stdout: %s", stdout_decoded)
        logger.debug("Command stderr: %s", stderr_decoded)

        if process.returncode != 0:
            logger.error("Error in local search with return code %s", process.returncode)
            raise HTTPException(status_code=500, detail=stderr_decoded)

        return JSONResponse(content={"response": stdout_decoded})
    
    except Exception as e:
        logger.exception("Exception occurred during local search")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/status")
async def status():
    return JSONResponse(content={"status": "Server is up and running"})


if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8000)
