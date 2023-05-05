import React, { useState } from "react"; //Source #4
import ChatMessage from "./chatmessage";
import "./chatdisplay.css";

const ChatDisplay = ({ messages }) => {
  const firstSender = messages.length > 0 ? messages[0][0] : null;

  return (
    <div className="chatwindow">
      <ul className="styled-list">
        {messages.map(function (item) {
          // console.log("This is item");
          // console.log(item);
          return (
            <li
              className={
                item[0] != firstSender
                  ? "left-sender-list-item"
                  : "right-sender-list-item"
              }
            >
              <ChatMessage
                message={item[1]}
                sender={item[0] == firstSender ? "left-sender" : "right-sender"}
                id = {item[2]}
              />
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default ChatDisplay;
