import React, { useState, useRef, useEffect } from 'react';
// import ChatBubble from '../components/ChatBubble';
import UploadSection from '../upload/UploadSection.jsx';
import ChatBubble from '../chatbubble/ChatBubble';
const Chat = () => {
  const [messages, setMessages] = useState([

    { role: 'assistant', content: 'Hi! I\'m HeaLLMe, your AI health assistant. What symptoms are you experiencing today?' },
  ]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    
    const newMessages = [
      ...messages,
      { role: 'user', content: input },
      { role: 'assistant', content: 'Thanks! Based on that, I need to ask a few more questions.' } // Placeholder
    ];
    setMessages(newMessages);
    setInput('');
  };

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Header */}
      <header className="bg-blue-600 text-white text-center py-4 text-2xl font-bold shadow-md">
        HeaLLMe.ai Chat
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, index) => (
          <ChatBubble key={index} role={msg.role} text={msg.content} />
        ))}
        <div ref={chatEndRef}></div>
      </main>

      {/* Input Box */}
      <footer className="p-4 bg-gray-100 flex gap-2 shadow-inner">
        <UploadSection/>
        <input
          type="text"
          placeholder="Type your symptoms..."
          className="flex-1 p-3 border rounded-lg focus:outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
        >
          Send
        </button>
      </footer>
    </div>
  );
};

export default Chat;
