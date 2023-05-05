import React, { useState } from "react"; //Source #4
import "./chatmessage.css";
const ChatMessage = ({ message, sender, id }) => {
  return (
    <div className={"box " + "_"+id} >
      <p>{message}</p>
    </div>
  );
};

export default ChatMessage;
