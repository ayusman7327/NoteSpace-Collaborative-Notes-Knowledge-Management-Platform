import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import { createWorkspace, getWorkspaces } from "../api/workspaces";
import { useAuth } from "../context/AuthContext";
import "./Dashboard.css";

function Dashboard() {
  const { user, logout } = useAuth();

  const [workspaces, setWorkspaces] = useState([]);
  const [workspaceName, setWorkspaceName] = useState("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const loadWorkspaces = async () => {
      try {
        const data = await getWorkspaces();
        setWorkspaces(data);
      } catch (error) {
        toast.error(
          error.response?.data?.detail || "Unable to load workspaces",
        );
      } finally {
        setLoading(false);
      }
    };

    loadWorkspaces();
  }, []);

  const handleCreateWorkspace = async (event) => {
    event.preventDefault();

    const cleanedName = workspaceName.trim();

    if (cleanedName.length < 2) {
      toast.error("Workspace name must contain at least 2 characters");
      return;
    }

    setCreating(true);

    try {
      const newWorkspace = await createWorkspace(cleanedName);

      setWorkspaces((currentWorkspaces) => [
        ...currentWorkspaces,
        newWorkspace,
      ]);

      setWorkspaceName("");
      toast.success("Workspace created");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to create workspace");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <h1>NoteSpace</h1>
          <p>Your collaborative knowledge workspace</p>
        </div>

        <div className="dashboard-user">
          <div className="user-details">
            <strong>{user?.name}</strong>
            <span>{user?.email}</span>
          </div>

          <button type="button" className="logout-button" onClick={logout}>
            Log out
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        <section className="dashboard-intro">
          <div>
            <p className="dashboard-label">Your workspaces</p>
            <h2>Organize your notes and shared knowledge</h2>
            <p>
              Create a workspace for projects, teams, study notes, or personal
              documentation.
            </p>
          </div>

          <form className="workspace-form" onSubmit={handleCreateWorkspace}>
            <input
              type="text"
              placeholder="Workspace name"
              value={workspaceName}
              onChange={(event) => setWorkspaceName(event.target.value)}
              minLength={2}
              maxLength={150}
              required
            />

            <button type="submit" disabled={creating}>
              {creating ? "Creating..." : "Create workspace"}
            </button>
          </form>
        </section>

        <section className="workspace-section">
          {loading ? (
            <div className="dashboard-message">Loading workspaces...</div>
          ) : workspaces.length === 0 ? (
            <div className="empty-workspaces">
              <div className="empty-icon">N</div>

              <h3>No workspaces yet</h3>

              <p>
                Create your first workspace to start adding pages and organizing
                your notes.
              </p>
            </div>
          ) : (
            <div className="workspace-grid">
              {workspaces.map((workspace) => (
                <button
                  type="button"
                  className="workspace-card"
                  key={workspace.id}
                >
                  <div className="workspace-icon">
                    {workspace.name.charAt(0).toUpperCase()}
                  </div>

                  <div className="workspace-card-content">
                    <h3>{workspace.name}</h3>

                    <p>
                      Created{" "}
                      {new Date(workspace.created_at).toLocaleDateString()}
                    </p>
                  </div>

                  <span className="workspace-arrow">→</span>
                </button>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
