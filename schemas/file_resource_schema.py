from typing import Optional
from pydantic import *

class getImageSchema(BaseModel):
    space_id: int
    filename: str