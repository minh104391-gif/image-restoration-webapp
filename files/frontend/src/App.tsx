import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

interface FilterState {
  selectedFile: File | null;
  uploadedFilepath: string | null;
  originalImage: string | null;
  filteredImage: string | null;
  selectedFilter: string;
  selectedNoise: string;
  noiseIntensity: number;
  isProcessing: boolean;
  message: string;
}

const App: React.FC = () => {
  const [state, setState] = useState<FilterState>({
    selectedFile: null,
    uploadedFilepath: null,
    originalImage: null,
    filteredImage: null,
    selectedFilter: 'bilateral',
    selectedNoise: 'gaussian',
    noiseIntensity: 0.1,
    isProcessing: false,
    message: '',
  });

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setState(prev => ({ ...prev, selectedFile: file }));
      
      // Preview original image
      const reader = new FileReader();
      reader.onload = (event) => {
        setState(prev => ({
          ...prev,
          originalImage: event.target?.result as string,
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!state.selectedFile) {
      setState(prev => ({ ...prev, message: 'Please select a file' }));
      return;
    }

    const formData = new FormData();
    formData.append('file', state.selectedFile);

    try {
      setState(prev => ({ ...prev, isProcessing: true, message: 'Uploading...' }));
      const response = await axios.post('http://localhost:5000/api/upload', formData);
      setState(prev => ({
        ...prev,
        uploadedFilepath: response.data.filepath,
        message: 'File uploaded successfully',
        isProcessing: false,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        message: 'Upload failed',
        isProcessing: false,
      }));
    }
  };

  const handleAddNoise = async () => {
    if (!state.uploadedFilepath) {
      setState(prev => ({ ...prev, message: 'Please upload an image first' }));
      return;
    }

    try {
      setState(prev => ({ ...prev, isProcessing: true, message: 'Adding noise...' }));
      const response = await axios.post('http://localhost:5000/api/add-noise', {
        filepath: state.uploadedFilepath,
        noise_type: state.selectedNoise,
        intensity: state.noiseIntensity,
      }, {
        responseType: 'blob',
      });

      const url = URL.createObjectURL(response.data);
      setState(prev => ({
        ...prev,
        filteredImage: url,
        message: 'Noise added successfully',
        isProcessing: false,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        message: 'Failed to add noise',
        isProcessing: false,
      }));
    }
  };

  const handleApplyFilter = async () => {
    if (!state.uploadedFilepath) {
      setState(prev => ({ ...prev, message: 'Please upload an image first' }));
      return;
    }

    try {
      setState(prev => ({ ...prev, isProcessing: true, message: 'Applying filter...' }));
      const response = await axios.post('http://localhost:5000/api/filter', {
        filepath: state.uploadedFilepath,
        filter: state.selectedFilter,
      }, {
        responseType: 'blob',
      });

      const url = URL.createObjectURL(response.data);
      setState(prev => ({
        ...prev,
        filteredImage: url,
        message: 'Filter applied successfully',
        isProcessing: false,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        message: 'Failed to apply filter',
        isProcessing: false,
      }));
    }
  };

  return (
    <div className="container">
      <h1>🖼️ Advanced Image Restoration System</h1>
      <p className="subtitle">Hệ thống lọc và khôi phục ảnh nâng cao</p>

      <div className="controls-section">
        <h2>📤 Upload Image</h2>
        <div className="file-input-group">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            disabled={state.isProcessing}
          />
          <button
            onClick={handleUpload}
            disabled={!state.selectedFile || state.isProcessing}
          >
            {state.isProcessing ? 'Processing...' : 'Upload'}
          </button>
        </div>

        <h2>🎨 Add Noise (Optional)</h2>
        <div className="filter-controls">
          <select
            value={state.selectedNoise}
            onChange={(e) => setState(prev => ({ ...prev, selectedNoise: e.target.value }))}
            disabled={state.isProcessing}
          >
            <option value="gaussian">Gaussian Noise</option>
            <option value="salt_pepper">Salt & Pepper Noise</option>
            <option value="periodic">Periodic Noise</option>
          </select>

          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={state.noiseIntensity}
            onChange={(e) => setState(prev => ({ ...prev, noiseIntensity: parseFloat(e.target.value) }))}
            disabled={state.isProcessing}
          />
          <span>Intensity: {state.noiseIntensity}</span>

          <button
            onClick={handleAddNoise}
            disabled={!state.uploadedFilepath || state.isProcessing}
          >
            {state.isProcessing ? 'Processing...' : 'Add Noise'}
          </button>
        </div>

        <h2>🔧 Apply Filter</h2>
        <div className="filter-controls">
          <select
            value={state.selectedFilter}
            onChange={(e) => setState(prev => ({ ...prev, selectedFilter: e.target.value }))}
            disabled={state.isProcessing}
          >
            <option value="bilateral">Bilateral Filter</option>
            <option value="nlm">Non-Local Means (NLM)</option>
            <option value="wiener">Wiener Filter</option>
            <option value="notch">Optimum Notch Filter</option>
          </select>

          <button
            onClick={handleApplyFilter}
            disabled={!state.uploadedFilepath || state.isProcessing}
          >
            {state.isProcessing ? 'Processing...' : 'Apply Filter'}
          </button>
        </div>

        {state.message && <p className="message">{state.message}</p>}
      </div>

      <div className="preview-section">
        <div className="preview-container">
          <h3>Original Image</h3>
          {state.originalImage ? (
            <img src={state.originalImage} alt="Original" className="preview-image" />
          ) : (
            <div className="placeholder">No image uploaded</div>
          )}
        </div>

        <div className="preview-container">
          <h3>Filtered Image</h3>
          {state.filteredImage ? (
            <img src={state.filteredImage} alt="Filtered" className="preview-image" />
          ) : (
            <div className="placeholder">Apply filter to see result</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;