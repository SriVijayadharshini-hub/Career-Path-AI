import { useState } from "react";
import API from "../services/api";

function Chatbot() {

  const [question,setQuestion] = useState("");
  const [answer,setAnswer] = useState("");

  const askAI = async () => {

    const res = await API.post("/career_chatbot",{
      question:question
    });

    setAnswer(res.data.answer);

  };

  return(

    <div style={{marginTop:"30px"}}>

      <h2>AI Career Chatbot</h2>

      <input
        placeholder="Ask about career..."
        value={question}
        onChange={(e)=>setQuestion(e.target.value)}
      />

      <button onClick={askAI}>Ask AI</button>

      <p>{answer}</p>

    </div>

  );

}

export default Chatbot;