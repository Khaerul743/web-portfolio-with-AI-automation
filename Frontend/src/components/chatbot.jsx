import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { FaPaperPlane, FaRobot, FaTimes } from "react-icons/fa";
import { sendAgentMessage } from "../service/agent";

const Chatbot = () => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { sender: "ai", text: "Ask anything about me and my AI Agent will answer your question." }
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Daftar placeholder messages
  const placeholderMessages = [
    "Berapa umur lu?",
    "Lu belajar dimana?"
  ];

  useEffect(() => {
    if (open && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, open]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMsg = { sender: "user", text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await sendAgentMessage(userMsg.text);
      setMessages((msgs) => [
        ...msgs,
        { sender: "ai", text: res.response || "(No response)" }
      ]);
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { sender: "ai", text: "Error: gagal mendapatkan respon dari server." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Fungsi untuk mengirim placeholder message
  const handlePlaceholderClick = async (message) => {
    if (loading) return;
    const userMsg = { sender: "user", text: message };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput(""); // Clear input after sending
    setLoading(true);
    try {
      const res = await sendAgentMessage(userMsg.text);
      setMessages((msgs) => [
        ...msgs,
        { sender: "ai", text: res.response || "(No response)" }
      ]);
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { sender: "ai", text: "Error: gagal mendapatkan respon dari server." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <>
      {/* Floating Chatbot Button */}
      <motion.button
        className="fixed z-50 bottom-6 right-6 left-6 bg-chatbot-primary hover:bg-chatbot-primary-hover text-chatbot-text rounded-full shadow-2xl p-4 flex items-center justify-center transition-all duration-300"
        style={{ 
          boxShadow: "0 8px 32px rgba(0,0,0,0.4), 0 0 20px hsl(var(--chatbot-primary) / 0.3)" 
        }}
        onClick={() => setOpen(true)}
        aria-label="Open Chatbot"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
      >
        <FaRobot className="w-9 h-9" />
      </motion.button>

      {/* Modal Chat UI with animation */}
      <AnimatePresence>
      {open && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.8, y: 50 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: 50 }}
              transition={{ 
                type: "spring", 
                stiffness: 300, 
                damping: 25,
                duration: 0.4 
              }}
              className="w-full h-full sm:w-[90%] sm:h-[90%] md:max-w-lg md:max-h-[600px] bg-chatbot-bg rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-chatbot-border m-4"
              style={{
                boxShadow: "0 25px 50px -12px rgba(0,0,0,0.8), 0 0 30px hsl(var(--chatbot-primary) / 0.1)"
              }}
          >
            {/* Header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-chatbot-border bg-gradient-to-r from-chatbot-surface to-chatbot-surface-hover">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="font-semibold text-chatbot-text text-lg">AI Assistant</span>
                </div>
                <motion.button 
                  onClick={() => setOpen(false)} 
                  aria-label="Close Chatbot"
                  className="text-chatbot-text-muted hover:text-chatbot-text transition-colors p-1 rounded-full hover:bg-chatbot-surface-hover"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                <FaTimes className="w-5 h-5" />
                </motion.button>
            </div>

            {/* Messages */}
              <div 
                className="flex-1 px-4 py-4 space-y-4 overflow-y-auto bg-chatbot-bg scrollbar-thin scrollbar-thumb-chatbot-border scrollbar-track-chatbot-surface hover:scrollbar-thumb-chatbot-primary"
                style={{
                  scrollbarWidth: 'thin',
                  scrollbarColor: 'hsl(var(--chatbot-border)) hsl(var(--chatbot-surface))'
                }}
              >
              {messages.map((msg, idx) => (
                  <motion.div
                  key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.1 }}
                  className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                      className={`px-4 py-3 rounded-2xl text-sm max-w-[80%] shadow-lg relative ${
                        msg.sender === "user" 
                          ? "bg-chatbot-primary text-chatbot-text" 
                          : "bg-chatbot-surface text-chatbot-text border border-chatbot-border"
                      }`}
                      style={{
                        boxShadow: msg.sender === "user" 
                          ? "0 4px 12px hsl(var(--chatbot-primary) / 0.3)" 
                          : "0 4px 12px rgba(0,0,0,0.2)"
                      }}
                  >
                    {msg.text}
                  </div>
                  </motion.div>
              ))}
              {loading && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex justify-start"
                >
                  <div className="px-4 py-3 rounded-2xl text-sm max-w-[80%] shadow-lg relative bg-chatbot-surface text-chatbot-text border border-chatbot-border opacity-70">
                    <span className="animate-pulse">AI is typing...</span>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>

              {/* Placeholder Messages */}
              <div className="flex flex-wrap gap-2 px-4 py-3 border-t border-chatbot-border bg-chatbot-surface">
                {placeholderMessages.map((msg, idx) => (
                  <motion.button
                    key={idx}
                    className="px-4 py-2 rounded-full text-sm bg-chatbot-surface-hover text-chatbot-text-muted hover:text-chatbot-text hover:bg-chatbot-border transition-all duration-200 border border-chatbot-border"
                    onClick={() => handlePlaceholderClick(msg)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    disabled={loading}
                  >
                    {msg}
                  </motion.button>
                ))}
              </div>

            {/* Input */}
              <div className="flex items-center gap-3 border-t border-chatbot-border bg-chatbot-surface px-4 py-4">
              <input
                type="text"
                  className="text-black flex-1 rounded-xl px-4 py-3 bg-chatbot-bg text-chatbot-text outline-none border border-chatbot-border focus:border-chatbot-primary transition-colors placeholder-chatbot-text-muted"
                placeholder="Type your message..."
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                autoFocus
                disabled={loading}
              />
                <motion.button
                  className="p-3 rounded-xl bg-chatbot-primary hover:bg-chatbot-primary-hover text-chatbot-text transition-all duration-200 shadow-lg"
                onClick={handleSend}
                aria-label="Send Message"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  style={{
                    boxShadow: "0 4px 12px hsl(var(--chatbot-primary) / 0.4)"
                  }}
                  disabled={loading || !input.trim()}
              >
                  <FaPaperPlane className="w-4 h-4" />
                </motion.button>
            </div>
            </motion.div>
          </motion.div>
      )}
      </AnimatePresence>
    </>
  );
};

export default Chatbot;