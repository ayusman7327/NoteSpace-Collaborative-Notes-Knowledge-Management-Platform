import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import {
  deleteWorkspace,
  getWorkspace,
  updateWorkspace,
} from "../api/workspaceSettings";

import "./WorkspaceSettingsPanel.css";

function WorkspaceSettingsPanel({ open, onClose, workspaceId }) {
  const navigate = useNavigate();

  const [workspace, setWorkspace] = useState(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!open || !workspaceId) {
      return;
    }

    const loadWorkspace = async () => {
      setLoading(true);

      try {
        const data = await getWorkspace(workspaceId);

        setWorkspace(data);
        setName(data.name || "");
        setDescription(data.description || "");
      } catch (error) {
        toast.error(
          error.response?.data?.detail || "Unable to load workspace settings",
        );
      } finally {
        setLoading(false);
      }
    };

    loadWorkspace();
  }, [open, workspaceId]);

  const handleSave = async (event) => {
    event.preventDefault();

    const cleanedName = name.trim();

    if (!cleanedName) {
      toast.error("Workspace name is required");
      return;
    }

    setSaving(true);

    try {
      const updated = await updateWorkspace(workspaceId, {
        name: cleanedName,
        description: description.trim(),
      });

      setWorkspace(updated);

      toast.success("Workspace settings updated");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to update workspace");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    const confirmed = window.confirm("Delete this workspace permanently?");

    if (!confirmed) {
      return;
    }

    setDeleting(true);

    try {
      await deleteWorkspace(workspaceId);

      toast.success("Workspace deleted");

      navigate("/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to delete workspace");
    } finally {
      setDeleting(false);
    }
  };

  if (!open) {
    return null;
  }

  return (
    <aside className="workspace-settings-panel">
      <div className="workspace-settings-header">
        <div>
          <span>WORKSPACE</span>

          <h2>Settings</h2>

          <p>Manage workspace details and preferences.</p>
        </div>

        <button type="button" onClick={onClose}>
          ×
        </button>
      </div>

      <div className="workspace-settings-body">
        {loading ? (
          <div className="workspace-settings-message">Loading settings...</div>
        ) : (
          <>
            <form className="workspace-settings-form" onSubmit={handleSave}>
              <div className="workspace-setting-field">
                <label>Workspace name</label>

                <input
                  type="text"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  maxLength={255}
                />
              </div>

              <div className="workspace-setting-field">
                <label>Description</label>

                <textarea
                  value={description}
                  onChange={(event) => setDescription(event.target.value)}
                  placeholder="What is this workspace for?"
                  maxLength={1000}
                />
              </div>

              <button
                type="submit"
                className="workspace-settings-save"
                disabled={saving}
              >
                {saving ? "Saving..." : "Save changes"}
              </button>
            </form>

            <div className="workspace-settings-meta">
              <h3>Workspace information</h3>

              <div>
                <span>Workspace ID</span>

                <strong>{workspace?.id}</strong>
              </div>

              <div>
                <span>Created</span>

                <strong>
                  {workspace?.created_at
                    ? new Date(workspace.created_at).toLocaleDateString()
                    : "Unknown"}
                </strong>
              </div>
            </div>

            <div className="workspace-danger-zone">
              <span>DANGER ZONE</span>

              <h3>Delete workspace</h3>

              <p>
                This permanently removes the workspace and its associated
                content.
              </p>

              <button type="button" onClick={handleDelete} disabled={deleting}>
                {deleting ? "Deleting..." : "Delete workspace"}
              </button>
            </div>
          </>
        )}
      </div>
    </aside>
  );
}

export default WorkspaceSettingsPanel;
