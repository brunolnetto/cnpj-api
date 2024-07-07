from fastapi import HTTPException, status

class ExpiredTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401, 
            detail="Token has expired. Generate another token with application secret."
        )

class MissingTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is missing",
        )


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is invalid",
        )