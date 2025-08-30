from pydantic import BaseModel
from typing import List, Optional

class FieldWithConfidence(BaseModel):
    value: Optional[str] = None
    confidence: Optional[float] = None

class Subject(BaseModel):
    subject_name: Optional[FieldWithConfidence] = None
    max_marks: Optional[FieldWithConfidence] = None
    obtained_marks: Optional[FieldWithConfidence] = None
    grade: Optional[FieldWithConfidence] = None

class MarksheetData(BaseModel):
    candidate_name: Optional[FieldWithConfidence] = None
    father_name: Optional[FieldWithConfidence] = None
    roll_no: Optional[FieldWithConfidence] = None
    board_university: Optional[FieldWithConfidence] = None
    institution_name: Optional[FieldWithConfidence] = None
    subjects: List[Subject] = []
    overall_result: Optional[FieldWithConfidence] = None

