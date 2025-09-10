import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.barcode import code128
from datetime import datetime, timedelta
import io
import os

def save_temp_file(uploaded_file, temp_name):
    if not uploaded_file:
        return None
    data = uploaded_file.read()
    path = temp_name
    with open(path, "wb") as f:
        f.write(data)
    try:
        uploaded_file.seek(0)
    except:
        pass
    return path

def generate_prescription(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    page_width, page_height = A4

    left_x = 40
    right_x = page_width - 40 

    if data.get("logo_path"):
        try:
            c.drawImage(data["logo_path"], left_x, page_height - 90, width=80, height=50, mask='auto')
        except Exception as e:
            pass

    c.setFont("Helvetica-Bold", 12)
    c.drawString(130, page_height - 50, data.get("clinic_name", "Care Clinic"))
    c.setFont("Helvetica", 9)
    c.drawString(130, page_height - 65, data.get("clinic_address", "Kothrud, Pune - 411038"))
    c.drawString(130, page_height - 80, "Ph: " + data.get("clinic_phone", "09423380390") + " | Timing: " + data.get("clinic_timing", "09:00 AM - 02:00 PM"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(right_x - 150, page_height - 50, data.get("doctor_name", "Dr. Onkar Bhave"))
    c.setFont("Helvetica", 9)
    c.drawString(right_x - 150, page_height - 65, data.get("doctor_qual", "M.B.B.S., M.D., M.S. | Reg No: 270988"))
    c.drawString(right_x - 150, page_height - 80, "Mob: " + data.get("doctor_phone", "8983390126"))

    c.setLineWidth(0.6)
    c.line(left_x, page_height - 120, right_x, page_height - 120)

    pid = str(data.get("patient_id", "")).strip()
    pname = data.get("patient_name", "").strip()
    barcode_value = f"ID:{pid}-{pname[:10].upper()}" if pid or pname else "ID:00-DEMOPAT"
    try:
        barcode = code128.Code128(barcode_value, barHeight=28, barWidth=0.5)
        barcode_x = left_x
        barcode_y = page_height - 165
        barcode.drawOn(c, barcode_x, barcode_y)
    except Exception as e:
        c.setFont("Helvetica", 8)
        c.drawString(left_x, page_height - 165, barcode_value)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, page_height - 190, f"ID: {pid}  -  {pname}  / {data.get('patient_gender','M')}  / {data.get('patient_age','')} Y")
    c.setFont("Helvetica", 9)
    c.drawString(left_x, page_height - 205, f"Address: {data.get('patient_address','')}")
    c.drawString(left_x, page_height - 220, f"Weight(kg): {data.get('weight','')} , Height (cms): {data.get('height','')} , BP: {data.get('bp','')}")
    c.drawRightString(right_x, page_height - 190, "Date: " + datetime.now().strftime("%d-%b-%Y, %I:%M %p"))

    y = page_height - 245
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, y, "Referred By:")
    c.setFont("Helvetica", 9)
    c.drawString(left_x + 90, y, data.get("referred_by",""))
    y -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, y, "Known History Of")
    c.setFont("Helvetica", 9)
    kh = data.get("known_history","").split("\\n")
    yy = y - 12
    for k in kh:
        if k.strip():
            c.drawString(left_x + 8, yy, "* " + k.strip())
            yy -= 12

    line_y = yy - 8
    c.setLineWidth(0.8)
    c.line(left_x, line_y, right_x, line_y)

    y_section = line_y - 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x + 10, y_section, "Chief Complaints")
    c.drawString(page_width/2 + 20, y_section, "Clinical Findings")
    y_headers_line = y_section - 6
    c.setLineWidth(0.6)
    c.line(left_x + 10, y_headers_line, right_x - 10, y_headers_line)

    y_content = y_headers_line - 14
    c.setFont("Helvetica", 9)
    c.drawString(left_x + 12, y_content, data.get("chief_complaints","*"))
    c.drawString(page_width/2 + 22, y_content, data.get("clinical_findings","*"))

    y_content -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, y_content, "Notes:")
    c.setFont("Helvetica", 9)
    c.drawString(left_x + 50, y_content, data.get("notes",""))

    y_content -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, y_content, "Diagnosis:")
    c.setFont("Helvetica", 9)
    c.drawString(left_x + 70, y_content, data.get("diagnosis",""))

    y_content -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, y_content, "Procedures conducted")
    c.setFont("Helvetica", 9)
    c.drawString(left_x + 140, y_content, data.get("procedures",""))

    y_meds_top = y_content - 36
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, y_meds_top, "Rx")
    c.drawString(left_x + 30, y_meds_top, "Medicine Name")
    c.drawString(left_x + 300, y_meds_top, "Dosage")
    c.drawString(left_x + 420, y_meds_top, "Duration")

    c.setLineWidth(0.8)
    c.line(left_x, y_meds_top - 6, right_x, y_meds_top - 6)

    y_med = y_meds_top - 24
    c.setFont("Helvetica", 9)
    medicines = data.get("medicines", [])
    for idx, m in enumerate(medicines, start=1):
        c.drawString(left_x + 10, y_med, f"{idx}) {m.get('name','')}")
        c.drawString(left_x + 270, y_med, m.get('dosage',''))
        c.drawString(left_x + 410, y_med, m.get('duration',''))
        y_med -= 18

    y_after = y_med - 10
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, y_after, "Investigations:")
    c.setFont("Helvetica", 9)
    invs = data.get("investigations","").split("\\n")
    yy = y_after - 12
    for inv in invs:
        if inv.strip():
            c.drawString(left_x + 8, yy, "* " + inv.strip())
            yy -= 12

    yy -= 6
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, yy, "Advice Given:")
    c.setFont("Helvetica", 9)
    c.drawString(left_x + 80, yy, data.get("advice",""))

    yy -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, yy, "Follow Up:")
    c.setFont("Helvetica", 9)
    c.drawString(left_x + 70, yy, (datetime.now() + timedelta(days=int(data.get("follow_up_days",7)))).strftime("%d-%b-%Y"))

    if data.get("signature_path"):
        try:
            c.drawImage(data["signature_path"], page_width - 180, 60, width=140, height=55, mask='auto')
        except Exception as e:
            pass

    c.setFont("Helvetica-Bold", 10)
    c.drawString(page_width - 160, 48, data.get("doctor_name","Dr. Onkar Bhave"))
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="Prescription Generator", layout="wide")
st.title("🩺 Fake Prescription Generator — Template Replica")

