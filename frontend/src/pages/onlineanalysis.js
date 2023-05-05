import logo from "./logo.png";
import "./App.css";
import "./onlineanalysis.css";
import React, { useState, useEffect } from "react"; //Source #4
import FileUploadField from "../components/fileUploadField";
import AnalysisButton from "./chatpages/analysisButton";
import FileUploadDialog from "../components/fileUploadDialog";
import ChatDisplay from "./chatpages/chatdisplay";
import BeatLoader from "react-spinners/BeatLoader";

const OnlineAnalysis = () => {
  const [files, setFiles] = useState([]);
  const [uploadedFiles, setUploadedFiles] = useState("none");
  const [messageIndex, setMessageIndex] = useState(0);
  const [messages, setMessages] = useState([]);
  const [predPercent, setPredPercent] = useState(0);
  const [loading, setLoading] = useState(false);

  const resetMessages = () => {
    setMessages([]);
    setMessageIndex(0);
    setPredPercent(0);
  };

  //   useEffect(() => {
  //     setMessages(["Hi bob", "hello Joe", "goodbye bob", "later joe"]);
  //   }, []);

  const addMessage = () => {
    if (uploadedFiles != "none") {
      let online_info = uploadedFiles[0]["online_pred"];
      if (messageIndex < online_info.length) {
        console.log(online_info[messageIndex]);
        const poster = online_info[messageIndex][0];
        const message = online_info[messageIndex][1];
        const percent = online_info[messageIndex][2];
        const poster_id = online_info[messageIndex][3];
        setMessages((prevState) => [...prevState, [poster, message, poster_id]]);
        setPredPercent(percent);
        setMessageIndex((prevstate) => prevstate + 1);
      }
    }
    // console.log(messages);
  };

  return (
    <div className="App">
      <div className="logo-container">
        <img src={logo} className="App-logo" alt="logo" />
        <logo-container>
          <header>
            <p>Please upload a file to begin for ~"online"~ analysis </p>
            <p>Then press 'analyze'. Once this is done, press 'next' to show each line of the file. The percentage will show how likely that grooming was detected in the previous lines. </p>
          </header>
        </logo-container>
        <div className="row">
          <FileUploadField
            files={files}
            setFiles={setFiles}
            className="file-upload"
          />
          <FileUploadDialog files={files} />
          <AnalysisButton
            files={files}
            uploadedFiles={uploadedFiles}
            setUploadedFiles={setUploadedFiles}
            setLoading={setLoading}
            resetMessages={resetMessages}
          />
          <div>{loading ? <BeatLoader color="red" /> : ""}</div>
        </div>

        <ChatDisplay messages={messages} />
        <div className="row">
          <button onClick={addMessage}>Next</button>
          <div className="row">
            <p>Percentage:</p>
            <p
              style={{
                color: (() => {
                  if (predPercent < 0.3) return "green";
                  else if (predPercent < 0.6) return "orange";
                  else return "red";
                })(),
              }}
            >
              {predPercent}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OnlineAnalysis;
