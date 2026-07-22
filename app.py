"""
app.py

AI Medical Coding Copilot

Workflow
--------
1. Upload / Paste Physician Note
2. Reader Agent
3. Diagnosis Agent
4. ICD Coding Agent
5. Display Results
"""

import streamlit as st

from services.document_loader import DocumentLoader

from models.workflow_state import WorkflowState

from agents.reader_agent import ReaderAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.icd_agent import ICDAgent


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Medical Coding Copilot",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 AI Medical Coding Copilot")
st.caption(
    "AI-powered Clinical Documentation & Medical Coding Assistant"
)

st.divider()


# =====================================================
# INPUT SECTION
# =====================================================

st.header("📄 Upload Clinical Document")

uploaded_file = st.file_uploader(
    "Upload Physician Note",
    type=["pdf", "docx", "txt", "csv"]
)

st.markdown("### OR")

clinical_note = st.text_area(
    "Paste Physician Clinical Note",
    height=250,
    placeholder="Paste physician documentation here..."
)


# =====================================================
# LOAD DOCUMENT
# =====================================================

document_text = ""

try:

    if uploaded_file is not None:

        document_text = DocumentLoader.load(uploaded_file)

    elif clinical_note.strip():

        document_text = clinical_note.strip()

except Exception as e:

    st.error(f"Document Loader Error\n\n{e}")
    st.stop()


# =====================================================
# RUN WORKFLOW
# =====================================================

if document_text:

    st.success("✅ Clinical document loaded successfully.")

    with st.expander(
        "📄 View Raw Clinical Note",
        expanded=False
    ):

        st.text_area(
            "Raw Text",
            document_text,
            height=250
        )

    # =================================================
    # CREATE WORKFLOW STATE
    # =================================================

    state = WorkflowState(
        raw_text=document_text
    )

    # =================================================
    # READER AGENT
    # =================================================

    st.divider()

    st.header("🧠 Reader Agent")

    reader = ReaderAgent()

    with st.spinner("Extracting structured clinical information..."):

        try:

            state = reader.run(state)

        except Exception as e:

            st.error(e)
            st.stop()

    st.success("Reader Agent completed.")

    st.subheader("Structured Clinical Note")

    st.json(
        state.clinical_note.model_dump(),
        expanded=True
    )

    # =================================================
    # DIAGNOSIS AGENT
    # =================================================

    st.divider()

    st.header("🩺 Diagnosis Agent")

    diagnosis_agent = DiagnosisAgent()

    with st.spinner("Determining diagnosis..."):

        try:

            state = diagnosis_agent.run(state)

        except Exception as e:

            st.error(e)
            st.stop()

    if state.diagnosis:

        diagnosis = state.diagnosis

        st.success("Diagnosis generated successfully.")

        st.subheader("Primary Diagnosis")

        st.success(
            diagnosis.primary_diagnosis
        )

        st.subheader("Secondary Diagnoses")

        if diagnosis.secondary_diagnoses:

            for item in diagnosis.secondary_diagnoses:

                st.write(f"• {item}")

        else:

            st.write("None")

        st.subheader("Supporting Evidence")

        if diagnosis.supporting_evidence:

            for evidence in diagnosis.supporting_evidence:

                st.write(f"• {evidence}")

        else:

            st.write("None")

        st.subheader("Clinical Reasoning")

        st.write(
            diagnosis.clinical_reasoning
        )

        st.metric(
            "Diagnosis Confidence",
            f"{diagnosis.confidence:.0%}"
        )

        if diagnosis.missing_information:

            st.warning("Missing Documentation")

            for item in diagnosis.missing_information:

                st.write(f"• {item}")

    else:

        st.warning(
            "Diagnosis Agent returned no diagnosis."
        )

    # =================================================
    # ICD AGENT
    # =================================================

    st.divider()

    st.header("🏷 ICD-10 Coding Agent")

    icd_agent = ICDAgent()

    with st.spinner("Assigning ICD-10-CM codes..."):

        try:

            state = icd_agent.run(state)

        except Exception as e:

            st.error(e)
            st.stop()

    if state.icd_result:

        icd = state.icd_result

        st.success("ICD Coding completed.")

        st.subheader("Primary ICD Code")

        primary = icd.primary_icd

        st.success(
            f"{primary.code} — {primary.description}"
        )

        st.write(
            f"**Diagnosis:** {primary.diagnosis}"
        )

        st.write(
            f"**Rationale:** {primary.rationale}"
        )

        if primary.coding_guideline:

            st.write(
                f"**Coding Guideline:** {primary.coding_guideline}"
            )

        st.metric(
            "Coding Confidence",
            f"{primary.confidence:.0%}"
        )

        st.subheader("Secondary ICD Codes")

        if icd.secondary_icds:

            for code in icd.secondary_icds:

                with st.container():

                    st.markdown(
                        f"### {code.code}"
                    )

                    st.write(
                        code.description
                    )

                    st.write(
                        f"Diagnosis: {code.diagnosis}"
                    )

                    st.write(
                        f"Rationale: {code.rationale}"
                    )

                    st.progress(
                        code.confidence
                    )

        else:

            st.write("No secondary ICD codes.")

        if icd.documentation_gaps:

            st.warning(
                "Documentation Gaps"
            )

            for gap in icd.documentation_gaps:

                st.write(f"• {gap}")

        if icd.coder_notes:

            st.info(
                f"Coder Notes:\n\n{icd.coder_notes}"
            )

    else:

        st.warning(
            "ICD Agent did not return coding results."
        )

    # =================================================
    # WORKFLOW STATUS
    # =================================================

    st.divider()

    st.header("🤖 AI Agent Workflow")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.success("✅ Reader")

    with col2:
        st.success("✅ Diagnosis")

    with col3:
        st.success("✅ ICD")

    with col4:
        st.info("⏳ Procedure")

    with col5:
        st.info("⏳ CPT")

    with col6:
        st.info("⏳ Validation")

else:

    st.info(
        "👆 Upload a physician note or paste clinical documentation to begin."
    )