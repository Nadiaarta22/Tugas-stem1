# 🌊 STEM Design Lab - Pengasaman Laut & Konservasi

Platform pembelajaran interaktif untuk memahami pengasaman laut dan mengembangkan solusi konservasi melalui pendekatan **Design Thinking** dan **Machine Learning**.

## 📌 Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Instalasi](#instalasi)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Struktur Project](#struktur-project)
- [API Endpoints](#api-endpoints)
- [Panduan Penggunaan](#panduan-penggunaan)

## ✨ Fitur Utama

### 🎓 Design Thinking Process
1. **Empati** (`empathy.html`) - Memahami perspektif nelayan & komunitas pesisir
2. **Identifikasi Masalah** (`swot.html`) - Analisis SWOT terhadap pengasaman laut
3. **Ideasi** (`ideation.html`) - Brainstorming solusi inovatif
4. **Prototipe** (`prototype.html`) - Desain & dokumentasi rancangan solusi
5. **Pengujian** (`testing.html`) - Uji solusi dengan data real
6. **Refleksi** (`reflection.html`) - Evaluasi & iterasi pembelajaran

### 📊 Data & Analytics
- **Dashboard** (`dashboard.html`) - Visualisasi data real-time tentang kondisi pengasaman laut
- **AI Predictor** (`predict.html`) - Machine Learning untuk memprediksi risiko pengasaman laut
- **Model ML** - Random Forest untuk prediksi berbasis 4 parameter:
  - CO₂ Emissions (Emisi Karbon)
  - Nutrient Runoff (Limpasan Nutrisi)
  - Water Temperature (Suhu Air)
  - Industrial Waste (Limbah Industri)

## 🛠️ Teknologi yang Digunakan

### Frontend
- **HTML5** - Struktur halaman
- **Tailwind CSS** - Styling & responsive design
- **Chart.js** - Visualisasi data & grafik
- **Vanilla JavaScript** - Interaksi halaman

### Backend
- **Flask** - Web framework Python
- **Flask-CORS** - Cross-Origin Resource Sharing
- **Scikit-learn** - Machine Learning (Random Forest)
- **Pandas & NumPy** - Data processing
- **Joblib** - Model serialization

## 📋 Instalasi

### Prerequisite
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone Repository
```bash
git clone https://github.com/Nadiaarta22/Tugas-stem1.git
cd Tugas-stem1
```

### Step 2: Buat Virtual Environment (Optional tapi Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Packages yang akan diinstall:
- `flask` - Web framework
- `flask-cors` - Enable CORS
- `scikit-learn` - ML algorithms
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `joblib` - Model serialization

## 🚀 Menjalankan Aplikasi

### 1. Training Model (First Time Only)
```bash
python train_model.py
```
Ini akan menghasilkan:
- `model.joblib` - Trained model
- `model_info.json` - Model metadata & feature importances

### 2. Jalankan Backend Server
```bash
python app.py
```
Output:
```
 * Running on http://127.0.0.1:5000
```

### 3. Buka Frontend di Browser
- Buka file `index.html` di browser, atau
- Serve dengan local server (recommended):
  ```bash
  # Windows - Gunakan Live Server extension di VS Code
  # atau gunakan Python simple server di folder project:
  python -m http.server 8000
  ```
- Akses di `http://localhost:8000`

## 📁 Struktur Project

```
Tugas-stem1/
├── app.py                  # Flask backend server
├── train_model.py          # Script untuk train model ML
├── model.joblib            # Trained model (generated)
├── model_info.json         # Model metadata (generated)
│
├── index.html              # Landing page / Homepage
├── dashboard.html          # Data visualization dashboard
├── predict.html            # ML prediction interface
│
├── empathy.html            # Design Thinking: Empati
├── swot.html               # Design Thinking: SWOT Analysis
├── ideation.html           # Design Thinking: Ideasi
├── prototype.html          # Design Thinking: Prototipe
├── testing.html            # Design Thinking: Testing
├── reflection.html         # Design Thinking: Refleksi
│
├── style.css               # Custom CSS styles
├── requirements.txt        # Python dependencies
├── README.md               # Dokumentasi (file ini)
└── img/                    # Folder untuk images/assets
```

## 🔌 API Endpoints

### 1. Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Predict Risk
```
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "nutrient_runoff": 50,
  "co2_emissions": 600,
  "water_temp": 28,
  "industrial_waste": 40
}
```

**Response:**
```json
{
  "risk_probability": 62.45,
  "status": "Sedang (Medium)",
  "feature_importances": {
    "co2_emissions": 0.40,
    "nutrient_runoff": 0.25,
    "water_temp": 0.20,
    "industrial_waste": 0.15
  }
}
```

**Risk Levels:**
- 🟢 **Rendah (Low)**: < 35%
- 🟡 **Sedang (Medium)**: 35% - 70%
- 🔴 **Kritis (Critical)**: > 70%

## 📖 Panduan Penggunaan

### Untuk Siswa/Pengguna
1. **Mulai dari Homepage** - Baca overview tentang proyek
2. **Ikuti Design Thinking Flow** - Urutan: Empati → SWOT → Ideasi → Prototipe → Testing → Refleksi
3. **Gunakan Dashboard** - Lihat data real-time & trend
4. **Test dengan Predictor** - Input parameter & lihat prediksi risiko
5. **Dokumentasikan Pembelajaran** - Catat insights di setiap tahap

### Untuk Developer
1. **Modifikasi Model** - Edit `train_model.py` untuk algoritma berbeda
2. **Tambah Endpoints** - Extend `app.py` untuk API baru
3. **Customize Styling** - Update `style.css` & Tailwind config di HTML
4. **Add New Pages** - Buat HTML baru mengikuti template yang ada

## 🔧 Troubleshooting

### Model tidak loading
```
Error: Model atau informasi tidak ditemukan
Solution: Jalankan python train_model.py terlebih dahulu
```

### CORS Error di Browser
```
Error: Access to XMLHttpRequest blocked by CORS
Solution: Flask CORS sudah enabled, pastikan backend running di port 5000
```

### Port 5000 sudah digunakan
```bash
# Ubah port di app.py atau gunakan port berbeda:
app.run(host='127.0.0.1', port=5001, debug=True)
```

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn ML Models](https://scikit-learn.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Design Thinking Process](https://www.ideo.com/how-we-work)
- [Ocean Acidification Info](https://www.noaa.gov/education/resource-collections/ocean-coasts/ocean-acidification)

## 📝 License

Project ini dibuat untuk tujuan pembelajaran STEM. Bebas digunakan & dimodifikasi.

## 👥 Author

**Nadia Arta** - STEM Design Lab Project

---

**Last Updated:** Juli 2024

Untuk pertanyaan atau kontribusi, silakan buat issue atau pull request! 🚀