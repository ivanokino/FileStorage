from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse

import os
from pathlib import Path
import uvicorn

os.chdir(Path(__file__).parent)
DATA_PATH = Path(__file__).parent / "data"
if not DATA_PATH.exists():
    DATA_PATH.mkdir()
app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],  
#     allow_headers=["*"],  
# )

@app.get("/")
async def root():
   return {"response":"server is working"}


@app.post("/multi_files")
async def upload_multi_files(upl_files: list[UploadFile]):
    for upl_file in upl_files:
        

        file = upl_file.file
        filename = upl_file.filename
        file_path = DATA_PATH / filename
        with open(file_path, "wb") as f:
            f.write(file.read())


@app.post("/files")
async def upload_file(upl_file:UploadFile):
    file = upl_file.file
    filename = upl_file.filename
    file_path = DATA_PATH / filename
    with open(file_path, "wb") as f:
        f.write(file.read())


@app.get("/files/{filename}")
async def get_file(filename:str):
    file_path = DATA_PATH / filename
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(file_path)


@app.get("/all_files")
async def view_all_files():
    files = [str(f) for f in DATA_PATH.iterdir() if f.is_file()]
    if len(files)==0:
        raise HTTPException(status_code=404, detail="data is empty")
    return {"response":files}


def iterfile(filename:str):
    with open(filename, "rb") as f:
        while chunk:=f.read(1024*1024):
            yield chunk

@app.get("/files_stream/{filename}")
async def get_file_stream(filename:str):
    file_path = DATA_PATH / filename
    return StreamingResponse(iterfile(file_path), media_type="video/mp4")

@app.delete("/del_file/{filename}")
def delete_file(filename:str):
    file_path = DATA_PATH / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="file not found")
    file_path.unlink()
    return {"response": "file is deleted"}

if __name__=="__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8000,
                reload=True)
