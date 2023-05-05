import React, { useState } from "react";
import Button from "@mui/material/Button";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";

// Title: Analysis Overview
/*  Highest level detected
    Total number of files 
    Number of files in each confidence range
    Disclaimer (Not )
*/

export default function AnalysisOverview(props) {
  var totalCount, criticalCount, highCount, moderateCount, lowCount;
  criticalCount = highCount = moderateCount = lowCount = 0;
  totalCount = props.uploadedFiles.length;

  props.uploadedFiles.forEach((file) => {
    if (typeof file.percentage != "number"){
      return;
    }
    if (file.percentage > 0.75) {
      criticalCount += 1
    } else if (file.percentage > 0.5) {
      highCount += 1
    } else if (file.percentage > 0.25) {
      moderateCount += 1
    } else if (file.percentage >= 0) {
      lowCount += 1
    }
  });

  const getHighestRisk = (files) => {
    if (files.length == 0){
      return 0;
    }
    return files.reduce((prev, curr) => (prev.percentage > curr.percentage) ? prev : curr).percentage;
  }



  return (
    <Paper style={{ display: "inline-block" }} elevation={3}>
      <Grid container justify="center" alignItems="center" spacing={2}>
        <Grid item xs={2}></Grid>
        <Grid item xs={8}>
          <Typography variant="h4">Analysis Overview</Typography>
        </Grid>
        <Grid item xs={2}>
          <Button variant="contained" onClick={() => props.setAnalysisViewState("table")}>Expand Table</Button>
        </Grid>
        <Grid item xs={12}>
          <Typography>{props.getRiskIcon(getHighestRisk(props.uploadedFiles))} Highest risk detected: {getHighestRisk(props.uploadedFiles)}</Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography>Total number of files: {totalCount}</Typography>
        </Grid>
        <Grid item xs={6}>
          {props.getRiskIcon(0.75)}
          <Typography>Critical: {criticalCount}</Typography>
        </Grid>
        <Grid item xs={6}>
          {props.getRiskIcon(0.5)}
          <Typography>High: {highCount}</Typography>
        </Grid>
        <Grid item xs={6}>
          {props.getRiskIcon(0.25)}
          <Typography>Moderate: {moderateCount}</Typography>
        </Grid>
        <Grid item xs={6}>
          {props.getRiskIcon(0)}
          <Typography>Low: {lowCount}</Typography>
        </Grid>
      </Grid>
    </Paper>
  );
}
