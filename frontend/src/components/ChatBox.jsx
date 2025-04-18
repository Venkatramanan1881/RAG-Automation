import React, { useState, useEffect, useRef } from 'react';
import './ChatBox.css';
import uploadSvg from '../assets/upload.svg';
import sendBtnSvg from '../assets/send-btn.svg';
import audioBtnSvg from '../assets/audio-btn.svg';

function ChatBox() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const chatHistoryRef = useRef(null);

  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleSendMessage = async () => {
    setMessage('');
    if (message.trim() === '') return;

    const userMessage = { sender: 'user', text: message };
    setChatHistory(prev => [...prev, userMessage]);

    try {
      const response = await fetch('http://localhost:8000/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
      });
      console.log("Response:", response);
      const data = await response.json();
      console.log("Response from server:", data);

      if (data.response) {
        const aiMessage = { sender: 'ai', text: data.response };
        setChatHistory(prev => [...prev, aiMessage]);
      } else {
        setChatHistory(prev => [...prev, { sender: 'ai', text: "No response received." }]);
      }
    } catch (error) {
      console.error("Error:", error);
      setChatHistory(prev => [...prev, { sender: 'ai', text: "Error: Could not send message." }]);
    }

    setMessage('');
  };

  const handleInputChange = (event) => {
    setMessage(event.target.value);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chatbox-container">
      <div className="chatbox-history" ref={chatHistoryRef}>
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message-wrapper ${msg.sender}`}>
            <div className="message-bubble">{msg.text}</div>
          </div>
        ))}
      </div>
      <div className="chatbox-input-area">
        
        <input
          type="text"
          value={message}
          onChange={handleInputChange}
          onKeyDown={handleKeyPress}
          placeholder="Message..."
          className="chatbox-input"
        />
        {message.trim() === '' ? (
          <img src={audioBtnSvg} alt="Audio" className="audio-button" />
        ) : (
          <img src={sendBtnSvg} alt="Send" className="send-button" onClick={handleSendMessage}/>
        )}
      </div>
    </div>
  );
}

export default ChatBox;
