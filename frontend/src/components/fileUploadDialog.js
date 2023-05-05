import React, { useState } from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";

export default function FileUploadField(props) {
    const [open, setOpen] = useState(false);

    const handleOpen = () => {
        setOpen(true)
    }

    const handleClose = () => {
        setOpen(false)
    }

    const listFiles = () => {
        return Array.from(props.files).map((file, index) => (
          <li key={index}>{file.name}</li>
        ));
    };

    return (
        <div>
            <Button style={{maxWidth: '30px', maxHeight: '30px', minWidth: '100px', minHeight: '100px'}} variant="contained" onClick={handleOpen}>
                {props.files.length} files uploaded
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Uploaded Files</DialogTitle>
                <DialogContent>
                    {props.files.length > 0 && <ul>{listFiles()}</ul>}
                </DialogContent>
            </Dialog>
        </div>
    )

}