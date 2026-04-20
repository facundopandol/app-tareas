import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [tareas, setTareas] = useState([]);
  const [nuevaTarea, setNuevaTarea] = useState("");
  const [mensaje, setMensaje] = useState("");

  const cargarTareas = async () => {
    try {
      const res = await fetch(`${API_URL}/tasks`);
      const data = await res.json();
      setTareas(data);
    } catch (err) {
      setMensaje("Error al cargar tareas");
    }
  };

  const agregarTarea = async () => {
    if (!nuevaTarea.trim()) {
      setMensaje("Escribí una tarea");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ titulo: nuevaTarea }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMensaje(data.detail);
        return;
      }

      setNuevaTarea("");
      setMensaje(data.mensaje);
      cargarTareas();
    } catch {
      setMensaje("Error de conexión");
    }
  };

  const eliminarTarea = async (id) => {
    const confirmar = window.confirm("¿Seguro que querés eliminar esta tarea?");
    if (!confirmar) return;

    try {
      const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
      });

      const data = await res.json();

      if (!res.ok) {
        setMensaje(data.detail);
        return;
      }

      setMensaje(data.mensaje);
      cargarTareas();
    } catch {
      setMensaje("Error al eliminar");
    }
  };

  const toggleTarea = async (id) => {
    try {
      const res = await fetch(`${API_URL}/tasks/${id}/toggle`, {
        method: "PUT",
      });

      const data = await res.json();

      if (!res.ok) {
        setMensaje(data.detail);
        return;
      }

      cargarTareas();
    } catch {
      setMensaje("Error al actualizar");
    }
  };

  useEffect(() => {
    cargarTareas();
  }, []);

  const pendientes = tareas.filter((t) => !t.completada);
  const completadas = tareas.filter((t) => t.completada);

  return (
    <div className="container">
      <h1>Lista de tareas</h1>

      <p>Pendientes: {pendientes.length}</p>

      <div className="input-group">
        <input
          type="text"
          placeholder="Nueva tarea"
          value={nuevaTarea}
          onChange={(e) => setNuevaTarea(e.target.value)}
        />
        <button onClick={agregarTarea}>Agregar</button>
      </div>

      {mensaje && <p>{mensaje}</p>}

      <h2>Pendientes</h2>
      <ul>
        {pendientes.length === 0 ? (
          <p>No hay tareas pendientes</p>
        ) : (
          pendientes.map((t) => (
            <li key={t.id}>
              <span
                onClick={() => toggleTarea(t.id)}
                style={{ cursor: "pointer" }}
              >
                {t.titulo}
              </span>
              <button onClick={() => eliminarTarea(t.id)}>❌</button>
            </li>
          ))
        )}
      </ul>

      <h2>Completadas</h2>
      <ul>
        {completadas.length === 0 ? (
          <p>No hay tareas completadas</p>
        ) : (
          completadas.map((t) => (
            <li key={t.id}>
              <span
                onClick={() => toggleTarea(t.id)}
                style={{
                  textDecoration: "line-through",
                  cursor: "pointer",
                }}
              >
                {t.titulo}
              </span>
              <button onClick={() => eliminarTarea(t.id)}>❌</button>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default App;