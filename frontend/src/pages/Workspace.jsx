import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import toast from "react-hot-toast";

import {
  createPage,
  deletePage,
  getTrash,
  getWorkspacePages,
  restorePage,
  updatePage,
} from "../api/pages";

import "./Workspace.css";

function Workspace() {
  const { workspaceId } = useParams();

  const [pages, setPages] = useState([]);
  const [trash, setTrash] = useState([]);

  const [selectedPage, setSelectedPage] = useState(null);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [creating, setCreating] = useState(false);

  const [showTrash, setShowTrash] = useState(false);

  useEffect(() => {
    const loadPages = async () => {
      try {
        const data = await getWorkspacePages(workspaceId);

        setPages(data);

        if (data.length > 0) {
          selectPage(data[0]);
        }
      } catch (error) {
        toast.error(error.response?.data?.detail || "Unable to load pages");
      } finally {
        setLoading(false);
      }
    };

    loadPages();
  }, [workspaceId]);

  const rootPages = useMemo(
    () => pages.filter((page) => page.parent_page_id === null),
    [pages],
  );

  const selectPage = (page) => {
    setSelectedPage(page);
    setTitle(page.title);
    setContent(page.content || "");
    setShowTrash(false);
  };

  const handleCreateRootPage = async () => {
    setCreating(true);

    try {
      const newPage = await createPage(workspaceId, "Untitled", null);

      setPages((current) => [...current, newPage]);
      selectPage(newPage);

      toast.success("Page created");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to create page");
    } finally {
      setCreating(false);
    }
  };

  const handleCreateChildPage = async (parentId) => {
    setCreating(true);

    try {
      const newPage = await createPage(workspaceId, "Untitled", parentId);

      setPages((current) => [...current, newPage]);
      selectPage(newPage);

      toast.success("Nested page created");
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Unable to create nested page",
      );
    } finally {
      setCreating(false);
    }
  };

  const handleSave = async () => {
    if (!selectedPage) return;

    setSaving(true);

    try {
      const updatedPage = await updatePage(selectedPage.id, {
        title,
        content,
      });

      setSelectedPage(updatedPage);

      setPages((current) =>
        current.map((page) =>
          page.id === updatedPage.id ? updatedPage : page,
        ),
      );

      toast.success("Page saved");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to save page");
    } finally {
      setSaving(false);
    }
  };

  const handleDeletePage = async () => {
    if (!selectedPage) return;

    try {
      const deleted = await deletePage(selectedPage.id);

      setPages((current) => current.filter((page) => page.id !== deleted.id));

      setSelectedPage(null);
      setTitle("");
      setContent("");

      toast.success("Page moved to trash");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to delete page");
    }
  };

  const handleOpenTrash = async () => {
    try {
      const data = await getTrash(workspaceId);

      setTrash(data);
      setSelectedPage(null);
      setShowTrash(true);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to load trash");
    }
  };

  const handleRestorePage = async (pageId) => {
    try {
      const restored = await restorePage(pageId);

      setTrash((current) => current.filter((page) => page.id !== pageId));

      setPages((current) => [...current, restored]);

      toast.success("Page restored");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to restore page");
    }
  };

  const renderPageTree = (parentId = null, level = 0) => {
    const childPages = pages.filter((page) => page.parent_page_id === parentId);

    return childPages.map((page) => (
      <div key={page.id}>
        <div
          className={
            selectedPage?.id === page.id ? "page-row active" : "page-row"
          }
          style={{
            paddingLeft: `${10 + level * 18}px`,
          }}
        >
          <button
            type="button"
            className="page-select-button"
            onClick={() => selectPage(page)}
          >
            <span>📄</span>
            <span className="page-title">{page.title}</span>
          </button>

          <button
            type="button"
            className="child-page-button"
            onClick={() => handleCreateChildPage(page.id)}
            title="Create nested page"
          >
            +
          </button>
        </div>

        {renderPageTree(page.id, level + 1)}
      </div>
    ));
  };

  return (
    <div className="workspace-layout">
      <aside className="workspace-sidebar">
        <div className="sidebar-top">
          <Link to="/dashboard" className="back-link">
            ← Workspaces
          </Link>

          <h2>NoteSpace</h2>
        </div>

        <button
          className="new-page-button"
          onClick={handleCreateRootPage}
          disabled={creating}
        >
          {creating ? "Creating..." : "+ New Page"}
        </button>

        <div className="page-list">
          {loading && <p className="sidebar-message">Loading pages...</p>}

          {!loading && rootPages.length === 0 && (
            <p className="sidebar-message">No pages yet.</p>
          )}

          {!loading && renderPageTree()}
        </div>

        <button
          type="button"
          className="trash-button"
          onClick={handleOpenTrash}
        >
          🗑 Trash
        </button>
      </aside>

      <main className="workspace-editor">
        {showTrash ? (
          <div className="trash-view">
            <h1>Trash</h1>

            {trash.length === 0 ? (
              <p>No deleted pages.</p>
            ) : (
              <div className="trash-list">
                {trash.map((page) => (
                  <div className="trash-item" key={page.id}>
                    <div>
                      <strong>{page.title}</strong>

                      <p>
                        Deleted{" "}
                        {page.deleted_at
                          ? new Date(page.deleted_at).toLocaleString()
                          : ""}
                      </p>
                    </div>

                    <button
                      type="button"
                      onClick={() => handleRestorePage(page.id)}
                    >
                      Restore
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : !selectedPage ? (
          <div className="empty-editor">
            <h1>Welcome to NoteSpace</h1>

            <p>Create a page from the sidebar to start writing.</p>

            <button onClick={handleCreateRootPage}>
              Create your first page
            </button>
          </div>
        ) : (
          <div className="editor-container">
            <div className="editor-header">
              <span className="save-status">
                {saving ? "Saving..." : "Ready"}
              </span>

              <button
                type="button"
                className="delete-button"
                onClick={handleDeletePage}
              >
                Delete
              </button>

              <button type="button" onClick={handleSave} disabled={saving}>
                {saving ? "Saving..." : "Save"}
              </button>
            </div>

            <input
              className="editor-title"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="Untitled"
            />

            <textarea
              className="editor-content"
              value={content}
              onChange={(event) => setContent(event.target.value)}
              placeholder="Start writing..."
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default Workspace;
