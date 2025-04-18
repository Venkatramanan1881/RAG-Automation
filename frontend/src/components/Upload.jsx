import React from 'react';
import './Upload.css';
import uploadIcon from '../assets/upload.svg';

const Upload = () => {
  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif'];
    const allowedExtensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif'];
    const fileExtension = file.name.slice((file.name.lastIndexOf('.') - 1 >>> 0) + 2).toLowerCase();

    if (!allowedTypes.includes(file.type) || !allowedExtensions.includes(`.${fileExtension}`)) {
      alert('Invalid file type. Only PDF, JPG, PNG, and GIF allowed.');
      return;
    }

    const uploadDir = file.type === 'application/pdf' ? 'files/pdf' : 'files/images';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_dir', uploadDir);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      if (res.ok) {
        alert(`✅ ${data.message}`);
      } else {
        alert(`❌ Upload failed: ${data.error || 'Upload error occurred'}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert(`❌ Upload error occurred: ${error.message}`);
    }
  };

  return (
    <label htmlFor="file-upload" className="upload-area">
      <img src={uploadIcon} alt="Upload Icon" className="upload-icon" />
      Click to upload or <i>drag and drop</i><br />
      PNG, JPG, PDF, DOCX, TXT
      <input
        id="file-upload"
        type="file"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </label>
  );
};

export default Upload;
