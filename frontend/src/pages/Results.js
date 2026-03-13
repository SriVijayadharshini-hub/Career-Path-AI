import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../services/api";

import { Bar, Radar } from "react-chartjs-2";
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

  useEffect(() => {

    if (!scores) return;

    const fetchAI = async () => {

      try {

        // AI Career Prediction
        const pred = await API.post("/predict_career", {
          R: scores.R,
          I: scores.I,
          A: scores.A,
          S: scores.S,
          E: scores.E,
          C: scores.C,
          interest: "Engineering"
        });

        setPrediction(pred.data);

        // Skill Gap
        const skill = await API.post("/skill_gap", {
          career: pred.data.model_recommendation,
          python: 6,
          maths: 6,
          communication: 6
        });

        setSkillGap(skill.data);

        // Course Recommendation
        const course = await API.post("/recommend_courses", {
          career: pred.data.model_recommendation,
          level: skill.data.recommended_level
        });

        setCourses(course.data.recommended_courses);

        // Career Simulation
        const sim = await API.post("/career_simulation", {
          career: pred.data.model_recommendation,
          level: skill.data.recommended_level
        });

        setSalary(sim.data);

        // Explainable AI
        const explain = await API.post("/explain_prediction", {
          R: scores.R,
          I: scores.I,
          A: scores.A,
          S: scores.S,
          E: scores.E,
          C: scores.C
        });

        setExplanation(explain.data);

      } catch (error) {

        console.error("API Error:", error);

      }

    };

    fetchAI();

  }, [scores]);

  if (!scores) {
    return <h2>No assessment data available</h2>;
  }

  // Career Probability Chart
  const chartData = prediction ? {
    labels: Object.keys(prediction.probabilities),
    datasets: [
      {
        label: "Career Probability %",
        data: Object.values(prediction.probabilities)
      }
    ]
  } : null;

  // RIASEC Radar Chart
  const radarData = {
    labels: [
      "Realistic",
      "Investigative",
      "Artistic",
      "Social",
      "Enterprising",
      "Conventional"
    ],
    datasets: [
      {
        label: "RIASEC Personality Profile",
        data: [
          scores.R,
          scores.I,
          scores.A,
          scores.S,
          scores.E,
          scores.C
        ]
      }
    ]
  };

  return (
    <div style={{ padding: "30px" }}>

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

      <div style={{ width: "500px" }}>
        <Radar data={radarData} />
      </div>

      {prediction && (
        <>
          <h2>AI Career Recommendation</h2>

          <p><b>Recommended Career:</b> {prediction.model_recommendation}</p>
          <p>{prediction.interest_analysis}</p>

          <h2>Career Probability Chart</h2>

          <div style={{ width: "500px" }}>
            <Bar data={chartData} />
          </div>
        </>
      )}

      {explanation && (
        <>
          <h2>Explainable AI Insight</h2>

          <p>
            <b>Top Influencing Personality Factor:</b> {explanation.top_influencing_factor}
          </p>
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
            {courses.map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ul>
        </>
      )}

      {salary && (
        <>
          <h2>Future Salary Projection</h2>

          <ul>
            {salary.growth_stages.map((stage, i) => (
              <li key={i}>
                {stage} → ₹{salary.salary_projection[i]}
              </li>
            ))}
          </ul>
        </>
      )}

    </div>
  );
}

export default Results;