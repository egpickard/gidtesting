import logo from "./logo.png";
import "./App.css";
import React, { useState } from "react"; //Source #4
import FileUploadField from "../components/fileUploadField";
import AnalysisButton from "../components/analysisButton";
import AnalysisResultsTable from "../components/analysisResultsTable";
import FileUploadDialog from "../components/fileUploadDialog";
import AnalysisOverview from "../components/analysisOverview";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';


import ReportIcon from "@mui/icons-material/Report"; //Top threshold
import PriorityHighIcon from "@mui/icons-material/PriorityHigh";
import ShieldIcon from "@mui/icons-material/Shield";
import VerifiedUserIcon from "@mui/icons-material/VerifiedUser";

const Home = () => {
  const [files, setFiles] = useState([]);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [analysisState, setAnalysisState] = useState("idle"); //states are "idle", "loading", "failed"
  const [analysisViewState, setAnalysisViewState] = useState("hidden"); //states are "hidden", "overview", and "table"

  const riskIconDict = {
    "4":<ReportIcon fontSize="large" style={{ color: "red" }} />,
    "3":<ReportIcon fontSize="large" style={{ color: "red" }} />,
    "2":<PriorityHighIcon fontSize="large" style={{ color: "orange" }} />,
    "1":<ShieldIcon fontSize="large" style={{ color: "gold" }} />,
    "0":<VerifiedUserIcon fontSize="large" style={{ color: "green" }} />
  }

  const getRiskIcon = (percentage) => {
    return riskIconDict[(Math.floor(percentage*100/25)).toString()]
  }

  return (
    <div className="App">
      <div className="logo-container">
        <img src={logo} className="App-logo" alt="logo" />
        <logo-container>
          <header>
            <p>Please upload a file to begin</p>
            <FileUploadField
              files={files}
              setFiles={setFiles}
              className="file-upload"
            />
          </header>
        </logo-container>
        <FileUploadDialog files={files}/>
        <AnalysisButton files={files} uploadedFiles={uploadedFiles} setUploadedFiles={setUploadedFiles} setAnalysisViewState={setAnalysisViewState} setAnalysisState={setAnalysisState}/>
        {analysisState == "loading" && <Box sx={{ display: 'flex' }}>
          <CircularProgress />
        </Box>}
        {analysisViewState=="overview" && uploadedFiles.length > 0 && <AnalysisOverview uploadedFiles={uploadedFiles} getRiskIcon={getRiskIcon} setAnalysisViewState={setAnalysisViewState} setAnalysisState={setAnalysisState}/>}
        {analysisViewState=="table" && uploadedFiles.length > 0 && <AnalysisResultsTable uploadedFiles={uploadedFiles}  getRiskIcon={getRiskIcon} setAnalysisViewState={setAnalysisViewState} setAnalysisState={setAnalysisState}/>}

      </div>
    </div>
  );
};

export default Home;
