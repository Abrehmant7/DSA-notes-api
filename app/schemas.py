from pydantic import BaseModel, ConfigDict, Field

# thsese are different from models, models describe database 
# and pydantic schema describes shape of your API response
# its responsible for validation, serialization and parsing 
# its simialr to serializers in django rest framework.

class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
    )

# for example this represents when category data is read 
# what data is returned
class CategoryRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


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

    # Pydantic needs permission to read values from their attributes
    # this is why we use this here
    # This is similar to how a DRF ModelSerializer knows how to
    # read fields from a Django model instance.
    model_config = ConfigDict(from_attributes=True)


class NoteCreate(NoteBase):
    category_id: int


class NoteRead(NoteBase):
    id: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)