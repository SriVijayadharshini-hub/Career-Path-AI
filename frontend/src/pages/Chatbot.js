import { useState } from "react";
import API from "../services/api";

function Chatbot() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  const sendQuestion = async () => {

    if (!question) return;

    const userMessage = { sender: "user", text: question };

    setMessages([...messages, userMessage]);

    try {

      const res = await API.post("/chatbot", {
        question: question
      });

      const botMessage = {
        sender: "bot",
        text: res.data.answer
      };

      setMessages(prev => [...prev, botMessage]);

      setQuestion("");

    } catch (error) {
      console.error("Chatbot error:", error);
    }

  };

  return (

    <div style={{ padding: "30px" }}>

      <h1>AI Career Chatbot</h1>

      <div
        style={{
          border: "1px solid #ccc",
          padding: "20px",
          height: "400px",
          overflowY: "scroll",
          marginBottom: "20px"
        }}
      >

        {messages.map((msg, i) => (

          <div key={i} style={{
            textAlign: msg.sender === "user" ? "right" : "left",
            marginBottom: "10px"
          }}>

            <b>{msg.sender === "user" ? "You" : "AI"}:</b> {msg.text}

          </div>

        ))}

      </div>

      <input
        type="text"
        placeholder="Ask about careers..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "70%", padding: "10px" }}
      />

      <button
        onClick={sendQuestion}
        style={{ padding: "10px 20px", marginLeft: "10px" }}
      >
        Ask
      </button>

    </div>

  );

}

export default Chatbot;