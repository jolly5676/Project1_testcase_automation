import streamlit as st
import os
from backend.requirements_generator import RequirementsGenerator
from backend.gherkin_generator import GherkinGeneratorHybrid

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="Hybrid Requirement → Gherkin Generator",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Hybrid Requirement → Gherkin Generator")
st.markdown(
    """
    Upload a Python file and automatically generate:
    1️⃣ A **Requirement Document**  
    2️⃣ A **Gherkin Feature File** derived from both the code and requirement  
    """
)

# -----------------------------
# Output directory
# -----------------------------
output_dir = os.path.join(os.getcwd(), "generated_outputs")
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# File Upload Section
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload your Python (.py) file", type=["py"])

if uploaded_file:
    py_code = uploaded_file.read().decode("utf-8")
    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    # ------------------------------------------
    # Step 1: Generate Requirement File
    # ------------------------------------------
    if st.button("🚀 Generate Requirement Document", use_container_width=True, key="generate_req_btn"):
        with st.spinner("✨ Generating Requirement Document..."):
            req_gen = RequirementsGenerator(py_code, uploaded_file.name)
            req_output = req_gen.process()

            # Save file
            req_filename = f"{os.path.splitext(uploaded_file.name)[0]}_requirement.md"
            req_path = os.path.join(output_dir, req_filename)

            with open(req_path, "w", encoding="utf-8") as f:
                f.write(req_output)

            # Store in session
            st.session_state["req_output_text"] = req_output
            st.session_state["req_path"] = req_path
            st.session_state["req_filename"] = req_filename

            st.success(f"📘 Requirement document generated and saved as `{req_filename}`")

# ------------------------------------------
# Step 2: SME Review & Edit Requirement
# ------------------------------------------
if "req_output_text" in st.session_state:
    st.divider()
    st.subheader("✏️ Step 2: Review / Edit Requirement Document")

    edited_req_text = st.text_area(
        "You can edit and update the requirement document below:",
        value=st.session_state["req_output_text"],
        height=350
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Requirement File", use_container_width=True, key="save_req_btn"):
            req_path = st.session_state["req_path"]
            try:
                with open(req_path, "w", encoding="utf-8") as f:
                    f.write(edited_req_text)
                st.session_state["req_output_text"] = edited_req_text
                st.success(f"✅ Requirement file saved successfully at `{req_path}`")
            except Exception as e:
                st.error(f"❌ Error saving requirement file: {e}")

    with col2:
        st.download_button(
            label="⬇️ Download Requirement File",
            data=edited_req_text,
            file_name=st.session_state["req_filename"],
            mime="text/plain",
            use_container_width=True,
            key="download_req_btn"
        )

# ------------------------------------------
# Step 3: Generate Gherkin File from Code + Requirement
# ------------------------------------------
if "req_output_text" in st.session_state and uploaded_file:
    st.divider()
    st.subheader("🧩 Step 3: Generate Gherkin Feature File from Code + Requirement")

    if st.button("✨ Generate Gherkin Feature File", use_container_width=True, key="generate_gherkin_btn"):
        with st.spinner("🧠 Generating Gherkin Feature File using Code + Requirement..."):
            gherkin_gen = GherkinGeneratorHybrid(
                code_text=py_code,
                requirement_text=st.session_state["req_output_text"],
                filename=uploaded_file.name
            )
            gherkin_output = gherkin_gen.process()

            gherkin_filename = f"{os.path.splitext(uploaded_file.name)[0]}_feature.feature"
            gherkin_path = os.path.join(output_dir, gherkin_filename)

            with open(gherkin_path, "w", encoding="utf-8") as f:
                f.write(gherkin_output)

            st.session_state["gherkin_output_text"] = gherkin_output
            st.session_state["gherkin_filename"] = gherkin_filename
            st.session_state["gherkin_path"] = gherkin_path

            st.success(f"🧩 Gherkin feature file generated and saved as `{gherkin_filename}`")

# ------------------------------------------
# Step 4: Review, Edit & Save Gherkin File
# ------------------------------------------
if "gherkin_output_text" in st.session_state:
    st.divider()
    st.subheader("🔍 Step 4: Review / Edit Gherkin Feature File")

    edited_gherkin_text = st.text_area(
        "Edit the generated Gherkin feature file below:",
        value=st.session_state["gherkin_output_text"],
        height=350
    )

    col3, col4 = st.columns(2)
    with col3:
        if st.button("💾 Save Gherkin File", use_container_width=True, key="save_gherkin_btn"):
            gherkin_path = st.session_state["gherkin_path"]
            try:
                with open(gherkin_path, "w", encoding="utf-8") as f:
                    f.write(edited_gherkin_text)
                st.session_state["gherkin_output_text"] = edited_gherkin_text
                st.success(f"✅ Gherkin file saved successfully at `{gherkin_path}`")
            except Exception as e:
                st.error(f"❌ Error saving Gherkin file: {e}")

    with col4:
        st.download_button(
            label="⬇️ Download Gherkin File",
            data=edited_gherkin_text,
            file_name=st.session_state["gherkin_filename"],
            mime="text/plain",
            use_container_width=True,
            key="download_gherkin_btn"
        )

if not uploaded_file and "req_output_text" not in st.session_state:
    st.info("👆 Upload a `.py` file to start generating your Requirement & Gherkin files.")
