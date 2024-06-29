from .base import BaseModel
from datetime import datetime

class FileInfo(BaseModel):
  """
  Pydantic model representing a CNPJ file.

  Attributes:
    filename (str): The name of the CNPJ file.
    updated_at (datetime): The date and time when the CNPJ file was last updated.
  """
  filename: str
  updated_at: datetime
  file_size_bytes: int = 0
  
  def __dict__(self):
    return {
      "filename": self.filename,
      "updated_at": self.updated_at,
      "file_size_bytes": self.file_size
    }