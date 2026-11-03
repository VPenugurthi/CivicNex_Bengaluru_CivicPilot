from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..services.seed import seed_demo_data
from fastapi import Depends

router = APIRouter(prefix="/demo", tags=["Demo Data"])

@router.post("/reset")
def reset_demo_data(db: Session = Depends(get_db)):
    seed_demo_data(db)
    return {"status": "success", "message": "Demo data has been reset to default scenarios."}
