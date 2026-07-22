"""
schemas.py

Defines all Pydantic models used throughout the
AI Medical Coding Copilot workflow.

Workflow
--------
Reader Agent
    -> ClinicalNote

Diagnosis Agent
    -> Diagnosis

ICD Coding Agent
    -> ICDCodingResult

Future
------
Procedure Agent
CPT Agent
Validation Agent
"""

from typing import Optional

from pydantic import BaseModel, Field


# ======================================================
# Diagnosis Model
# ======================================================

class Diagnosis(BaseModel):
    """
    Structured diagnosis produced by the Diagnosis Agent.
    """

    primary_diagnosis: str

    secondary_diagnoses: list[str] = Field(
        default_factory=list
    )

    supporting_evidence: list[str] = Field(
        default_factory=list
    )

    clinical_reasoning: str = ""

    confidence: float = 0.0

    missing_information: list[str] = Field(
        default_factory=list
    )


# ======================================================
# Procedure Model
# ======================================================

class Procedure(BaseModel):
    """
    Medical procedure extracted from the physician note.
    """

    name: str

    result: Optional[str] = None


# ======================================================
# Medication Model
# ======================================================

class Medication(BaseModel):
    """
    Medication extracted from the physician note.
    """

    name: str

    dose: Optional[str] = None

    frequency: Optional[str] = None

    duration: Optional[str] = None


# ======================================================
# Clinical Note Model
# ======================================================

class ClinicalNote(BaseModel):
    """
    Structured physician note produced by the Reader Agent.
    """

    # -----------------------------
    # Patient Information
    # -----------------------------

    patient_name: Optional[str] = None

    age: Optional[int] = None

    gender: Optional[str] = None

    # -----------------------------
    # Clinical Findings
    # -----------------------------

    symptoms: list[str] = Field(
        default_factory=list
    )

    diagnoses: list[Diagnosis] = Field(
        default_factory=list
    )

    procedures: list[Procedure] = Field(
        default_factory=list
    )

    medications: list[Medication] = Field(
        default_factory=list
    )

    # -----------------------------
    # Provider Information
    # -----------------------------

    physician: Optional[str] = None

    provider_notes: list[str] = Field(
        default_factory=list
    )


# ======================================================
# ICD Coding Models
# ======================================================

class ICDCode(BaseModel):
    """
    Represents a single ICD-10-CM diagnosis code.
    """

    diagnosis: str

    code: str

    description: str

    confidence: float = 1.0

    rationale: str = ""

    coding_guideline: Optional[str] = None


class ICDCodingResult(BaseModel):
    """
    Output of the ICD Coding Agent.
    """

    primary_icd: Optional[ICDCode] = None

    secondary_icds: list[ICDCode] = Field(
        default_factory=list
    )

    documentation_gaps: list[str] = Field(
        default_factory=list
    )

    coder_notes: str = ""


# ======================================================
# Future Procedure Coding Models
# ======================================================

class ProcedureCode(BaseModel):
    """
    Placeholder for future procedure coding.
    """

    procedure: str

    code: str

    description: str

    confidence: float = 1.0


class ProcedureCodingResult(BaseModel):
    """
    Placeholder for Procedure Agent output.
    """

    procedures: list[ProcedureCode] = Field(
        default_factory=list
    )


# ======================================================
# Future CPT Coding Models
# ======================================================

class CPTCode(BaseModel):
    """
    Represents a CPT code.
    """

    procedure: str

    code: str

    description: str

    confidence: float = 1.0

    rationale: str = ""


class CPTCodingResult(BaseModel):
    """
    Output of the CPT Coding Agent.
    """

    primary_cpt: Optional[CPTCode] = None

    additional_cpts: list[CPTCode] = Field(
        default_factory=list
    )

    coder_notes: str = ""