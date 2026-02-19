import os
import io
import secrets
import string
import qrcode

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from models import URL
from schemas import ShortenRequest, ShortenResponse, StatsResponse

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

router = APIRouter(tags=["shortener"])

ALPHABET = string.ascii_letters + string.digits

def generate_code(n: int = 6) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(n))


@router.post("/shorten", response_model=ShortenResponse)
def shorten(req: ShortenRequest, db: Session = Depends(get_db)):

    # If user gives alias, use it
    if req.alias:
        code = req.alias

        # check alias already exists
        if db.query(URL).filter(URL.code == code).first():
            raise HTTPException(status_code=409, detail="Alias already taken")
    else:
        # else generate random code
        code = generate_code()
        while db.query(URL).filter(URL.code == code).first():
            code = generate_code()

    row = URL(code=code, original_url=str(req.url))
    db.add(row)
    db.commit()
    db.refresh(row)

    return ShortenResponse(
        code=row.code,
        short_url=f"{BASE_URL}/{row.code}",
        original_url=row.original_url
    )


@router.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    row = db.query(URL).filter(URL.code == code).first()
    if not row:
        raise HTTPException(status_code=404, detail="Short code not found")

    row.clicks += 1
    db.commit()
    return RedirectResponse(url=row.original_url, status_code=307)


@router.get("/stats/{code}", response_model=StatsResponse)
def stats(code: str, db: Session = Depends(get_db)):
    row = db.query(URL).filter(URL.code == code).first()
    if not row:
        raise HTTPException(status_code=404, detail="Short code not found")

    return StatsResponse(
        code=row.code,
        original_url=row.original_url,
        short_url=f"{BASE_URL}/{row.code}",
        clicks=row.clicks,
        created_at=row.created_at.isoformat()
    )


@router.get("/qr/{code}")
def qr(code: str, db: Session = Depends(get_db)):
    row = db.query(URL).filter(URL.code == code).first()
    if not row:
        raise HTTPException(status_code=404, detail="Short code not found")

    short_url = f"{BASE_URL}/{row.code}"

    img = qrcode.make(short_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
