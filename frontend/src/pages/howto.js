import React from "react";
import "./HowToPage.css"; // Import CSS for styling
import step1 from "./step1.jpg";
import step2 from "./step2.png";
import step3 from "./step3.jpg";
import imessage from "./imessage.png";
import messenger from "./messenger.png";
import whatsapp from "./whatsapp.png";
import discord from "./discord.png";
import { Link } from "react-router-dom";

const HowToPage = () => {
  return (
    <div className="how-to-page">
      <h1 className="how-to-title">Welcome to GID!</h1>
      <p className="how-to-description">
        Here's a step-by-step guide on how to use our website:
      </p>
      <div className="step-container">
        <div className="step">
          <img src={step1} alt="Step 1" className="step-image" />
          <h2 className="step-title">Step 1</h2>
          <p className="step-description">
            Download your data into an acceptable format. Below are instructions
            on how to do so.
          </p>
        </div>
        <div className="step">
          <img src={step2} alt="Step 2" className="step-image" />
          <h2 className="step-title">Step 2</h2>
          <p className="step-description">
            Drap and Drop in the space marked by slash-marks or click the chose
            file on the "File(s) Analysis" page. Or you can chose "Live Analysis" to import one file and see grooming detection based on each line.
          </p>
        </div>
        <div className="step">
          <img src={step3} alt="Step 3" className="step-image" />
          <h2 className="step-title">Step 3</h2>
          <p className="step-description">
            Press "Analyze Text" and view your results. For any questions,
            please feel free to contact us!
          </p>
        </div>
      </div>
      <div className="how-to-description">
        <h2 className="step-title">How to download your messages:</h2>
        <img src={messenger} alt={messenger} className="step-image" />
        <p>
          <a
            href="https://www.remote.tools/remote-work/download-facebook-messenger-conversation"
            className="my-link"
          >
            Click here for instructions to download Facebook Messenger messages (ensure you choose json instead of html)
          </a>{" "}
        </p>
        <img src={whatsapp} alt={whatsapp} className="step-image" />
        <p>
          <a
            href="https://faq.whatsapp.com/1180414079177245/?cms_platform=android"
            className="my-link"
          >
            Click here for instructions to download WhatsApp messages (ensure
            you choose no media)
          </a>{" "}
        </p>
        <img src={discord} alt={discord} className="step-image" />
        <p>
          <a
            href="https://www.groovypost.com/howto/export-discord-chat-messages/"
            className="my-link"
          >
            Click here for instructions to download Discord messages
          </a>{" "}
        </p>
      </div>
      <div className="cta-container">
        <h2 className="cta-title">Ready to Get Started?</h2>
        <p className="cta-description">
          Click here to begin analyzing your file(s)!
        </p>

        <Link to="/begin">
          <button className="cta-button">Begin</button>
        </Link>
      </div>
    </div>
  );
};

export default HowToPage;
