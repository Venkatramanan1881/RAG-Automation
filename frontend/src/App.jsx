import React, { useState } from 'react';
import ChatBox from './components/ChatBox';
import Upload from './components/Upload';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');

  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };

  return (
    <>
      <div className="blob blob1"></div>
      <div className="blob blob2"></div>
      <div className="blob blob3"></div>
      <div className="sidebar">
        <button
          className={`sidebar-button ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => handleTabClick('chat')}
        >
          Chat
        </button>
        <button
          className={`sidebar-button ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => handleTabClick('upload')}
        >
          Upload
        </button>
      </div>
      
        {activeTab === 'chat' ? <ChatBox /> : <Upload />}
      
    </>
  );
}

export default App
