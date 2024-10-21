from pydantic import BaseModel, EmailStr


# final
class SearchRequest(BaseModel):
    """
    Search Request
    contains email search string
    """
    email: EmailStr
