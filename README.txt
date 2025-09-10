# Fake Prescription Generator

A Python-based web application built with **Streamlit** that allows users to generate customizable prescription documents. Users can add **doctor information, patient details, medicines, logo, and signature**, and download a professional-looking PDF prescription.

---

## 📝 Features

- Add doctor and clinic details.
- Input patient information.
- Add multiple medicines with dosage and instructions.
- Upload logo and signature images.
- Generate PDF prescriptions ready for download.
- User-friendly **Streamlit interface**.

---

## ⚙️ Technologies Used

- **Python 3.x**
- **Streamlit** - for web interface
- **Pillow (PIL)** - for image processing
- **BytesIO** - for handling in-memory files

---

## 🚀 Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/FakePrescriptionGenerator.git
cd FakePrescriptionGenerator 

2. Create a virtual environment (optional but recommended)

   -python -m venv venv
   -source venv/bin/activate   # For Linux/Mac
   -venv\Scripts\activate      # For Windows


3. Install dependencies

   -pip install -r requirements.txt


4. Run the app

   -streamlit run app.py

🖼️ Screenshots

https://github.com/sarkrarjun-wq/FakePrescriptionGenerator/blob/f9afd778bb99f3d79b0e81b54e162644baafd9db/Screenshot%202025-09-10%20180348.png

https://github.com/sarkrarjun-wq/FakePrescriptionGenerator/blob/73ccc2f324125b10a19611635828d2ca471c2a5d/Screenshot%202025-09-10%20180359.png


📁 Project Structure
FakePrescriptionGenerator/
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── README.md
├── assets/              # Folder for logos, signatures, etc.
└── modules/             # Optional: separate Python modules

💡 Usage

1.open the app in your browser.

2.Fill in doctor and patient details.

3.Upload logo and signature if needed.

4.Add medicines and instructions.

5.Click Generate PDF to download the prescription.

⚖️ Disclaimer

This project is for educational purposes only. Do not use it for creating real prescriptions.

📄 License

This project is licensed under the MIT License - see the LICENSE
 file for details.
