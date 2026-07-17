from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    question: str = Field(min_length=2, max_length=200)
    signal: str = Field(min_length=2)
    brute_force: str = Field(min_length=2)
    useful_memory: str = Field(min_length=2)
    pattern: str = Field(min_length=2, max_length=100)
    key_question: str = Field(min_length=2)
    solution_approach: str = Field(min_length=2)
    time_complexity: str = Field(min_length=1, max_length=50)
    space_complexity: str = Field(min_length=1, max_length=50)


class NoteCreate(NoteBase):
    category_id: int


class NoteRead(NoteBase):
    id: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)
