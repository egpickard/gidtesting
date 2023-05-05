import React, { useState } from "react";
import Button from "@mui/material/Button";
// import Paper from "@mui/material/Paper";

export default function FileUploadField(props) {
  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    // props.setFiles(event.dataTransfer.files);
    const fileList = event.dataTransfer.files;
    handleFileChange(fileList)
  };

  const handleFileSelect = (event) => {
    const fileList = event.target.files;
    handleFileChange(fileList)
  };

  function handleFileChange(fileList) {
    const fileArray = [];

    for (let i = 0; i < fileList.length; i++) {
      fileArray.push(fileList[i]);
    }

    props.setFiles(fileArray);
  }

  // const listFiles = () => {
  //   return Array.from(props.files).map((file, index) => (
  //     <li key={index}>{file.name}</li>
  //   ));
  // };

  return (
    <div
      style={{
        border: "2px dashed white",
        display: "inline-block",
        padding: "10px"
      }}
    >
      {/* <Paper elevation={2} variant="elevation"> */}
      <div onDragOver={handleDragOver} onDrop={handleDrop}>
        <header>
          <input
            id="file-upload"
            multiple
            type="file"
            onChange={handleFileSelect}
            hidden
          />
          <label htmlFor="file-upload">
            <Button variant="contained" component="span">
              Upload File(s)
            </Button>
          </label>

          <p>Or drag and drop a file here</p>
          {/* {files && <p>Selected file: {files}</p>} */}
          {/* {props.files.length > 0 && <ul>Files: {listFiles()}</ul>} */}
        </header>
      </div>
    </div>
  );
}
