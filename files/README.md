# 🖼️ Advanced Image Restoration WebApp
# Hệ thống lọc và khôi phục ảnh nâng cao

A comprehensive web application for image filtering and restoration using advanced spatial and frequency domain filters.

## ✨ Features

### 🔧 Supported Filters
- **Bilateral Filter** - Edge-preserving smoothing
- **Non-Local Means (NLM)** - Advanced denoising using image self-similarity
- **Wiener Filter** - Optimal frequency domain filtering
- **Optimum Notch Filter** - Removes periodic/sinusoidal noise

### 📊 Noise Types Support
- **Gaussian Noise** - Random noise with normal distribution
- **Salt & Pepper Noise** - Impulse noise
- **Periodic Noise** - Sinusoidal/cyclic interference

### 🎯 Core Capabilities
- Upload images in multiple formats (PNG, JPG, JPEG, GIF, BMP)
- Add synthetic noise for testing
- Apply filters for noise removal and restoration
- Real-time before/after preview
- Batch processing support

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Flask server**
```bash
python app.py
```

The server will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm start
```

The app will open at `http://localhost:3000`

## 📁 Project Structure

```
image-restoration-webapp/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── image_filters.py       # Filter implementations
│   ├── noise_handling.py      # Noise generation & removal
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # Uploaded images directory
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Main React component
│   │   ├── App.css           # Styling
│   │   └── index.tsx         # Entry point
│   ├── package.json          # Node dependencies
│   └── public/               # Static assets
└── README.md                 # This file
```

## 🔌 API Endpoints

### Upload Image
```http
POST /api/upload
Content-Type: multipart/form-data

file: <image_file>
```

**Response:**
```json
{
  "success": true,
  "filename": "image.jpg",
  "filepath": "uploads/image.jpg"
}
```

### Add Noise
```http
POST /api/add-noise
Content-Type: application/json

{
  "filepath": "uploads/image.jpg",
  "noise_type": "gaussian",
  "intensity": 0.1
}
```

### Apply Filter
```http
POST /api/filter
Content-Type: application/json

{
  "filepath": "uploads/image.jpg",
  "filter": "bilateral"
}
```

### Health Check
```http
GET /api/health
```

## 🎨 Filter Parameters

### Bilateral Filter
- `d`: Diameter of pixel neighborhood (default: 9)
- `sigma_color`: Color space sigma (default: 75)
- `sigma_space`: Coordinate space sigma (default: 75)

### Non-Local Means (NLM)
- `h`: Filter strength (default: 10)
- `patch_size`: Patch size (default: 5)
- `patch_distance`: Search distance (default: 7)

### Wiener Filter
- `noise_variance`: Estimated noise variance (auto-estimated)

### Notch Filter
- `center_x`: Frequency domain X center
- `center_y`: Frequency domain Y center
- `radius`: Notch radius (default: 10)

## 📊 Supported Image Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)

## 🔒 Security Features
- File size limit: 10MB
- Allowed file types validation
- Secure filename handling
- CORS enabled for cross-origin requests

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **OpenCV** - Image processing
- **NumPy/SciPy** - Numerical computations
- **scikit-image** - Advanced image algorithms

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Axios** - HTTP client
- **CSS3** - Styling

## 📝 Usage Examples

### Example 1: Remove Gaussian Noise with Bilateral Filter
1. Upload an image
2. Select "Add Noise" → Choose "Gaussian Noise" → Set intensity
3. Click "Add Noise"
4. Select "Bilateral Filter" from dropdown
5. Click "Apply Filter"

### Example 2: Remove Periodic Noise with Notch Filter
1. Upload an image
2. Select "Add Noise" → Choose "Periodic Noise"
3. Click "Add Noise"
4. Select "Optimum Notch Filter"
5. Click "Apply Filter"

## 🚧 Future Enhancements
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Batch image processing
- [ ] Filter parameter tuning UI
- [ ] History/undo functionality
- [ ] Download processed images
- [ ] Compare multiple filters side-by-side
- [ ] Real-time preview with adjustable parameters
- [ ] Advanced image quality metrics
- [ ] GPU acceleration support

## 📄 License
MIT License

## 👨‍💻 Author
Created for advanced image processing applications

## 🤝 Contributing
Contributions are welcome! Please feel free to submit PRs or open issues.