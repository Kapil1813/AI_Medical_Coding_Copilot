"""
reader_agent.py

Agent 1: Reader Agent

Purpose:
--------
Reads an unstructured physician note and converts it into
a structured ClinicalNote object.

Responsibilities:
------------------
✓ Extract patient demographics
✓ Extract symptoms
✓ Extract diagnoses
✓ Extract procedures
✓ Extract medications
✓ Extract provider notes

Does NOT:
---------
✗ Assign ICD-10 codes
✗ Assign CPT codes
✗ Perform medical coding decisions
"""


import json
import os

from dotenv import load_dotenv
from openai import OpenAI


from agents.base_agent import BaseAgent
from models.workflow_state import WorkflowState
from models.schemas import ClinicalNote



# -------------------------------------------------------
# Load Environment Variables
# -------------------------------------------------------

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



class ReaderAgent(BaseAgent):

    """
    Extracts structured clinical information
    from physician documentation.
    """



    # ---------------------------------------------------
    # Automatic JSON Repair Function
    # ---------------------------------------------------

    def repair_output(self, data: dict) -> dict:
        """
        Repairs common LLM formatting mistakes
        before Pydantic validation.
        """


        # -----------------------------------------------
        # Repair procedures
        # -----------------------------------------------

        repaired_procedures = []


        for procedure in data.get("procedures", []):

            if isinstance(procedure, str):

                repaired_procedures.append(
                    {
                        "name": procedure,
                        "result": None
                    }
                )

            elif isinstance(procedure, dict):

                repaired_procedures.append(procedure)



        data["procedures"] = repaired_procedures



        # -----------------------------------------------
        # Repair medications
        # -----------------------------------------------

        repaired_medications = []


        for medication in data.get("medications", []):

            if isinstance(medication, str):

                repaired_medications.append(
                    {
                        "name": medication,
                        "dose": None,
                        "frequency": None,
                        "duration": None
                    }
                )


            elif isinstance(medication, dict):

                repaired_medications.append(medication)



        data["medications"] = repaired_medications



        # -----------------------------------------------
        # Repair provider notes
        # -----------------------------------------------

        provider_notes = data.get(
            "provider_notes",
            []
        )


        if isinstance(provider_notes, str):

            data["provider_notes"] = [
                provider_notes
            ]

        elif provider_notes is None:

            data["provider_notes"] = []



        # -----------------------------------------------
        # Repair diagnoses
        # -----------------------------------------------

        repaired_diagnoses = []


        for diagnosis in data.get(
            "diagnoses",
            []
        ):


            if isinstance(diagnosis, str):

                repaired_diagnoses.append(
                    {
                        "primary_diagnosis": diagnosis,
                        "secondary_diagnoses": [],
                        "supporting_evidence": [],
                        "clinical_reasoning": "",
                        "confidence": 0.0,
                        "missing_information": []
                    }
                )


            elif isinstance(diagnosis, dict):

                repaired_diagnoses.append(diagnosis)



        data["diagnoses"] = repaired_diagnoses



        return data





    # ---------------------------------------------------
    # Main Agent Execution
    # ---------------------------------------------------

    def run(
        self,
        state: WorkflowState
    ) -> WorkflowState:


        system_prompt = """

You are an expert Clinical Documentation Specialist.

Your task is ONLY to extract structured information
from physician notes.

DO NOT:
- Assign ICD-10 codes
- Assign CPT codes
- Make coding decisions
- Add information not present in the note


Extraction Rules:

1. Return ONLY valid JSON.
2. Use null for missing demographic information.
3. Use empty arrays [] when information is unavailable.

IMPORTANT OUTPUT RULES:

- procedures MUST always be JSON objects.
- medications MUST always be JSON objects.
- diagnoses MUST always be JSON objects.
- provider_notes MUST always be an array of strings.

Never return:
- procedures as strings
- medications as strings
- diagnoses as plain text

"""



        user_prompt = """

Extract the physician note into exactly this JSON format:


{
  "patient_name": "",
  "age": null,
  "gender": "",


  "symptoms": [],


  "diagnoses": [
    {
      "primary_diagnosis": "",

      "secondary_diagnoses": [],

      "supporting_evidence": [],

      "clinical_reasoning": "",

      "confidence": 0.0,

      "missing_information": []
    }
  ],


  "procedures": [
    {
      "name": "",
      "result": ""
    }
  ],


  " medications": [
    {
      "name": "",
      "dose": "",
      "frequency": "",
      "duration": ""
    }
  ],


  "physician": "",


  "provider_notes": []

}



Physician Note
================

""" + state.raw_text + """

================


Return ONLY JSON.

"""



        try:


            response = client.chat.completions.create(

                model="gpt-5-mini",

                messages=[

                    {
                        "role": "system",
                        "content": system_prompt
                    },


                    {
                        "role": "user",
                        "content": user_prompt
                    }

                ],


                response_format={
                    "type": "json_object"
                }

            )



            raw_response = (
                response
                .choices[0]
                .message
                .content
            )



            print("\n" + "=" * 80)

            print(
                "READER AGENT RAW RESPONSE"
            )

            print("=" * 80)

            print(raw_response)

            print("=" * 80 + "\n")




            parsed_json = json.loads(
                raw_response
            )



            # -------------------------------------------
            # Repair before validation
            # -------------------------------------------

            parsed_json = self.repair_output(
                parsed_json
            )



            print(
                "✅ JSON repair completed."
            )



            # -------------------------------------------
            # Validate against Pydantic schema
            # -------------------------------------------

            clinical_note = (
                ClinicalNote
                .model_validate(parsed_json)
            )



            state.clinical_note = clinical_note



            print(
                "✅ Reader Agent completed successfully."
            )


            return state



        except json.JSONDecodeError as e:


            raise Exception(
                f"""
Reader Agent returned invalid JSON.

{e}
"""
            )



        except Exception as e:


            raise Exception(
                f"""
Reader Agent failed.

{e}
"""
            )