from sqlalchemy import Column, DateTime, Integer, Text, func

from schema.db import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=True)
    author = Column(Text, nullable=True)
    img_path = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    time_taken = Column(Integer, nullable=True)# in minutes
    servings = Column(Integer, nullable=True)
    ingredients = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
