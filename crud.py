from http.client import HTTPException

from models import Resume
from database import AsyncSessionLocal
from sqlalchemy.future import select

# The function is used to save the Resume Into DB
async def save_resume(file_name, data):
    try:
        # coverting String data to Json format
        if isinstance(data, str):
            import json
            data = json.loads(data)

        # print("Data to save:", data)

        async with AsyncSessionLocal() as session:
            resume = Resume(
                file_name=file_name,
                name=data.get("name", ""),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                skills=data.get("skills", []),
                experience=data.get("experience", ""),
                suggestions=data.get("upskill_suggestions", ""),
                recommended_skills=data.get("improvement_areas", [])
            )
            session.add(resume)
            await session.commit()
            # print(f" Saved resume ID: {resume.id}")
            return resume.id
    except json.JSONDecodeError:
        print("Invalid JSON data")
        raise HTTPException(status_code=400, detail="Invalid resume data format")
    except Exception as e:
        print(f" Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save resume")
#Function Returns all resumes from Db
async def get_resume():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Resume))
        resumes = result.scalars().all()
        return [{"id": r.id, "file_name": r.file_name, "name": r.name, "email": r.email, "phone": r.phone, "created_at": r.created_at,"suggestions":r.suggestions,"recommended_skills":r.recommended_skills} for r in resumes]
# function to returns resumes by id from DB
async def get_resume_id(resume_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Resume).where(Resume.id == resume_id))
        resume = result.scalar_one_or_none()
        return {
            "id": resume.id,
            "file_name": resume.file_name,
            "name": resume.name,
            "email": resume.email,
            "phone": resume.phone,
            "skills": resume.skills,
            "experience": resume.experience,
            "suggestions": resume.suggestions,
            "recommended_skills": resume.recommended_skills,
            "created_at": resume.created_at
        } if resume else None
