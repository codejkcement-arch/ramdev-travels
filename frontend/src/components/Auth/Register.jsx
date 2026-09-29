import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../../services/authService";

export default function Register() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    password: "",
  });

  const [error, setError] = useState("");
  const nav = useNavigate();

  const set = (key) => (e) =>
    setForm({ ...form, [key]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setError("");

    try {
      const response = await register(form);
      console.log("REGISTER SUCCESS:", response.data);
      nav("/login");
    } catch (e) {
      console.error("REGISTER ERROR:", e);

      const message =
        e.response?.data?.detail ||
        e.response?.data?.message ||
        e.message ||
        "Registration failed";

      setError(`Registration failed: ${message}`);
    }
  }

  return (
    <div className="card" style={{ maxWidth: 450, margin: "50px auto" }}>
      <h2>Create account</h2>

      {error && (
        <p style={{ color: "crimson", whiteSpace: "pre-wrap" }}>
          {error}
        </p>
      )}

      <form onSubmit={submit}>
        {["name", "email", "phone", "password"].map((k) => (
          <input
            key={k}
            placeholder={k}
            type={
              k === "password"
                ? "password"
                : k === "email"
                ? "email"
                : "text"
            }
            value={form[k]}
            onChange={set(k)}
            style={{
              width: "100%",
              margin: "10px 0",
              padding: 10,
            }}
          />
        ))}

        <button className="btn">Register</button>
      </form>
    </div>
  );
}
