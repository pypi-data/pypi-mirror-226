from fastapi import FastAPI, Request, HTTPException, Depends, Body
import os
import threading
import sh
import shutil
import yaml 

app = FastAPI()

def run_webhook_job():
    repo_path = "/temprepo"
    proper_repo_path = "/repo"
    
    # 1. Remove /repo directory and recreate it
    shutil.rmtree(repo_path, ignore_errors=True)
    os.makedirs(repo_path)

    # 2. Git clone the repo into /repo
    sh.git.clone("git@gitlab.atro.xyz:inf/charts.git", repo_path)

    # 3. Read the .mkdocs.repos.yaml file inside of the /repo
    with open(os.path.join(repo_path, ".mkdocs.repos.yaml"), 'r') as file:
        repos = yaml.safe_load(file)

    for name, repo_url in repos.items():
        # 4. Clone repo into a temporary directory
        temp_dir = f"/tmp/{name}"
        
        # Considering an optimization to not clone the whole thing each time...
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            print(f"The path {temp_dir} already exists, instead of creating simply git pulling")
            with sh.pushd(temp_dir):
                sh.git.reset("--hard")
                sh.git.pull()
            continue
        
        shutil.rmtree(temp_dir, ignore_errors=True)
        sh.git.clone(repo_url, temp_dir)

        # 5. rsync excluding docs directory
        sh.rsync("-avz", "--exclude", "docs", f"{temp_dir}/", repo_path)

        # 6. rsync docs contents to /repo/docs/<NAME_FROM_YAML>
        sh.rsync("-avz", f"{temp_dir}/docs/", f"{repo_path}/docs/{name}")

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
    

    # List all items in the /repo directory
    # In order to keep "auto-upadte" we can't delete the docs directory, all other directories should be deleted and docs should be empited
    items = os.listdir(proper_repo_path)

    for item in items:
        item_path = os.path.join(proper_repo_path, item)
        
        # If the item is the 'docs' directory, delete its contents
        if item == "docs" and os.path.isdir(item_path):
            docs_contents = os.listdir(item_path)
            for content in docs_contents:
                content_path = os.path.join(item_path, content)
                if os.path.isfile(content_path) or os.path.islink(content_path):
                    os.unlink(content_path)  # Remove files or links
                elif os.path.isdir(content_path):
                    shutil.rmtree(content_path)  # Remove subdirectories

        # For other directories, delete them
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    
    sh.rsync("-avz", f"{repo_path}/", proper_repo_path)

@app.post("/webhook")
async def webhook(body = Body(), repo = Depends()):
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

if __name__ == "__main__":
    run_job()
