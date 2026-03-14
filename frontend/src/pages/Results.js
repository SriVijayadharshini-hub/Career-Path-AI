import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../services/api";

import { Bar, Radar, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  RadialLinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  RadialLinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function Results() {

  const location = useLocation();
  const scores = location.state?.RIASEC;

  const [prediction, setPrediction] = useState(null);
  const [skillGap, setSkillGap] = useState(null);
  const [courses, setCourses] = useState([]);
  const [salary, setSalary] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [roadmap, setRoadmap] = useState([]);
  const [progress, setProgress] = useState(null);

  const [question, setQuestion] = useState("");
  const [chatResponse, setChatResponse] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const askChatbot = async () => {
    try {
      const res = await API.post("/career_chatbot", {
        question: question
      });

      setChatResponse(res.data.answer);

    } catch (err) {
      console.error("Chatbot error:", err);
    }
  };

  const downloadReport = async () => {

    try {

      const res = await API.post(
        "/download_report",
        {
          name: "Student",
          career: prediction?.model_recommendation,
          level: skillGap?.recommended_level,
          factor: explanation?.top_influencing_factor
        },
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");

      link.href = url;
      link.download = "career_report.pdf";

      document.body.appendChild(link);
      link.click();

    } catch (err) {
      console.error("Report Download Error:", err);
    }

  };

  useEffect(() => {

    if (!scores) return;

    const fetchAI = async () => {

      try {

        setLoading(true);

        const predRes = await API.post("/predict_career", {
          R: scores.R,
          I: scores.I,
          A: scores.A,
          S: scores.S,
          E: scores.E,
          C: scores.C,
          interest: "Engineering"
        });

        const pred = predRes.data;
        setPrediction(pred);

        const skillRes = await API.post("/skill_gap", {
          career: pred.model_recommendation,
          python: 6,
          maths: 6,
          communication: 6
        });

        const skill = skillRes.data;
        setSkillGap(skill);

        const courseRes = await API.post("/recommend_courses", {
          career: pred.model_recommendation,
          level: skill.recommended_level
        });

        setCourses(courseRes.data?.recommended_courses || []);

        const simRes = await API.post("/career_simulation", {
          career: pred.model_recommendation,
          level: skill.recommended_level
        });

        setSalary(simRes.data);

        const explainRes = await API.post("/explain_prediction", {
          R: scores.R,
          I: scores.I,
          A: scores.A,
          S: scores.S,
          E: scores.E,
          C: scores.C
        });

        setExplanation(explainRes.data);

        const roadmapRes = await API.post("/career_roadmap", {
          career: pred.model_recommendation
        });

        setRoadmap(roadmapRes.data?.roadmap || []);

        const progressRes = await API.get("/skill_progress");

        setProgress(progressRes.data);

        await API.post("/save_result", {
          user_id: 1,
          career: pred.model_recommendation,
          level: skill.recommended_level
        });

        setLoading(false);

      } catch (err) {

        console.error("API Error:", err);
        setError("Failed to load AI analysis.");
        setLoading(false);

      }

    };

    fetchAI();

  }, [scores]);

  if (!scores) return <h2>No assessment data available</h2>;
  if (loading) return <h2>Loading AI Career Analysis...</h2>;
  if (error) return <h2>{error}</h2>;

  const chartData = prediction ? {
    labels: Object.keys(prediction.probabilities || {}),
    datasets: [
      {
        label: "Career Probability %",
        data: Object.values(prediction.probabilities || [])
      }
    ]
  } : null;

  const radarData = {
    labels: ["Realistic","Investigative","Artistic","Social","Enterprising","Conventional"],
    datasets: [
      {
        label: "RIASEC Personality Profile",
        data: [scores.R,scores.I,scores.A,scores.S,scores.E,scores.C]
      }
    ]
  };

  const salaryChart = salary ? {
    labels: salary.growth_stages || [],
    datasets: [
      {
        label: "Salary Projection (₹)",
        data: salary.salary_projection || []
      }
    ]
  } : null;

  const progressChart = progress ? {
    labels: progress.months,
    datasets: [
      {
        label: "Python Skill Progress",
        data: progress.python
      }
    ]
  } : null;

  return (

    <div className="dashboard">

      <h1>AI Career Guidance Dashboard</h1>

      <h2>RIASEC Scores</h2>

      <ul>
        <li>Realistic: {scores.R}</li>
        <li>Investigative: {scores.I}</li>
        <li>Artistic: {scores.A}</li>
        <li>Social: {scores.S}</li>
        <li>Enterprising: {scores.E}</li>
        <li>Conventional: {scores.C}</li>
      </ul>

      <h2>RIASEC Personality Radar Chart</h2>
      <div className="chart-box">
        <Radar data={radarData} />
      </div>

      {prediction && (
        <>
          <h2>AI Career Recommendation</h2>
          <p><b>Recommended Career:</b> {prediction.model_recommendation}</p>
          <p>{prediction.interest_analysis}</p>

          <h2>Career Probability Chart</h2>
          <div className="chart-box">
            <Bar data={chartData} />
          </div>
        </>
      )}

      {explanation && (
        <>
          <h2>Explainable AI Insight</h2>
          <p><b>Top Influencing Personality Factor:</b> {explanation.top_influencing_factor}</p>
        </>
      )}

      {skillGap && (
        <>
          <h2>Skill Gap Analysis</h2>
          <p>Gap Score: {skillGap.gap_score}</p>
          <p>Recommended Level: {skillGap.recommended_level}</p>
        </>
      )}

      {courses.length > 0 && (
        <>
          <h2>Recommended Courses</h2>
          <ul>
            {courses.map((course, i) => (
              <li key={i}>
                {course.name ? (
                  <>
                    {course.name} - {course.platform}
                    <br/>
                    <a href={course.link} target="_blank" rel="noreferrer">
                      Start Course
                    </a>
                  </>
                ) : course}
              </li>
            ))}
          </ul>
        </>
      )}

      {roadmap.length > 0 && (
        <>
          <h2>Career Roadmap</h2>
          <ol>
            {roadmap.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </>
      )}

      {salary && (
        <>
          <h2>Future Career Salary Growth</h2>
          <div className="chart-box">
            <Line data={salaryChart} />
          </div>
        </>
      )}

      {progress && (
        <>
          <h2>Skill Progress Chart</h2>
          <div className="chart-box">
            <Line data={progressChart} />
          </div>
        </>
      )}

      <h2>AI Career Chatbot</h2>

      <input
        type="text"
        placeholder="Ask about your career..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askChatbot}>
        Ask AI
      </button>

      {chatResponse && (
        <p>
          <b>AI Answer:</b> {chatResponse}
        </p>
      )}

      <br/><br/>

      <button onClick={downloadReport}>
        Download AI Career Report
      </button>

    </div>

  );
}

export default Results;