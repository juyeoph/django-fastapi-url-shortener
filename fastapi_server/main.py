from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@db:5432/shortener_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "shortener_url"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    click_count = Column(Integer, default=0)

app = FastAPI()

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return

@app.get("/{short_code}")
def redirect_to_original_url(short_code: str):
    db = SessionLocal()
    url_record = db.query(URL).filter(URL.short_code == short_code).first()

    if url_record:
        # 클릭 횟수 1 증가
        url_record.click_count += 1
        db.commit()
        db.refresh(url_record)
        db.close()
        return RedirectResponse(url=url_record.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    db.close()
    raise HTTPException(status_code=404, detail="URL not found")