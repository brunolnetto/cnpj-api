from fastapi import HTTPException

class ExpiredTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401, 
            detail="Token has expired. Generate another token with application secret."
        )