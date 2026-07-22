import os

from dotenv import load_dotenv
from openai import OpenAI

from agents.base_agent import BaseAgent
from models.workflow_state import WorkflowState
from models.schemas import ICDCodingResult

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class ICDAgent(BaseAgent):

    def run(self, state: WorkflowState) -> WorkflowState:

        if state.diagnosis is None:
            raise ValueError("Diagnosis Agent must run before ICD Agent.")

        diagnosis_json = state.diagnosis.model_dump_json(indent=2)

        prompt = f"""
You are an AHIMA Certified Medical Coder.

Assign ICD-10-CM diagnosis codes ONLY.

Return valid JSON matching this schema.

Diagnosis:
{diagnosis_json}
"""

        response = client.responses.parse(
            model="gpt-5",
            input=prompt,
            text_format=ICDCodingResult,
        )

        state.icd_result = response.output_parsed

        return state