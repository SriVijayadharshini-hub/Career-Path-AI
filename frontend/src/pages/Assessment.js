import { useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";

function Assessment() {

  const navigate = useNavigate();

  const questions = [
    "I enjoy working with machines or tools",
    "I like building or fixing things",
    "I prefer practical activities over theory",

    "I enjoy solving complex problems",
    "I like scientific experiments",
    "I enjoy analysing data",

    "I enjoy drawing or designing",
    "I like creative writing or storytelling",
    "I enjoy expressing ideas through art",

    "I enjoy helping people solve problems",
    "I like teaching or guiding others",
    "I feel comfortable working in teams",

    "I enjoy leading projects",
    "I like persuading people to accept ideas",
    "I enjoy business or management",

    "I like organizing data or files",
    "I enjoy structured tasks",
    "I prefer working with clear instructions"
  ];

  const [answers, setAnswers] = useState(Array(18).fill(3));

  const handleChange = (index, value) => {
    const newAnswers = [...answers];
    newAnswers[index] = value;
    setAnswers(newAnswers);
  };

  const handleSubmit = async () => {

    try {

      const data = {
        user_id: 1,
        q1: answers[0],
        q2: answers[1],
        q3: answers[2],
        q4: answers[3],
        q5: answers[4],
        q6: answers[5],
        q7: answers[6],
        q8: answers[7],
        q9: answers[8],
        q10: answers[9],
        q11: answers[10],
        q12: answers[11],
        q13: answers[12],
        q14: answers[13],
        q15: answers[14],
        q16: answers[15],
        q17: answers[16],
        q18: answers[17]
      };

      const response = await API.post("/assessment", data);

      console.log(response.data);

      navigate("/results", { state: response.data });

    } catch (error) {

      console.error(error);
      alert("Error submitting assessment");

    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2>RIASEC Career Assessment</h2>

      {questions.map((q, index) => (
        <div key={index} style={{ marginBottom: "20px" }}>

          <p>{q}</p>

          <input
            type="range"
            min="1"
            max="5"
            value={answers[index]}
            onChange={(e) =>
              handleChange(index, parseInt(e.target.value))
            }
          />

          <span> {answers[index]}</span>

        </div>
      ))}

      <button
        onClick={handleSubmit}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer"
        }}
      >
        Submit Assessment
      </button>

    </div>
  );
}

export default Assessment;