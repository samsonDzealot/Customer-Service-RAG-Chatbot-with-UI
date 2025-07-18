import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageCircle, Utensils, Clock, Users } from 'lucide-react';
import './index.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Welcome to Orisirisi Restaurant! I'm here to help you with menu items, operating hours, staff information, and restaurant policies. What would you like to know?",
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputMessage })
      });
      
      const data = await response.json();
      const botResponse = {
        id: messages.length + 2,
        text: data.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      };
      
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error('Error:', error);
      const errorResponse = {
        id: messages.length + 2,
        text: "Sorry, I'm having trouble connecting to the server. Please make sure the chatbot API is running.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      };
      setMessages(prev => [...prev, errorResponse]);
    }
    setIsLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const quickQuestions = [
    { icon: Clock, text: "What are your operating hours?" },
    { icon: Utensils, text: "Show me the menu" },
    { icon: Users, text: "Who are the staff members?" }
  ];

  const handleQuickQuestion = (question) => {
    setInputMessage(question);
  };

  return (
    <div className="container">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-icon">
          <Utensils />
        </div>
        <div>
          <h1>Orisirisi Restaurant</h1>
          <p>Ask me anything about our menu, hours, and services</p>
        </div>
      </div>

      {/* Chat Container */}
      <div className="chat-container">
        {/* Messages Area */}
        <div className="messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${
                message.sender === 'user' ? 'user-message' : 
                message.id === 1 ? 'welcome-message' : 'bot-message'
              }`}
            >
              <div>{message.text}</div>
              <div className="timestamp">{message.timestamp}</div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message bot-message loading">
              Thinking
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Questions */}
        <div className="quick-questions">
          <h4>Quick questions:</h4>
          <div className="quick-buttons">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleQuickQuestion(question.text)}
                className="quick-button"
              >
                <question.icon style={{ width: '16px', height: '16px', marginRight: '8px' }} />
                {question.text}
              </button>
            ))}
          </div>
        </div>

        {/* Input Area */}
        <div className="input-container">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about our menu, hours, or services..."
            className="message-input"
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="send-button"
          >
            <Send style={{ width: '20px', height: '20px' }} />
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="footer">
        <p>Powered by AI • Orisirisi Restaurant Assistant</p>
      </div>
    </div>
  );
}

export default App;