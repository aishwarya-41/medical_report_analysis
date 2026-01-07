import React from "react";

const UploadButton = ({ enabled, onClick, loading }) => {
  return (
    <button
      className={`upload-btn ${enabled ? "active" : "disabled"}`}
      disabled={!enabled || loading}
      onClick={onClick}
    >
      {loading ? "Uploading..." : "Analyze Report"}
    </button>
  );
};

export default UploadButton;
