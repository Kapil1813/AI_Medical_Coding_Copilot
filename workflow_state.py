"""
workflow_state.py

Shared workflow state passed between every AI agent
in the AI Medical Coding Copilot.

Workflow
--------
Raw Physician Note
        │
        ▼
Reader Agent
        │
        ▼
ClinicalNote
        │
        ▼
Diagnosis Agent
        │
        ▼
Diagnosis
        │
        ▼
ICD Coding Agent
        │
        ▼
ICDCodingResult
        │
        ▼
Procedure Agent
        │
        ▼
ProcedureCodingResult
        │
        ▼
CPT Coding Agent
        │
        ▼
CPTCodingResult
        │
        ▼
Validation Agent
        │
        ▼
Explainability Agent
"""

from typing import Optional

from pydantic import BaseModel

from models.schemas import (
    ClinicalNote,
    Diagnosis,
    ICDCodingResult,
    ProcedureCodingResult,
    CPTCodingResult,
)


class WorkflowState(BaseModel):
    """
    Shared workflow state passed between all AI agents.
    """

    # ==================================================
    # Original Input
    # ==================================================

    raw_text: str = ""

    # ==================================================
    # Reader Agent Output
    # ==================================================

    clinical_note: Optional[ClinicalNote] = None

    # ==================================================
    # Diagnosis Agent Output
    # ==================================================

    diagnosis: Optional[Diagnosis] = None

    # ==================================================
    # ICD Coding Agent Output
    # ==================================================

    icd_result: Optional[ICDCodingResult] = None

    # ==================================================
    # Future Procedure Agent Output
    # ==================================================

    procedure_result: Optional[ProcedureCodingResult] = None

    # ==================================================
    # Future CPT Agent Output
    # ==================================================

    cpt_result: Optional[CPTCodingResult] = None

    # ==================================================
    # Validation Agent Output
    # ==================================================

    validation_result: Optional[dict] = None

    # ==================================================
    # Explainability Agent Output
    # ==================================================

    explainability_result: Optional[dict] = None

    # ==================================================
    # Overall Workflow
    # ==================================================

    confidence_score: float = 0.0

    final_summary: str = ""

    processing_complete: bool = False

    workflow_status: str = "Initialized"