from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from models.user import User
from models.profile import AboutMe, WorkExperience, Education
from schemas.profile import (
    AboutMeCreate,
    WorkExperienceCreate,
    WorkExperienceUpdate,
    EducationCreate
)
from deps import get_current_user
from database import get_session
from crud import (
    get_about_me,
    create_or_update_about_me,
    create_work_experience,
    get_user_work_experiences,
    update_work_experience,
    delete_work_experience,
    create_education,
    get_user_educations
)

router = APIRouter(prefix="/profile", tags=["profile"])


# ============================
#        ABOUT ME
# ============================

@router.get("/about-me", response_model=AboutMe)
async def get_my_about_me(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    about_me = get_about_me(session, current_user.id)
    if not about_me:
        return AboutMe(user_id=current_user.id)
    return about_me


@router.put("/about-me", response_model=AboutMe)
async def update_about_me(
    about_data: AboutMeCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return create_or_update_about_me(
        session=session,
        user_id=current_user.id,
        **about_data.dict(exclude_unset=True)
    )


# ============================
#   WORK EXPERIENCE
# ============================

@router.post("/work-experiences", response_model=WorkExperience)
async def add_work_experience(
    experience: WorkExperienceCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return create_work_experience(
        session=session,
        user_id=current_user.id,
        **experience.dict()
    )


@router.get("/work-experiences", response_model=List[WorkExperience])
async def get_my_work_experiences(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_user_work_experiences(session, current_user.id)


@router.put("/work-experiences/{experience_id}", response_model=WorkExperience)
async def update_my_work_experience(
    experience_id: int,
    experience_data: WorkExperienceUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    experience = session.get(WorkExperience, experience_id)
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiencia no encontrada"
        )

    if experience.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta experiencia"
        )

    return update_work_experience(
        session=session,
        experience_id=experience_id,
        **experience_data.dict(exclude_unset=True)
    )


@router.delete("/work-experiences/{experience_id}")
async def delete_my_work_experience(
    experience_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    experience = session.get(WorkExperience, experience_id)
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiencia no encontrada"
        )

    if experience.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta experiencia"
        )

    success = delete_work_experience(session, experience_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la experiencia"
        )

    return {"message": "Experiencia eliminada correctamente"}


# ============================
#          EDUCATION
# ============================

@router.post("/educations", response_model=Education)
async def add_education(
    education: EducationCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return create_education(
        session=session,
        user_id=current_user.id,
        **education.dict()
    )


@router.get("/educations", response_model=List[Education])
async def get_my_educations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_user_educations(session, current_user.id)
