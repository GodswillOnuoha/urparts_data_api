from sqlmodel import create_engine, Session
import logging

DATABASE_URL = "postgresql://postgres:fake_password@db/urparts"

engine = create_engine(DATABASE_URL)
sessionLocal = Session(bind=engine)
log_level = logging.DEBUG
