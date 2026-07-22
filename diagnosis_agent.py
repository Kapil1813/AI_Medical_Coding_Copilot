import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from agents.base_agent import BaseAgent
from models.workflow_state import WorkflowState
from models.schemas import Diagnosis

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class DiagnosisAgent(BaseAgent):

    def run(self, state: WorkflowState) -> WorkflowState:

        clinical_note = state.clinical_note.model_dump_json(indent=2)

        prompt = f"""
You are an experienced physician.

Review the structured clinical note.

Determine:

1. Primary diagnosis
2. Secondary diagnoses
3. Supporting clinical evidence
4. Clinical reasoning
5. Confidence score between 0 and 1
6. Missing information

Return ONLY valid JSON.
Clinical Note:

{clinical_note}
"""

        response = client.responses.parse(
            model="gpt-5",
            input=prompt,
            text_format=Diagnosis
        )

        diagnosis = response.output_parsed

        state.diagnosis = diagnosis

        return state