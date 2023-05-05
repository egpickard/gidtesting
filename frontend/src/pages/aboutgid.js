import React from "react";
import "./aboutgid.css";
import myPicture from "./umass.jpeg";

const AboutPage = () => {
  return (
    <div className="App">
      <div className="about-container">
        <img src={myPicture} alt="img" className="about-img" />
        <div className="about-text">
          <h1>About GID</h1>
          <p>
            GID (Grooming Identification) is a web application created with the
            goal of assisting with the early detection of child grooming in
            digital communications.{" "}
          </p>
          <p>
            GID uses a modified version of the{" "}
            <a href="https://github.com/danielafe7-usp/BF-PSR-Framework">
              BF-PSR Framework
            </a>
            , a state of the art grooming classification model.
          </p>
          <p>
            For more information about the creation and performance of the
            BF-PSR framework, read this{" "}
            <a href="https://www.sciencedirect.com/science/article/abs/pii/S0950705121011187">
              study.
            </a>{" "}
          </p>
          <p>
            This application was created at the University of Massachusetts
            Amherst for COMPSCI 596E- Machine Learning Applied to Child Rescue.{" "}
          </p>
        </div>
      </div>
    </div>
  );
};
export default AboutPage;
