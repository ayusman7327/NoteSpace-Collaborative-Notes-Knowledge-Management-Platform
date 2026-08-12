import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import {
  createComment,
  deleteComment,
  getPageComments,
  reopenComment,
  resolveComment,
  updateComment,
} from "../api/comments";

import "./CommentsPanel.css";

function CommentsPanel({ open, onClose, pageId, currentUserId }) {
  const [comments, setComments] = useState([]);
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [editingId, setEditingId] = useState(null);
  const [editingContent, setEditingContent] = useState("");

  useEffect(() => {
    if (!open || !pageId) {
      return;
    }

    const loadComments = async () => {
      setLoading(true);

      try {
        const data = await getPageComments(pageId);
        setComments(data);
      } catch (error) {
        toast.error(error.response?.data?.detail || "Unable to load comments");
      } finally {
        setLoading(false);
      }
    };

    loadComments();
  }, [open, pageId]);

  const handleCreateComment = async (event) => {
    event.preventDefault();

    const cleanedContent = content.trim();

    if (!cleanedContent) {
      toast.error("Write a comment first");
      return;
    }

    setSubmitting(true);

    try {
      const newComment = await createComment(pageId, cleanedContent);

      setComments((current) => [newComment, ...current]);

      setContent("");

      toast.success("Comment added");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to add comment");
    } finally {
      setSubmitting(false);
    }
  };

  const handleStartEdit = (comment) => {
    setEditingId(comment.id);
    setEditingContent(comment.content);
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditingContent("");
  };

  const handleSaveEdit = async (commentId) => {
    const cleanedContent = editingContent.trim();

    if (!cleanedContent) {
      toast.error("Comment cannot be empty");
      return;
    }

    try {
      const updated = await updateComment(commentId, cleanedContent);

      setComments((current) =>
        current.map((comment) =>
          comment.id === updated.id ? updated : comment,
        ),
      );

      setEditingId(null);
      setEditingContent("");

      toast.success("Comment updated");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to update comment");
    }
  };

  const handleResolve = async (commentId) => {
    try {
      const updated = await resolveComment(commentId);

      setComments((current) =>
        current.map((comment) =>
          comment.id === updated.id ? updated : comment,
        ),
      );

      toast.success("Comment resolved");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to resolve comment");
    }
  };

  const handleReopen = async (commentId) => {
    try {
      const updated = await reopenComment(commentId);

      setComments((current) =>
        current.map((comment) =>
          comment.id === updated.id ? updated : comment,
        ),
      );

      toast.success("Comment reopened");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to reopen comment");
    }
  };

  const handleDelete = async (commentId) => {
    try {
      await deleteComment(commentId);

      setComments((current) =>
        current.filter((comment) => comment.id !== commentId),
      );

      toast.success("Comment deleted");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to delete comment");
    }
  };

  if (!open) {
    return null;
  }

  return (
    <aside className="comments-panel">
      <div className="comments-header">
        <div>
          <strong>Comments</strong>
          <span>
            {comments.length} discussion
            {comments.length === 1 ? "" : "s"}
          </span>
        </div>

        <button
          type="button"
          className="comments-close-button"
          onClick={onClose}
        >
          ×
        </button>
      </div>

      <div className="comments-body">
        <form className="comment-create-form" onSubmit={handleCreateComment}>
          <textarea
            placeholder="Add a comment..."
            value={content}
            onChange={(event) => setContent(event.target.value)}
            maxLength={5000}
          />

          <div className="comment-create-footer">
            <span>{content.length}/5000</span>

            <button type="submit" disabled={submitting}>
              {submitting ? "Posting..." : "Comment"}
            </button>
          </div>
        </form>

        {loading ? (
          <div className="comments-message">Loading comments...</div>
        ) : comments.length === 0 ? (
          <div className="comments-empty">
            <div>💬</div>

            <h3>No comments yet</h3>

            <p>Start a discussion about this page.</p>
          </div>
        ) : (
          <div className="comments-list">
            {comments.map((comment) => {
              const isOwner = Number(comment.user_id) === Number(currentUserId);

              return (
                <article
                  key={comment.id}
                  className={
                    comment.is_resolved
                      ? "comment-card resolved"
                      : "comment-card"
                  }
                >
                  <div className="comment-card-header">
                    <div className="comment-avatar">
                      {String(comment.user_id).slice(-2)}
                    </div>

                    <div className="comment-author">
                      <strong>
                        {isOwner ? "You" : `User ${comment.user_id}`}
                      </strong>

                      <span>
                        {comment.created_at
                          ? new Date(comment.created_at).toLocaleString()
                          : "Recently"}
                      </span>
                    </div>

                    {comment.is_resolved && (
                      <span className="resolved-badge">Resolved</span>
                    )}
                  </div>

                  {editingId === comment.id ? (
                    <div className="comment-edit-area">
                      <textarea
                        value={editingContent}
                        onChange={(event) =>
                          setEditingContent(event.target.value)
                        }
                      />

                      <div className="comment-edit-actions">
                        <button type="button" onClick={handleCancelEdit}>
                          Cancel
                        </button>

                        <button
                          type="button"
                          className="primary"
                          onClick={() => handleSaveEdit(comment.id)}
                        >
                          Save
                        </button>
                      </div>
                    </div>
                  ) : (
                    <p className="comment-content">{comment.content}</p>
                  )}

                  <div className="comment-actions">
                    {comment.is_resolved ? (
                      <button
                        type="button"
                        onClick={() => handleReopen(comment.id)}
                      >
                        Reopen
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={() => handleResolve(comment.id)}
                      >
                        Resolve
                      </button>
                    )}

                    {isOwner && (
                      <>
                        <button
                          type="button"
                          onClick={() => handleStartEdit(comment)}
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          className="danger"
                          onClick={() => handleDelete(comment.id)}
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </div>
    </aside>
  );
}

export default CommentsPanel;
