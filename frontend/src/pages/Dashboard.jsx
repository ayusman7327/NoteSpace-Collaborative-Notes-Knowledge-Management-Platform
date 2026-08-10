import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import { createWorkspace, getWorkspaces } from "../api/workspaces";

import { getFavoritePages, getRecentPages } from "../api/pages";

import { useAuth } from "../context/AuthContext";
import SearchModal from "../components/SearchModal";

import "./Dashboard.css";

function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [workspaces, setWorkspaces] = useState([]);
  const [workspaceName, setWorkspaceName] = useState("");

  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  const [workspaceSearch, setWorkspaceSearch] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);

  const [recentPages, setRecentPages] = useState([]);
  const [favoritePages, setFavoritePages] = useState([]);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const workspaceData = await getWorkspaces();

        setWorkspaces(workspaceData);

        const recentRequests = workspaceData.map(async (workspace) => {
          try {
            const pages = await getRecentPages(workspace.id);

            return pages.map((page) => ({
              ...page,
              workspace_name: workspace.name,
            }));
          } catch {
            return [];
          }
        });

        const favoriteRequests = workspaceData.map(async (workspace) => {
          try {
            const pages = await getFavoritePages(workspace.id);

            return pages.map((page) => ({
              ...page,
              workspace_name: workspace.name,
            }));
          } catch {
            return [];
          }
        });

        const recentResults = await Promise.all(recentRequests);

        const favoriteResults = await Promise.all(favoriteRequests);

        const mergedRecent = recentResults
          .flat()
          .sort((a, b) => {
            const first = a.last_opened_at
              ? new Date(a.last_opened_at)
              : new Date(0);

            const second = b.last_opened_at
              ? new Date(b.last_opened_at)
              : new Date(0);

            return second - first;
          })
          .slice(0, 6);

        setRecentPages(mergedRecent);
        setFavoritePages(favoriteResults.flat());
      } catch (error) {
        toast.error(error.response?.data?.detail || "Unable to load dashboard");
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  useEffect(() => {
    const handleShortcut = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setSearchOpen(true);
      }
    };

    window.addEventListener("keydown", handleShortcut);

    return () => {
      window.removeEventListener("keydown", handleShortcut);
    };
  }, []);

  const filteredWorkspaces = useMemo(() => {
    const query = workspaceSearch.trim().toLowerCase();

    if (!query) {
      return workspaces;
    }

    return workspaces.filter((workspace) =>
      workspace.name.toLowerCase().includes(query),
    );
  }, [workspaceSearch, workspaces]);

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

      setWorkspaces((current) => [newWorkspace, ...current]);

      setWorkspaceName("");

      toast.success("Workspace created");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to create workspace");
    } finally {
      setCreating(false);
    }
  };

  const getInitials = () => {
    if (!user?.name) {
      return "U";
    }

    return user.name
      .split(" ")
      .map((part) => part[0])
      .slice(0, 2)
      .join("")
      .toUpperCase();
  };

  const formatRecentTime = (dateValue) => {
    if (!dateValue) {
      return "Recently";
    }

    const date = new Date(dateValue);

    const now = new Date();

    const difference = now.getTime() - date.getTime();

    const minutes = Math.floor(difference / 60000);

    if (minutes < 1) {
      return "Just now";
    }

    if (minutes < 60) {
      return `${minutes} min ago`;
    }

    const hours = Math.floor(minutes / 60);

    if (hours < 24) {
      return `${hours} hr ago`;
    }

    const days = Math.floor(hours / 24);

    if (days < 7) {
      return `${days} day${days === 1 ? "" : "s"} ago`;
    }

    return date.toLocaleDateString();
  };

  const openRecentPage = (page) => {
    navigate(`/workspace/${page.workspace_id}?page=${page.id}`);
  };

  return (
    <div className="dashboard-shell">
      <aside className="dashboard-sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-logo">N</div>

          <div>
            <h2>NoteSpace</h2>

            <span>Knowledge workspace</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button type="button" className="nav-item active">
            <span>⌂</span>
            Home
          </button>

          <button type="button" className="nav-item">
            <span>▣</span>
            Workspaces
          </button>

          <button type="button" className="nav-item">
            <span>★</span>
            Favorites
          </button>

          <button type="button" className="nav-item">
            <span>◷</span>
            Recent
          </button>

          <button
            type="button"
            className="nav-item"
            onClick={() => setSearchOpen(true)}
          >
            <span>⌕</span>
            Search
          </button>
        </nav>

        <div className="sidebar-divider" />

        <div className="sidebar-section-title">My workspaces</div>

        <div className="sidebar-workspaces">
          {workspaces.slice(0, 5).map((workspace) => (
            <button
              key={workspace.id}
              type="button"
              className="sidebar-workspace-item"
              onClick={() => navigate(`/workspace/${workspace.id}`)}
            >
              <span className="workspace-mini-icon">
                {workspace.name.charAt(0).toUpperCase()}
              </span>

              <span>{workspace.name}</span>
            </button>
          ))}
        </div>

        <div className="sidebar-bottom">
          <button type="button" className="nav-item">
            <span>⚙</span>
            Settings
          </button>

          <button type="button" className="nav-item">
            <span>?</span>
            Help & Support
          </button>
        </div>
      </aside>

      <main className="dashboard-main">
        <header className="dashboard-topbar">
          <div className="topbar-search" onClick={() => setSearchOpen(true)}>
            <span>⌕</span>

            <input
              readOnly
              type="text"
              placeholder="Search your knowledge..."
            />

            <kbd>⌘ K</kbd>
          </div>

          <div className="topbar-actions">
            <button type="button" className="notification-button">
              ♢
            </button>

            <div className="profile-wrapper">
              <div className="profile-avatar">{getInitials()}</div>

              <div className="profile-info">
                <strong>{user?.name}</strong>

                <span>{user?.email}</span>
              </div>

              <button
                type="button"
                className="logout-text-button"
                onClick={logout}
              >
                Log out
              </button>
            </div>
          </div>
        </header>

        <div className="dashboard-content">
          <section className="welcome-section">
            <div>
              <span className="section-eyebrow">Dashboard</span>

              <h1>Welcome back, {user?.name?.split(" ")[0] || "there"}.</h1>

              <p>
                Pick up where you left off and keep your knowledge organized.
              </p>
            </div>

            <form
              className="create-workspace-form"
              onSubmit={handleCreateWorkspace}
            >
              <input
                type="text"
                placeholder="Workspace name"
                value={workspaceName}
                onChange={(event) => setWorkspaceName(event.target.value)}
                minLength={2}
                maxLength={150}
              />

              <button type="submit" disabled={creating}>
                <span>+</span>

                {creating ? "Creating..." : "New workspace"}
              </button>
            </form>
          </section>

          <section className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">▣</div>

              <div>
                <span>Total Workspaces</span>

                <strong>{workspaces.length}</strong>
              </div>

              <span className="stat-change">Active</span>
            </div>

            <div className="stat-card">
              <div className="stat-icon">◷</div>

              <div>
                <span>Recent Pages</span>

                <strong>{recentPages.length}</strong>
              </div>

              <span className="stat-change">Last opened</span>
            </div>

            <div className="stat-card">
              <div className="stat-icon">★</div>

              <div>
                <span>Favorites</span>

                <strong>{favoritePages.length}</strong>
              </div>

              <span className="stat-change">Saved pages</span>
            </div>

            <div className="stat-card">
              <div className="stat-icon">⌕</div>

              <div>
                <span>Global Search</span>

                <strong>⌘K</strong>
              </div>

              <span className="stat-change">Ready</span>
            </div>
          </section>

          <section className="dashboard-section">
            <div className="section-heading">
              <div>
                <h2>Your workspaces</h2>

                <p>Access and manage your collaborative spaces.</p>
              </div>

              <span>
                {filteredWorkspaces.length} workspace
                {filteredWorkspaces.length === 1 ? "" : "s"}
              </span>
            </div>

            <div className="workspace-filter-row">
              <input
                type="text"
                placeholder="Filter workspaces..."
                value={workspaceSearch}
                onChange={(event) => setWorkspaceSearch(event.target.value)}
              />
            </div>

            {loading ? (
              <div className="workspace-skeleton-grid">
                <div className="workspace-skeleton" />
                <div className="workspace-skeleton" />
                <div className="workspace-skeleton" />
              </div>
            ) : filteredWorkspaces.length === 0 ? (
              <div className="premium-empty-state">
                <div className="empty-state-icon">N</div>

                <h3>
                  {workspaceSearch
                    ? "No matching workspaces"
                    : "Create your first workspace"}
                </h3>

                <p>
                  {workspaceSearch
                    ? "Try searching with another workspace name."
                    : "Workspaces keep projects, documents and ideas organized in one place."}
                </p>
              </div>
            ) : (
              <div className="premium-workspace-grid">
                {filteredWorkspaces.map((workspace) => (
                  <article
                    className="premium-workspace-card"
                    key={workspace.id}
                    onClick={() => navigate(`/workspace/${workspace.id}`)}
                  >
                    <div className="workspace-card-top">
                      <div className="workspace-large-icon">
                        {workspace.name.charAt(0).toUpperCase()}
                      </div>

                      <button
                        type="button"
                        className="workspace-menu-button"
                        onClick={(event) => event.stopPropagation()}
                      >
                        •••
                      </button>
                    </div>

                    <div className="workspace-card-body">
                      <h3>{workspace.name}</h3>

                      <p>
                        Collaborative workspace for notes, documents and shared
                        knowledge.
                      </p>
                    </div>

                    <div className="workspace-meta">
                      <span>
                        Created{" "}
                        {workspace.created_at
                          ? new Date(workspace.created_at).toLocaleDateString()
                          : "recently"}
                      </span>

                      <span className="open-workspace">Open →</span>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>

          <section className="bottom-dashboard-grid">
            <div className="activity-panel">
              <div className="section-heading compact">
                <div>
                  <h2>Recently opened</h2>

                  <p>Continue where you left off.</p>
                </div>

                <span>{recentPages.length} recent</span>
              </div>

              {recentPages.length === 0 ? (
                <div className="activity-empty">
                  <div className="activity-empty-icon">◷</div>

                  <div>
                    <strong>No recent pages yet</strong>

                    <p>Pages you open will appear here.</p>
                  </div>
                </div>
              ) : (
                <div className="recent-pages-list">
                  {recentPages.map((page) => (
                    <button
                      key={`${page.workspace_id}-${page.id}`}
                      type="button"
                      className="recent-page-item"
                      onClick={() => openRecentPage(page)}
                    >
                      <div className="recent-page-icon">▤</div>

                      <div className="recent-page-content">
                        <strong>{page.title}</strong>

                        <span>{page.workspace_name}</span>
                      </div>

                      <div className="recent-page-time">
                        {formatRecentTime(page.last_opened_at)}
                      </div>

                      {page.is_favorite && (
                        <span className="recent-page-star">★</span>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div className="quick-start-panel">
              <span className="section-eyebrow">Quick start</span>

              <h2>Build your knowledge base</h2>

              <p>
                Create a workspace, build structured pages, favorite important
                documents and find everything instantly using global search.
              </p>

              <button
                type="button"
                onClick={() => {
                  const input = document.querySelector(
                    ".create-workspace-form input",
                  );

                  input?.focus();
                }}
              >
                Create a workspace →
              </button>
            </div>
          </section>
        </div>
      </main>

      <SearchModal open={searchOpen} onClose={() => setSearchOpen(false)} />
    </div>
  );
}

export default Dashboard;
