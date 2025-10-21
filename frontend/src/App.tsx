import { useState } from "react";
import "./App.css";

interface Recommendation {
  meal_items: string[];
  kcal_total: number;
  protein_g: number;
  price_ksh: number;
  score: number;
}

function App() {
  const [formData, setFormData] = useState({
    age: "",
    gender: "female",
    weight_kg: "",
    height_cm: "",
    activity_level: "moderate",
    goal: "maintain_weight",
    dietary_preference: "none",
    daily_budget_ksh: "",
  });

  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle form submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          age: Number(formData.age),
          weight_kg: Number(formData.weight_kg),
          height_cm: Number(formData.height_cm),
          daily_budget_ksh: Number(formData.daily_budget_ksh),
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        setError(errData.detail?.[0]?.msg || "Error fetching recommendations.");
      } else {
        const data = await response.json();
        setRecommendations(data.recommendations || []);
      }
    } catch {
      setError("Error connecting to backend.");
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1>🥗 NutriAI - Personalized Meal Planner</h1>

      <form className="form-container" onSubmit={handleSubmit}>
        <div className="input-grid">
          <input
            name="age"
            placeholder="Age"
            value={formData.age}
            onChange={handleChange}
            required
          />

          <select name="gender" value={formData.gender} onChange={handleChange}>
            <option value="female">Female</option>
            <option value="male">Male</option>
          </select>

          <input
            name="weight_kg"
            placeholder="Weight (kg)"
            value={formData.weight_kg}
            onChange={handleChange}
            required
          />

          <input
            name="height_cm"
            placeholder="Height (cm)"
            value={formData.height_cm}
            onChange={handleChange}
            required
          />

          <select name="activity_level" value={formData.activity_level} onChange={handleChange}>
            <option value="low">Low</option>
            <option value="moderate">Moderate</option>
            <option value="high">High</option>
          </select>

          <select name="goal" value={formData.goal} onChange={handleChange}>
            <option value="lose_weight">Lose Weight</option>
            <option value="maintain_weight">Maintain Weight</option>
            <option value="gain_weight">Gain Weight</option>
          </select>

          <select name="dietary_preference" value={formData.dietary_preference} onChange={handleChange}>
            <option value="none">No Preference</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="low_carb">Low Carb</option>
          </select>

          <input
            name="daily_budget_ksh"
            placeholder="Daily Budget (KSh)"
            value={formData.daily_budget_ksh}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Get Recommendations"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      <div className="results-container">
        {recommendations.length > 0 && <h2>Recommended Meals 🍱</h2>}
        {recommendations.map((rec, index) => (
  <div key={index} className="card">
    <h3>{rec.meal_items.join(" + ")}</h3>
    <p>Calories: {rec.kcal_total}</p>
    <p>Protein: {rec.protein_g}g</p>
    <p>Price: KSh {rec.price_ksh}</p>
    <p>Score: {rec.score}</p>
  </div>
))}
      </div>
    </div>
  );
}

export default App;
