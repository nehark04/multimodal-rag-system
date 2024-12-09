import React, { useState, useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFileUpload } from "@fortawesome/free-solid-svg-icons";
import fetcher from "./http/RequestConfig";

const FileUploader = ({ onUploadSuccess }) => {
  const fileInputRef = useRef();
  const [isUploading, setIsUploading] = useState(false);

  const uploadFile = async (e) => {
    const files = e.target.files;
    const formData = new FormData();
    Array.from(files).forEach((file) => formData.append("file", file));

    setIsUploading(true);
    try {
      const response = await fetcher("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to upload files.");

      onUploadSuccess();
    } catch (error) {
      alert("Error uploading files. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        ref={fileInputRef}
        onChange={uploadFile}
        style={{ display: "none" }}
      />
      <button onClick={() => fileInputRef.current.click()} disabled={isUploading}>
        <FontAwesomeIcon icon={faFileUpload} /> Upload File
      </button>
    </div>
  );
};

export default FileUploader;