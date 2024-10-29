import React, { useEffect, useState } from "react";
import './App.css';

// Single image URL (replace this with your actual image URL)
const imageUrl = "./img2.jpeg";

// Function to fetch and parse the text file
const fetchApiText = async () => {
  try {
    // Path to the text file
    const textFileUrl = '/personalized_weekly_plan.txt';  // Ensure the file is placed in the public folder

    // Perform the fetch request to load the text file
    const response = await fetch(textFileUrl);

    // Check if the response is successful
    if (!response.ok) {
      throw new Error('Failed to load the text file');
    }

    // Parse the text file content
    const text = await response.text();

    return text;  // Return the text content of the file
  } catch (error) {
    console.error('Error fetching the text file:', error);
    return 'Error fetching the text file';
  }
};

// Typing effect function
const useTypingEffect = (text, speed) => {
  const [displayedText, setDisplayedText] = useState("");
  const [isCursorVisible, setIsCursorVisible] = useState(true);

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      if (index < text.length) {
        setDisplayedText((prev) => prev + text.charAt(index));
        index++;
      } else {
        clearInterval(interval);
      }
    }, speed);

    const cursorInterval = setInterval(() => {
      setIsCursorVisible((prev) => !prev);
    }, 500); // Blinking cursor every 500ms

    return () => {
      clearInterval(interval);
      clearInterval(cursorInterval);
    };
  }, [text, speed]);

  return { displayedText, isCursorVisible };
};

function App() {
  const [apiText, setApiText] = useState("");
  const { displayedText, isCursorVisible } = useTypingEffect(apiText, 50); // Adjust speed as needed

  useEffect(() => {
    const fetchText = async () => {
      const text = await fetchApiText();
      setApiText(text);
    };

    fetchText();
  }, []);

  // Handle displayed text with line breaks
  const formattedText = displayedText.split('<br />').map((line, index) => (
    <span key={index}>
      {line}
      <br />
    </span>
  ));

  return (
    <div className="App">
      <header className="header">
        <img
          src="./logo4.png" // Replace with your logo URL
          alt="Logo"
          className="logo"
        />
      </header>

      <div className="main-container">
        <div className="image-section">
          <img src={imageUrl} alt="Your Content" className="image" />
        </div>
        <div className="text-section">
          <h2></h2>
          <p>
            {formattedText}
            {isCursorVisible && <span className="cursor">|</span>}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
