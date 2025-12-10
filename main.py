from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
import os
from fastapi.middleware.cors import CORSMiddleware


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
        with open(filename, "wb") as f:
            f.write(file.read())


@app.post("/files")
async def upload_file(upl_file:UploadFile):
    file = upl_file.file
    filename = upl_file.filename
    with open(filename, "wb") as f:
        f.write(file.read())


@app.get("/files/{filename}")
async def get_file(filename:str):
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(filename)


@app.get("/all_files")
async def view_all_files():
    files = []
    for f in os.listdir("."):
        if os.path.isfile(f):
            files.append(f)
    return {"response":files}


def iterfile(filename:str):
    with open(filename, "rb") as f:
        while chunk:=f.read(1024*1024):
            yield chunk

@app.get("/files_stream/{filename}")
async def get_file_stream(filename:str):
    return StreamingResponse(iterfile(filename), media_type="video/mp4")