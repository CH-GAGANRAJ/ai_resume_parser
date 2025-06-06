from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import database, crud, resume_parser,utils
import shutil
import os

app = FastAPI()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#To Intitialized the Database
@app.on_event('startup')
async def startup():
    await database.init_db()
    #print(" Database initialized")

# To Upload resume and update to the "uploads" file and Take LLM suggetions and save to DB
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        text = utils.convert_resume_to_text(file_path)
        result = resume_parser.llm_suggestion(text)

        await crud.save_resume(file.filename, result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#To get all the saved resumes in DB
@app.get('/get_resume/')
async def get_resume():
    return await crud.get_resume()

#To get resumes by Id
@app.get("/get_resume_id/{resume_id}")
async def get_resume_id(resume_id: int):
    return await crud.get_resume_id(resume_id)

from dotenv import load_dotenv
load_dotenv()


