import axios from "axios";
import React, { useRef, useState } from "react";
import { Document, Page } from "react-pdf";
import { pdfjs } from "react-pdf";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFileUpload } from "@fortawesome/free-solid-svg-icons";
import fetcher from "./http/RequestConfig";

// Import the required CSS for TextLayer and AnnotationLayer
import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import "react-pdf/dist/esm/Page/TextLayer.css";

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function PDFUploader({ chat_id, handleForceUpdate = () => {} }) {
  const [files, setFiles] = useState([]);
  const [numPages, setNumPages] = useState({});
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef();

  const onDocumentLoadSuccess = (fileIndex, { numPages }) => {
    setNumPages((prevNumPages) => ({
      ...prevNumPages,
      [fileIndex]: numPages,
    }));
  };

  const splashScreenStyle = {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(0, 0, 0, 0.7)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontSize: "1.5rem",
    color: "white",
    zIndex: 1000,
  };

  const uploadFile = async (e) => {
    const selectedFiles = e.target.files;
    setFiles(selectedFiles);

    // Example: Validate file size (5MB limit)
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    for (let i = 0; i < selectedFiles.length; i++) {
      if (selectedFiles[i].size > maxSize) {
        alert("File is too large. Please upload a file smaller than 5MB.");
        return;
      }
    }
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append("file", selectedFiles[i]);
    }

    formData.append("chat_id", chat_id);

    setIsUploading(true);

    try {
      const response = await fetcher("upload/upload-file", {
        method: 'POST',
        body: formData,
        credentials: 'include' // Make sure credentials are included in the request
      });

      if (!response.ok) {
        throw new Error("Failed to upload files.");
      }

      const response_str = await response.json();
      console.log("Upload successful:", response_str);

      // // Process the response and pass the file content to the chatbot for querying.
      // const processedText = response_str.processedText || '';  // Assuming the server returns processed text or file reference.
      // handleFileUploaded(processedText);  // Pass this to the chatbot

      setIsUploading(false);
      // handleForceUpdate();
      // Call the handleForceUpdate function if it's provided
      if (typeof handleForceUpdate === "function") {
        handleForceUpdate();
      } else {
        console.warn("handleForceUpdate is not a valid function.");
      }
    } catch (error) {
      console.error("Error during file upload:", error);
      alert("Error uploading files. Please try again.");
      setIsUploading(false);
    }
  };

  const handleUploadBtnClick = () => {
    fileInputRef.current.click();
  };

  // const handleFileUploaded = (processedText) => {
  //   // Assuming the server returns processed text or metadata
  //   setMessages((prevMessages) => [
  //     ...prevMessages,
  //     {
  //       message: `File uploaded and processed. You can now ask questions about the content.`,
  //       direction: "incoming",
  //     },
  //   ]);
  
  //   // Store the processed file content for later use in querying
  //   setMessages((prevMessages) => [
  //     ...prevMessages,
  //     {
  //       message: `Processed text: ${processedText}`,  // Display the text for now, or store it for queries
  //       direction: "incoming",
  //     },
  //   ]);
  // };
  

  return (
    <div>
      {isUploading && (
        <div style={splashScreenStyle}>Processing Document...</div>
      )}
      <input
        type="file"
        style={{ display: "none" }}
        ref={fileInputRef}
        onChange={uploadFile}
        accept=".pdf, .docx, .doc, .txt, .csv, .jpg, .jpeg, .png,  .mp4, .avi, .mov, .wav, .mp3, .m4a"
        multiple // Allow multiple file selection
      />
      <div className="">
        <FontAwesomeIcon
          icon={faFileUpload}
          onClick={handleUploadBtnClick}
          className="px-2"
        />
      </div>
      <div>
        {files.length > 0 && (
          <div>
            {Array.from(files).map((singleFile, fileIndex) => (
              <Document
                key={`file_${fileIndex}`}
                file={singleFile}
                onLoadSuccess={(pdf) => onDocumentLoadSuccess(fileIndex, pdf)}
              >
                {Array.from(
                  new Array(numPages[fileIndex] || 0),
                  (el, pageIndex) => (
                    <Page
                      key={`page_${fileIndex}_${pageIndex + 1}`}
                      pageNumber={pageIndex + 1}
                    />
                  )
                )}
              </Document>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default PDFUploader;