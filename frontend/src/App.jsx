import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [incidents, setIncidents] = useState([]);
  const [tickets, setTickets] = useState([]);

  // -----------------------------
  // Load Incidents & Tickets
  // -----------------------------
  const loadData = async () => {
    try {
      const incidentRes = await axios.get(
        "http://127.0.0.1:8000/api/incidents/"
      );

      const ticketRes = await axios.get(
        "http://127.0.0.1:8000/api/tickets/"
      );

      setIncidents(incidentRes.data);
      setTickets(ticketRes.data);
    } catch (err) {
      console.error(err);
    }
  };

  // -----------------------------
  // Fault Simulator
  // -----------------------------
  const injectFault = async (faultType) => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/api/inject-fault/",
        {
          fault_type: faultType,
        }
      );

      alert(faultType + " injected successfully");

      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  // -----------------------------
  // Ticket Workflow
  // -----------------------------
  const updateTicket = async (ticketNumber, status) => {
    try {
      await axios.post(
        `http://127.0.0.1:8000/api/tickets/${ticketNumber}/status/`,
        {
          status: status,
        }
      );

      alert("Ticket updated successfully");

      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div
      style={{
        maxWidth: "1200px",
        margin: "auto",
        padding: "30px",
        fontFamily: "Arial",
        background: "#f5f5f5",
        minHeight: "100vh",
      }}
    >
      <h1 style={{ textAlign: "center" }}>
        ⚡ Propel AI Fault Localization Dashboard
      </h1>

      {/* Summary */}

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginTop: "20px",
          marginBottom: "30px",
        }}
      >
        <div
          style={{
            flex: 1,
            background: "white",
            padding: "20px",
            borderRadius: "10px",
            boxShadow: "0px 2px 6px rgba(0,0,0,.1)",
            textAlign: "center",
          }}
        >
          <h3>Total Incidents</h3>

          <h2>{incidents.length}</h2>
        </div>

        <div
          style={{
            flex: 1,
            background: "white",
            padding: "20px",
            borderRadius: "10px",
            boxShadow: "0px 2px 6px rgba(0,0,0,.1)",
            textAlign: "center",
          }}
        >
          <h3>Total Tickets</h3>

          <h2>{tickets.length}</h2>
        </div>
      </div>

      {/* Fault Simulator */}

      <h2>⚡ Fault Simulator</h2>

      <div
        style={{
          display: "flex",
          gap: "10px",
          flexWrap: "wrap",
          marginBottom: "30px",
        }}
      >
        <button onClick={() => injectFault("span_fault")}>
          Span Fault
        </button>

        <button onClick={() => injectFault("dt_fault")}>
          DT Fault
        </button>

        <button onClick={() => injectFault("feeder_fault")}>
          Feeder Fault
        </button>

        <button onClick={() => injectFault("device_failure")}>
          Device Failure
        </button>

        <button onClick={() => injectFault("duplicate_messages")}>
          Duplicate Messages
        </button>

        <button onClick={() => injectFault("out_of_order")}>
          Out-of-Order Telemetry
        </button>

        <button onClick={() => injectFault("scheduled_outage")}>
          Scheduled Outage
        </button>

        <button onClick={() => injectFault("repair_fault")}>
          Repair Fault
        </button>
      </div>

      <hr />

      {/* Incidents */}

      <h2>🚨 Incidents</h2>

      {incidents.map((incident) => (
        <div
          key={incident.incident_id}
          style={{
            background: "white",
            padding: "15px",
            marginBottom: "15px",
            borderRadius: "10px",
            boxShadow: "0px 2px 6px rgba(0,0,0,.1)",
          }}
        >
          <h3>{incident.incident_id}</h3>

          <p>
            <b>Fault:</b>{" "}
            {incident.start_pole} → {incident.end_pole}
          </p>

          <p>
            <b>Status:</b> {incident.status}
          </p>

          <p>
            <b>Confidence:</b> {incident.confidence}
          </p>
        </div>
      ))}

      <hr />

      {/* Tickets */}

      <h2>🎫 Tickets</h2>

      {tickets.map((ticket) => (
        <div
          key={ticket.ticket_number}
          style={{
            background: "white",
            padding: "15px",
            marginBottom: "15px",
            borderRadius: "10px",
            boxShadow: "0px 2px 6px rgba(0,0,0,.1)",
          }}
        >
          <h3>{ticket.ticket_number}</h3>

          <p>
            <b>Incident:</b> {ticket.incident}
          </p>

          <p>
            <b>Status:</b> {ticket.status}
          </p>

          <p>
            <b>Assigned To:</b>{" "}
            {ticket.assigned_to || "Not Assigned"}
          </p>

          <div
            style={{
              display: "flex",
              gap: "10px",
              flexWrap: "wrap",
              marginTop: "15px",
            }}
          >
            <button
              onClick={() =>
                updateTicket(
                  ticket.ticket_number,
                  "ACKNOWLEDGED"
                )
              }
            >
              Acknowledge
            </button>

            <button
              onClick={() =>
                updateTicket(
                  ticket.ticket_number,
                  "ASSIGNED"
                )
              }
            >
              Assign Crew
            </button>

            <button
              onClick={() =>
                updateTicket(
                  ticket.ticket_number,
                  "RESOLVED"
                )
              }
            >
              Resolve
            </button>

            <button
              onClick={() =>
                updateTicket(
                  ticket.ticket_number,
                  "CLOSED"
                )
              }
            >
              Close
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default App;