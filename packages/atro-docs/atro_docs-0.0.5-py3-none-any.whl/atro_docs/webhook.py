from fastapi import FastAPI, Request, HTTPException
import os
import threading
from temp_dir import reset_already_existing_repos, fill_up_docs_and_mkdocs_yml

app = FastAPI()

def run_webhook_job():
    reset_already_existing_repos()
    fill_up_docs_and_mkdocs_yml()
    

@app.post("/webhook")
async def webhook(request: Request):
    # GitHub secret
    secret = os.environ.get("ATRO_WEBHOOK_SECRET")

    # Get the request headers and payload
    headers = request.headers

    if secret:
        header = headers.get("X-Gitlab-Token")
        if not header:
            raise HTTPException(status_code=400, detail="No Signature provided.")
        if header != secret:
            raise HTTPException(status_code=400, detail="Mismatched signatures")
    
    # Use threading to run job in the background
    thread = threading.Thread(target=run_webhook_job)
    thread.start()

    return {"status": "OK"}  

#uvicorn.run(app, host="0.0.0.0", port=9000, reload=True)