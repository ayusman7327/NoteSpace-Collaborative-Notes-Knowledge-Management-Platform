import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import toast from "react-hot-toast";
import { EditorContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";

import {
  createPage,
  deletePage,
  favoritePage,
  getPageVersions,
  getTrash,
  getWorkspacePages,
  openPage,
  restorePage,
  restorePageVersion,
  unfavoritePage,
  updatePage,
} from "../api/pages";

import { useAuth } from "../context/AuthContext";

import AIAssistant from "../components/AIAssistant";
import CommentsPanel from "../components/CommentsPanel";
import InviteMembersModal from "../components/InviteMembersModal";
import WorkspaceMembersPanel from "../components/WorkspaceMembersPanel";

import "./Workspace.css";

function Workspace() {
  const { workspaceId } = useParams();
  const { user } = useAuth();

  const [pages, setPages] = useState([]);
  const [trash, setTrash] = useState([]);
  const [versions, setVersions] = useState([]);

  const [selectedPage, setSelectedPage] = useState(null);

  const [title, setTitle] = useState("");
  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [saving, setSaving] = useState(false);
  const [loadingVersions, setLoadingVersions] = useState(false);

  const [showTrash, setShowTrash] = useState(false);
  const [showVersions, setShowVersions] = useState(false);
  const [showAI, setShowAI] = useState(false);
  const [showComments, setShowComments] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [showMembers, setShowMembers] = useState(false);

  const saveTimer = useRef(null);

  const closeSidePanels = () => {
    setShowAI(false);
    setShowComments(false);
    setShowInviteModal(false);
    setShowMembers(false);
  };

  const editor = useEditor({
    extensions: [StarterKit],
    content: "",

    onUpdate: ({ editor }) => {
      if (!selectedPage) {
        return;
      }

      scheduleAutoSave(title, editor.getHTML());
    },
  });

  useEffect(() => {
    const loadPages = async () => {
      try {
        const data = await getWorkspacePages(workspaceId);

        setPages(data);

        if (data.length > 0) {
          await handleSelectPage(data[0]);
        }
      } catch (error) {
        toast.error(error.response?.data?.detail || "Unable to load pages");
      } finally {
        setLoading(false);
      }
    };

    loadPages();
  }, [workspaceId]);

  useEffect(() => {
    return () => {
      if (saveTimer.current) {
        clearTimeout(saveTimer.current);
      }
    };
  }, []);

  const filteredPages = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return pages;
    }

    return pages.filter((page) => page.title.toLowerCase().includes(query));
  }, [pages, search]);

  const scheduleAutoSave = (newTitle, newContent) => {
    if (!selectedPage) {
      return;
    }

    if (saveTimer.current) {
      clearTimeout(saveTimer.current);
    }

    saveTimer.current = setTimeout(async () => {
      setSaving(true);

      try {
        const updatedPage = await updatePage(selectedPage.id, {
          title: newTitle.trim() || "Untitled",
          content: newContent,
        });

        setSelectedPage(updatedPage);

        setPages((current) =>
          current.map((page) =>
            page.id === updatedPage.id ? updatedPage : page,
          ),
        );
      } catch (error) {
        console.error(error);

        toast.error(error.response?.data?.detail || "Auto-save failed");
      } finally {
        setSaving(false);
      }
    }, 900);
  };

  const handleSelectPage = async (page) => {
    if (saveTimer.current) {
      clearTimeout(saveTimer.current);
    }

    try {
      const openedPage = await openPage(page.id);

      setSelectedPage(openedPage);

      setTitle(openedPage.title);

      setShowTrash(false);
      setShowVersions(false);

      closeSidePanels();

      setPages((current) =>
        current.map((item) => (item.id === openedPage.id ? openedPage : item)),
      );

      if (editor) {
        editor.commands.setContent(openedPage.content || "");
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to open page");
    }
  };

  const handleTitleChange = (event) => {
    const newTitle = event.target.value;

    setTitle(newTitle);

    scheduleAutoSave(newTitle, editor?.getHTML() || "");
  };

  const handleCreateRootPage = async () => {
    setCreating(true);

    try {
      const newPage = await createPage(workspaceId, "Untitled", null);

      setPages((current) => [...current, newPage]);

      await handleSelectPage(newPage);

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

      await handleSelectPage(newPage);

      toast.success("Nested page created");
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Unable to create nested page",
      );
    } finally {
      setCreating(false);
    }
  };

  const handleDeletePage = async () => {
    if (!selectedPage) {
      return;
    }

    try {
      const deletedPage = await deletePage(selectedPage.id);

      setPages((current) =>
        current.filter((page) => page.id !== deletedPage.id),
      );

      setSelectedPage(null);
      setTitle("");

      editor?.commands.clearContent();

      setShowVersions(false);

      closeSidePanels();

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
      setShowVersions(false);

      closeSidePanels();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to load trash");
    }
  };

  const handleRestorePage = async (pageId) => {
    try {
      const restoredPage = await restorePage(pageId);

      setTrash((current) => current.filter((page) => page.id !== pageId));

      setPages((current) => [...current, restoredPage]);

      toast.success("Page restored");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to restore page");
    }
  };

  const handleToggleFavorite = async () => {
    if (!selectedPage) {
      return;
    }

    try {
      const updatedPage = selectedPage.is_favorite
        ? await unfavoritePage(selectedPage.id)
        : await favoritePage(selectedPage.id);

      setSelectedPage(updatedPage);

      setPages((current) =>
        current.map((page) =>
          page.id === updatedPage.id ? updatedPage : page,
        ),
      );

      toast.success(
        updatedPage.is_favorite
          ? "Added to favorites"
          : "Removed from favorites",
      );
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to update favorite");
    }
  };

  const handleOpenVersions = async () => {
    if (!selectedPage) {
      return;
    }

    setLoadingVersions(true);

    try {
      const data = await getPageVersions(selectedPage.id);

      setVersions(data);

      setShowVersions(true);
      setShowTrash(false);

      closeSidePanels();
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Unable to load version history",
      );
    } finally {
      setLoadingVersions(false);
    }
  };

  const handleRestoreVersion = async (versionId) => {
    if (!selectedPage) {
      return;
    }

    try {
      const restored = await restorePageVersion(selectedPage.id, versionId);

      setSelectedPage(restored);

      setTitle(restored.title);

      editor?.commands.setContent(restored.content || "");

      setPages((current) =>
        current.map((page) => (page.id === restored.id ? restored : page)),
      );

      toast.success("Previous version restored");

      const refreshedVersions = await getPageVersions(restored.id);

      setVersions(refreshedVersions);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to restore version");
    }
  };

  const handleOpenAI = () => {
    setShowComments(false);
    setShowInviteModal(false);
    setShowMembers(false);

    setShowAI(true);
  };

  const handleOpenComments = () => {
    setShowAI(false);
    setShowInviteModal(false);
    setShowMembers(false);

    setShowComments(true);
  };

  const handleOpenShare = () => {
    setShowAI(false);
    setShowComments(false);
    setShowMembers(false);

    setShowInviteModal(true);
  };

  const handleOpenMembers = () => {
    setShowAI(false);
    setShowComments(false);
    setShowInviteModal(false);

    setShowMembers(true);
  };

  const renderPageTree = (parentId = null, level = 0) => {
    const children = filteredPages.filter(
      (page) => page.parent_page_id === parentId,
    );

    return children.map((page) => (
      <div key={page.id}>
        <div
          className={
            selectedPage?.id === page.id ? "page-row active" : "page-row"
          }
          style={{
            paddingLeft: `${8 + level * 14}px`,
          }}
        >
          <button
            type="button"
            className="page-select-button"
            onClick={() => handleSelectPage(page)}
          >
            <span className="page-icon">▤</span>

            <span className="page-title">{page.title}</span>

            {page.is_favorite && <span className="page-favorite-star">★</span>}
          </button>

          <button
            type="button"
            className="child-page-button"
            onClick={() => handleCreateChildPage(page.id)}
            title="Add nested page"
          >
            +
          </button>
        </div>

        {renderPageTree(page.id, level + 1)}
      </div>
    ));
  };

  return (
    <div className="workspace-shell">
      <aside className="workspace-sidebar">
        <div className="workspace-brand">
          <div className="workspace-logo">N</div>

          <div>
            <strong>NoteSpace</strong>

            <span>Knowledge workspace</span>
          </div>
        </div>

        <Link to="/dashboard" className="workspace-back-link">
          ← Back to dashboard
        </Link>

        <div className="workspace-search">
          <span>⌕</span>

          <input
            type="text"
            placeholder="Search pages..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>

        <div className="workspace-sidebar-header">
          <span>Pages</span>

          <button
            type="button"
            onClick={handleCreateRootPage}
            disabled={creating}
          >
            +
          </button>
        </div>

        <div className="workspace-page-tree">
          {loading ? (
            <div className="page-tree-message">Loading pages...</div>
          ) : filteredPages.length === 0 ? (
            <div className="page-tree-message">
              {search ? "No matching pages" : "No pages yet"}
            </div>
          ) : (
            renderPageTree()
          )}
        </div>

        <div className="workspace-sidebar-footer">
          <button
            type="button"
            onClick={handleOpenTrash}
            className={
              showTrash
                ? "sidebar-footer-button active"
                : "sidebar-footer-button"
            }
          >
            <span>♲</span>
            Trash
          </button>

          <button
            type="button"
            className="sidebar-footer-button"
            onClick={handleOpenMembers}
          >
            <span>👥</span>
            Members
          </button>

          <button type="button" className="sidebar-footer-button">
            <span>⚙</span>
            Workspace settings
          </button>
        </div>
      </aside>

      <main className="workspace-main">
        <header className="workspace-topbar">
          <div className="workspace-breadcrumb">
            <span>Workspace</span>

            <span>/</span>

            <strong>
              {showTrash
                ? "Trash"
                : showVersions
                  ? "Version History"
                  : selectedPage?.title || "No page selected"}
            </strong>
          </div>

          <div className="workspace-actions">
            {!showTrash && selectedPage && (
              <>
                <span
                  className={
                    saving ? "save-indicator saving" : "save-indicator"
                  }
                >
                  <span />

                  {saving ? "Saving..." : "Saved"}
                </span>

                <button
                  type="button"
                  className={
                    selectedPage.is_favorite
                      ? "favorite-button active"
                      : "favorite-button"
                  }
                  onClick={handleToggleFavorite}
                  title={
                    selectedPage.is_favorite
                      ? "Remove from favorites"
                      : "Add to favorites"
                  }
                >
                  {selectedPage.is_favorite ? "★" : "☆"}
                </button>

                <button
                  type="button"
                  className="workspace-secondary-button"
                  onClick={handleOpenAI}
                >
                  ✦ Ask AI
                </button>

                <button
                  type="button"
                  className="workspace-secondary-button"
                  onClick={handleOpenComments}
                >
                  Comments
                </button>

                <button
                  type="button"
                  className="workspace-secondary-button"
                  onClick={handleOpenVersions}
                >
                  History
                </button>

                <button
                  type="button"
                  className="workspace-secondary-button"
                  onClick={handleOpenShare}
                >
                  Share
                </button>

                <button
                  type="button"
                  className="workspace-secondary-button"
                  onClick={handleOpenMembers}
                >
                  Members
                </button>

                <button type="button" className="workspace-more-button">
                  •••
                </button>
              </>
            )}
          </div>
        </header>

        {showTrash ? (
          <section className="premium-trash-view">
            <div className="trash-header">
              <span className="section-eyebrow">Deleted pages</span>

              <h1>Trash</h1>

              <p>
                Restore pages that were previously removed from this workspace.
              </p>
            </div>

            {trash.length === 0 ? (
              <div className="trash-empty-state">
                <div>♲</div>

                <h3>Trash is empty</h3>

                <p>Deleted pages will appear here.</p>
              </div>
            ) : (
              <div className="premium-trash-list">
                {trash.map((page) => (
                  <div className="premium-trash-item" key={page.id}>
                    <div className="trash-page-info">
                      <div className="trash-page-icon">▤</div>

                      <div>
                        <strong>{page.title}</strong>

                        <span>
                          {page.deleted_at
                            ? `Deleted ${new Date(
                                page.deleted_at,
                              ).toLocaleString()}`
                            : "Deleted page"}
                        </span>
                      </div>
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
          </section>
        ) : showVersions && selectedPage ? (
          <section className="version-history-view">
            <div className="version-history-header">
              <div>
                <span className="section-eyebrow">Page history</span>

                <h1>Version History</h1>

                <p>Review and restore previous versions of this page.</p>
              </div>

              <button type="button" onClick={() => setShowVersions(false)}>
                Back to editor
              </button>
            </div>

            {loadingVersions ? (
              <div className="version-message">Loading versions...</div>
            ) : versions.length === 0 ? (
              <div className="version-message">No previous versions yet.</div>
            ) : (
              <div className="version-list">
                {versions.map((version, index) => (
                  <div className="version-card" key={version.id}>
                    <div>
                      <strong>Version {versions.length - index}</strong>

                      <span>
                        {version.created_at
                          ? new Date(version.created_at).toLocaleString()
                          : "Saved version"}
                      </span>
                    </div>

                    <button
                      type="button"
                      onClick={() => handleRestoreVersion(version.id)}
                    >
                      Restore
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>
        ) : !selectedPage ? (
          <section className="premium-editor-empty">
            <div className="editor-empty-icon">N</div>

            <h1>Start building your knowledge base</h1>

            <p>
              Create a page and begin organizing notes, documentation, and
              ideas.
            </p>

            <button type="button" onClick={handleCreateRootPage}>
              + Create page
            </button>
          </section>
        ) : (
          <section className="premium-editor">
            <div className="editor-document-header">
              <span className="editor-page-label">DOCUMENT</span>

              <input
                className="premium-editor-title"
                value={title}
                onChange={handleTitleChange}
                placeholder="Untitled"
              />

              <div className="editor-metadata">
                <span>
                  Last updated{" "}
                  {selectedPage.updated_at
                    ? new Date(selectedPage.updated_at).toLocaleString()
                    : "recently"}
                </span>

                <span>•</span>

                <span>Auto-save enabled</span>

                {selectedPage.is_favorite && (
                  <>
                    <span>•</span>

                    <span className="favorite-metadata">★ Favorite</span>
                  </>
                )}
              </div>
            </div>

            {editor && (
              <div className="premium-editor-toolbar">
                <div className="toolbar-group">
                  <button
                    type="button"
                    className={editor.isActive("bold") ? "active" : ""}
                    onClick={() => editor.chain().focus().toggleBold().run()}
                  >
                    B
                  </button>

                  <button
                    type="button"
                    className={editor.isActive("italic") ? "active" : ""}
                    onClick={() => editor.chain().focus().toggleItalic().run()}
                  >
                    I
                  </button>
                </div>

                <div className="toolbar-divider" />

                <div className="toolbar-group">
                  <button
                    type="button"
                    className={
                      editor.isActive("heading", {
                        level: 1,
                      })
                        ? "active"
                        : ""
                    }
                    onClick={() =>
                      editor
                        .chain()
                        .focus()
                        .toggleHeading({
                          level: 1,
                        })
                        .run()
                    }
                  >
                    H1
                  </button>

                  <button
                    type="button"
                    className={
                      editor.isActive("heading", {
                        level: 2,
                      })
                        ? "active"
                        : ""
                    }
                    onClick={() =>
                      editor
                        .chain()
                        .focus()
                        .toggleHeading({
                          level: 2,
                        })
                        .run()
                    }
                  >
                    H2
                  </button>
                </div>

                <div className="toolbar-divider" />

                <div className="toolbar-group">
                  <button
                    type="button"
                    className={editor.isActive("bulletList") ? "active" : ""}
                    onClick={() =>
                      editor.chain().focus().toggleBulletList().run()
                    }
                  >
                    List
                  </button>

                  <button
                    type="button"
                    className={editor.isActive("blockquote") ? "active" : ""}
                    onClick={() =>
                      editor.chain().focus().toggleBlockquote().run()
                    }
                  >
                    Quote
                  </button>

                  <button
                    type="button"
                    className={editor.isActive("codeBlock") ? "active" : ""}
                    onClick={() =>
                      editor.chain().focus().toggleCodeBlock().run()
                    }
                  >
                    Code
                  </button>
                </div>

                <div className="toolbar-spacer" />

                <button
                  type="button"
                  className="danger-toolbar-button"
                  onClick={handleDeletePage}
                >
                  Delete
                </button>
              </div>
            )}

            <EditorContent editor={editor} className="premium-rich-editor" />
          </section>
        )}
      </main>

      <AIAssistant
        open={showAI}
        onClose={() => setShowAI(false)}
        editor={editor}
        pageTitle={title}
      />

      <CommentsPanel
        open={showComments}
        onClose={() => setShowComments(false)}
        pageId={selectedPage?.id}
        currentUserId={user?.id}
      />

      <InviteMembersModal
        open={showInviteModal}
        onClose={() => setShowInviteModal(false)}
        workspaceId={workspaceId}
      />

      <WorkspaceMembersPanel
        open={showMembers}
        onClose={() => setShowMembers(false)}
        workspaceId={workspaceId}
        currentUserId={user?.id}
      />
    </div>
  );
}

export default Workspace;
