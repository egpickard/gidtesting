import React, { useState } from "react";
import "./aboutus.css";
import erica from "./erica.jpg";
import emerson from "./emerson.jpeg";
import aidan from "./aidan.jpeg";
import jeevitha from "./jeevitha.png";

const images = [
  {
    id: 1,
    src: erica,
    alt: "Image 1",
    name: "Erica Pickard",
    description:
      "Erica is a senior at UMass, graduating in May 2023 with a BS in computer science with a focus on cybersecurity. She is part of the research, UI, and frontend teams.",
  },
  {
    id: 2,
    src: emerson,
    alt: "Image 2",
    name: "Emerson Kiefer",
    description:
      "Emerson is a UMass senior who will pursue his Master's in Computer Science at UMass next year with a focus on artificial intelligence. He is a member of GID's research, UI, and frontend team, contributing to the design and development of the website.",
  },
  {
    id: 3,
    src: aidan,
    alt: "Image 3",
    name: "Aidan Nuzum-Clark",
    description:
      "Aidan is a masters student at UMass studying computer science with a focus on artificial intelligence, graduating in May 2023. He is a member if the backend and research teams",
  },
  {
    id: 4,
    src: jeevitha,
    alt: "Image 4",
    name: "Jeevitha Patel",
    description:
      "Jeevitha is a master's student at UMass studying computer science (graduating May 2024) with a bachelor's degree in Mechanical Engineering. She is a part of the research and backend teams.",
  },
];

function AboutUs() {
  const [activeImage, setActiveImage] = useState(null);

  return (
    <>
      <h1 className="team-header">Meet the Team!</h1>
      <div className="about-container">
        {images.map((image) => (
          <div
            key={image.id}
            className={`about-item ${image.id === activeImage ? "active" : ""}`}
            onClick={() => setActiveImage(image.id)}
          >
            <img src={image.src} alt={image.alt} />
            <div className="about-text">
              <h2>{image.name}</h2>
              <p className="about-description">{image.description}</p>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

export default AboutUs;
