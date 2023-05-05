import React, { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Checkbox,
  TableSortLabel,
  Button,
  Grid,
} from "@mui/material";
// import ReportIcon from "@mui/icons-material/Report"; //Top threshold
// import PriorityHighIcon from "@mui/icons-material/PriorityHigh";
// import ShieldIcon from "@mui/icons-material/Shield";
// import VerifiedUserIcon from "@mui/icons-material/VerifiedUser";

const AnalysisResultsTable = (props) => {
  const [sortDirection, setSortDirection] = useState("asc");
  const [sortedBy, setSortedBy] = useState(null);

  const handleSort = (property) => {
    const isAsc = sortedBy === property && sortDirection === "asc";
    setSortDirection(isAsc ? "desc" : "asc");
    setSortedBy(property);
  };

  const sortedFiles = props.uploadedFiles.sort((a, b) => {
    if (sortDirection === "asc") {
      return a[sortedBy] > b[sortedBy] ? 1 : -1;
    } else {
      return a[sortedBy] < b[sortedBy] ? 1 : -1;
    }
  });

  return (
    <Paper style={{ display: "inline-block" }} elevation={3}>
      {props.uploadedFiles.length > 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>
                  <TableSortLabel
                    active={sortedBy === "name"}
                    direction={sortDirection}
                    onClick={() => handleSort("name")}
                  >
                    File Name
                  </TableSortLabel>
                </TableCell>
                <TableCell>
                  <TableSortLabel
                    active={sortedBy === "percentage"}
                    direction={sortDirection}
                    onClick={() => handleSort("percentage")}
                  >
                    Risk Percentage
                  </TableSortLabel>
                </TableCell>
                <TableCell>
                  <Button variant="contained" onClick={() => props.setAnalysisViewState("overview")}>Collapse Table</Button>
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sortedFiles.map((file) => (
                <TableRow key={file.name}>
                  <TableCell>{file.name}</TableCell>
                  <TableCell>{file.percentage}</TableCell>
                  <TableCell>{props.getRiskIcon(file.percentage)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Paper>
  );
};

export default AnalysisResultsTable;
