from fastapi import FastAPI, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select

from models import *
from connecton import init_db, get_session

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.post("/warrior")
def warriors_create(warrior: WarriorCreateOrUpdate, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Warrior}):
    warrior_data = warrior.model_dump(exclude={"skills_ids"})
    warrior_obj = Warrior(**warrior_data)

    if warrior.skills_ids:
        skills = session.exec(select(Skill).where(Skill.id.in_(warrior.skills_ids))).all()
        warrior_obj.skills = skills

    session.add(warrior_obj)
    session.commit()
    session.refresh(warrior_obj)
    return {"status": 200, "data": warrior_obj}


@app.get("/warrior/{warrior_id}", response_model=WarriorProfessions)
def warriors_get(warrior_id: int, session=Depends(get_session)) -> Warrior:
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior


@app.patch("/warrior/{warrior_id}")
def warrior_update(warrior_id: int, warrior: WarriorCreateOrUpdate, session=Depends(get_session)) -> Warrior:
    db_warrior = session.get(Warrior, warrior_id)
    if not db_warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    warrior_data = warrior.model_dump(exclude_unset=True, exclude={"skills_ids"})
    for key, value in warrior_data.items():
        setattr(db_warrior, key, value)

    # Если передали новые skills_ids — меняем
    if warrior.skills_ids is not None:
        skills = session.exec(select(Skill).where(Skill.id.in_(warrior.skills_ids))).all()
        db_warrior.skills = skills

    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    return db_warrior


@app.delete("/warrior/delete/{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}


@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    prof = session.get(Profession, profession_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profession not found")
    return prof


@app.post("/profession")
def profession_create(prof: ProfessionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Profession}):
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}


@app.patch("/profession/{profession_id}")
def profession_update(profession_id: int, prof: ProfessionDefault, session=Depends(get_session)) -> Profession:
    db_prof = session.get(Profession, profession_id)
    if not db_prof:
        raise HTTPException(status_code=404, detail="Profession not found")
    prof_data = prof.model_dump(exclude_unset=True)
    for key, value in prof_data.items():
        setattr(db_prof, key, value)
    session.add(db_prof)
    session.commit()
    session.refresh(db_prof)
    return db_prof


@app.delete("/profession/delete/{profession_id}")
def profession_delete(profession_id: int, session=Depends(get_session)):
    prof = session.get(Profession, profession_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profession not found")
    session.delete(prof)
    session.commit()
    return {"ok": True}


@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skill/{skill_id}")
def skill_get(skill_id: int, session=Depends(get_session)) -> Skill:
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@app.post("/skill")
def skill_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Skill}):
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}


@app.patch("/skill/{skill_id}")
def skill_update(skill_id: int, skill: SkillDefault, session=Depends(get_session)) -> Skill:
    db_skill = session.get(Skill, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill_data = skill.model_dump(exclude_unset=True)
    for key, value in skill_data.items():
        setattr(db_skill, key, value)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill


@app.delete("/skill/delete/{skill_id}")
def skill_delete(skill_id: int, session=Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}
