// import React from "react";
import React, { useState } from "react"; //Source #4
import Button from "@mui/material/Button";

const AnalysisButton = (props) => {
  async function handleSubmit(event) {
    event.preventDefault();
    props.setLoading(true);

    const formData = new FormData();

    for (let i = 0; i < props.files.length; i++) {
      formData.append("files", props.files[i]);
    }
    const response = await fetch("http://127.0.0.1:8080/api/online_upload", {
      method: "POST",
      body: formData,
    });

    // handle the server response
    if (response.ok) {
      const data = await response.json();
      props.setUploadedFiles(data.files);
    } else {
      console.error(response.statusText);
    }
    props.setLoading(false);
    props.resetMessages();
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {/* <input type="file" multiple onChange={handleFileChange} /> */}
        <Button type="submit" variant="contained">
          Run Analysis
        </Button>
      </form>
    </div>
  );
};

export default AnalysisButton;
