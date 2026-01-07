import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router";
import UploadButton from "./UploadButton";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const uploadedFile = e.target.files[0];

    if (uploadedFile && uploadedFile.type === "application/pdf") {
      setFile(uploadedFile);
    } else {
      alert("Please upload a PDF file only");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Save report_id for later use
      localStorage.setItem("report_id", response.data.report_id);

      // Navigate to report analysis page
      navigate("/report");
    } catch (err) {
      alert("Failed to upload report");
      setUploading(false);
    }
  };

  return (
    <div className="upload-page">
      {/* Upload Card */}
      <div className="upload-card">
        <h2>Upload Medical Report</h2>
        <p className="upload-subtext">
          Upload your medical report (PDF) to analyze and ask questions based on it.
        </p>

        <label className="upload-box">
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            hidden
          />
          <span>Click to upload or drag & drop</span>
          <small>PDF only • Max 10MB</small>
        </label>
      </div>

      {/* Uploaded File Preview */}
      {file && (
        <div className="file-preview">
          <div>
            <strong>{file.name}</strong>
            <p>{(file.size / 1024).toFixed(1)} KB</p>
          </div>
          <span className="status-badge">Ready to analyze</span>
        </div>
      )}

      {/* Action Button */}
      <UploadButton
        enabled={!!file && !uploading}
        onClick={handleUpload}
        loading={uploading}
      />
    </div>
  );
};

export default Upload;
