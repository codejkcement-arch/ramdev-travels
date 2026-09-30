import { useEffect, useState } from "react";
import api from "../../services/api";

export default function Dashboard() {
  const [s, setS] = useState(null);
  const [buses, setBuses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({
    operator: "Ramdev Travels",
    bus_number: "",
    source: "Jodhpur",
    destination: "Jaipur",
    departure_time: "22:00",
    arrival_time: "05:30",
    fare: "650",
    total_seats: "40",
  });

  async function loadBuses() {
    try {
      const r = await api.get("/admin/buses");
      setBuses(r.data);
    } catch {
      setMessage("Could not load buses.");
    }
  }

  useEffect(() => {
    api.get("/admin/stats").then((r) => setS(r.data));
    loadBuses();
  }, []);

  function change(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function addBus(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      await api.post("/admin/buses", {
        ...form,
        fare: Number(form.fare),
        total_seats: Number(form.total_seats),
      });

      setMessage("Bus added successfully.");
      setForm({
        ...form,
        bus_number: "",
      });
      await loadBuses();
    } catch (err) {
      setMessage(
        err?.response?.data?.detail || "Could not add bus."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2>Admin Dashboard</h2>

      {s && (
        <div
          style={{
            display: "flex",
            gap: 30,
            flexWrap: "wrap",
            marginBottom: 30,
          }}
        >
          <div>
            Users
            <br />
            <b>{s.users}</b>
          </div>

          <div>
            Bookings
            <br />
            <b>{s.bookings}</b>
          </div>

          <div>
            Revenue
            <br />
            <b>₹{s.revenue}</b>
          </div>
        </div>
      )}

      <hr />

      <h2>Bus Management</h2>

      <form onSubmit={addBus}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
            gap: 10,
          }}
        >
          <input
            name="operator"
            value={form.operator}
            onChange={change}
            placeholder="Operator"
          />

          <input
            name="bus_number"
            value={form.bus_number}
            onChange={change}
            placeholder="Bus Number"
            required
          />

          <input
            name="source"
            value={form.source}
            onChange={change}
            placeholder="Source"
            required
          />

          <input
            name="destination"
            value={form.destination}
            onChange={change}
            placeholder="Destination"
            required
          />

          <input
            name="departure_time"
            value={form.departure_time}
            onChange={change}
            placeholder="Departure"
            required
          />

          <input
            name="arrival_time"
            value={form.arrival_time}
            onChange={change}
            placeholder="Arrival"
            required
          />

          <input
            name="fare"
            type="number"
            value={form.fare}
            onChange={change}
            placeholder="Fare"
            required
          />

          <input
            name="total_seats"
            type="number"
            min="1"
            value={form.total_seats}
            onChange={change}
            placeholder="Seats"
            required
          />
        </div>

        <button
          className="btn"
          type="submit"
          disabled={loading}
          style={{ marginTop: 15 }}
        >
          {loading ? "Adding..." : "Add Bus"}
        </button>
      </form>

      {message && (
        <p style={{ marginTop: 15 }}>
          <b>{message}</b>
        </p>
      )}

      <h3 style={{ marginTop: 30 }}>Registered Buses</h3>

      {buses.length === 0 ? (
        <p>No buses registered yet.</p>
      ) : (
        <div>
          {buses.map((b) => (
            <div
              key={b.id}
              style={{
                borderTop: "1px solid #ddd",
                padding: "15px 0",
              }}
            >
              <b>{b.operator}</b> — {b.bus_number}
              <div>
                {b.source} → {b.destination}
              </div>
              <div>
                {b.departure_time} - {b.arrival_time} · ₹{b.fare} ·{" "}
                {b.total_seats} seats
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
