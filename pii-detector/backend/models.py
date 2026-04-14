from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    pii_detected = Column(Text, nullable=True)  # Store detected PII information
    redacted_content = Column(Text, nullable=True)  # Store redacted content

    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename})>"