with st.sidebar:
    st.header("Doctor & Clinic (editable)")
    doctor_name = st.text_input("Doctor Name", "Dr. Onkar Bhave")
    doctor_qual = st.text_input("Doctor Qualification / Reg No", "M.B.B.S., M.D., M.S. | Reg No: 270988")
    doctor_phone = st.text_input("Doctor Mobile", "8983390126")
    clinic_name = st.text_input("Clinic Name", "Care Clinic")
    clinic_address = st.text_input("Clinic Address", "Kothrud, Pune - 411038")
    clinic_phone = st.text_input("Clinic Phone", "09423380390")
    clinic_timing = st.text_input("Clinic Timing", "09:00 AM - 02:00 PM")

    st.header("Patient Information")
    patient_id = st.text_input("Patient ID", "14")
    patient_name = st.text_input("Patient Name", "DEMO PATIENT")
    patient_age = st.number_input("Age (years)", 1, 120, 9)
    patient_gender = st.selectbox("Gender", ["M","F","Other"])
    patient_address = st.text_input("Address", "KOTHRUD, PUNE")
    weight = st.text_input("Weight (kg)", "58")
    height_cm = st.text_input("Height (cms)", "130")
    bp = st.text_input("BP", "120/80")

    st.header("Clinical Details")
    referred_by = st.text_input("Referred By", "Dr. Rane")
    known_history = st.text_area("Known History (one per line)", "ABC\\nPQR")
    chief_complaints = st.text_input("Chief Complaints", "ACIDITY (2 DAYS)")
    clinical_findings = st.text_input("Clinical Findings", "DEMO FINDING 1")
    notes = st.text_input("Notes", "SAMPLE INTERNAL NOTE")
    diagnosis = st.text_input("Diagnosis", "FEVER")
    procedures = st.text_input("Procedures conducted", "DEMO PROCEDURE")

    st.header("Medicines")
    num_meds = st.number_input("Number of Medicines", 1, 6, 2)
    medicines = []
    for i in range(num_meds):
        st.subheader(f"Medicine {i+1}")
        mname = st.text_input(f"Name {i+1}", f"TAB. DEMO MEDICINE {i+1}", key=f"name{i}")
        mdos = st.text_input(f"Dosage {i+1}", "1 Morning, 1 Night (Before Food)", key=f"dos{i}")
        mdur = st.text_input(f"Duration {i+1}", "8 Days (Tot:20 Tab)", key=f"dur{i}")
        medicines.append({"name": mname, "dosage": mdos, "duration": mdur})

    st.header("Other")
    investigations = st.text_area("Investigations (one per line)", "X-RAY\\nP-53")
    advice = st.text_input("Advice", "AVOID OILY AND SPICY FOOD")
    follow_up_days = st.number_input("Follow-up after (days)", 1, 60, 7)

    st.header("Upload Images (optional)")
    logo_file = st.file_uploader("Upload Logo (png/jpg)", type=["png","jpg","jpeg"])
    signature_file = st.file_uploader("Upload Signature (png/jpg)", type=["png","jpg","jpeg"])

    generate = st.button("Generate Prescription PDF")

if generate:
    logo_path = save_temp_file(logo_file, "temp_logo.png") if 'logo_file' in locals() and logo_file else None
    signature_path = save_temp_file(signature_file, "temp_sig.png") if 'signature_file' in locals() and signature_file else None

    payload = {
        "doctor_name": doctor_name,
        "doctor_qual": doctor_qual,
        "doctor_phone": doctor_phone,
        "clinic_name": clinic_name,
        "clinic_address": clinic_address,
        "clinic_phone": clinic_phone,
        "clinic_timing": clinic_timing,
        "patient_id": patient_id,
        "patient_name": patient_name,
        "patient_age": patient_age,
        "patient_gender": patient_gender,
        "patient_address": patient_address,
        "weight": weight,
        "height": height_cm,
        "bp": bp,
        "referred_by": referred_by,
        "known_history": known_history,
        "chief_complaints": chief_complaints,
        "clinical_findings": clinical_findings,
        "notes": notes,
        "diagnosis": diagnosis,
        "procedures": procedures,
        "medicines": medicines,
        "investigations": investigations,
        "advice": advice,
        "follow_up_days": follow_up_days,
        "logo_path": logo_path,
        "signature_path": signature_path
    }

    pdf_buffer = generate_prescription(payload)
    st.success("✅ Prescription generated successfully!")
    st.download_button("📥 Download Prescription", data=pdf_buffer, file_name="fake_prescription_v2.pdf", mime="application/pdf")
else:
    st.info("Fill the sidebar form and click 'Generate Prescription PDF' to create the PDF.")