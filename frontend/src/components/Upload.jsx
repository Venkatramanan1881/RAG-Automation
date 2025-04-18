import React from 'react';
import './Upload.css';
import uploadIcon from '../assets/upload.svg';

const Upload = () => {
  return (
    
      <label htmlFor="file-upload" className="upload-area">
        <img src={uploadIcon} alt="Upload Icon" className="upload-icon" />
        Click to upload or <i>drag and drop</i> <br />
        PNG, JPG, PDF, DOCX, TXT
        <input id="file-upload" type="file" style={{ display: 'none' }} />
      </label>
    
  );
};

export default Upload;
