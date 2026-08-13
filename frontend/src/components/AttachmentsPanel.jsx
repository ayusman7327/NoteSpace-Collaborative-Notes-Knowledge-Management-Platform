import { useEffect, useRef, useState } from "react";
import toast from "react-hot-toast";

import {
  deletePageAttachment,
  getPageAttachments,
  uploadPageAttachment,
} from "../api/attachments";

import "./AttachmentsPanel.css";

function AttachmentsPanel({ open, onClose, pageId }) {
  const [attachments, setAttachments] = useState([]);

  const [loading, setLoading] = useState(false);

  const [uploading, setUploading] = useState(false);

  const [dragging, setDragging] = useState(false);

  const fileInputRef = useRef(null);

  useEffect(() => {
    if (!open || !pageId) {
      return;
    }

    const loadAttachments = async () => {
      setLoading(true);

      try {
        const data = await getPageAttachments(pageId);

        setAttachments(data);
      } catch (error) {
        toast.error(
          error.response?.data?.detail || "Unable to load attachments",
        );
      } finally {
        setLoading(false);
      }
    };

    loadAttachments();
  }, [open, pageId]);

  const uploadFile = async (file) => {
    if (!file) {
      return;
    }

    setUploading(true);

    try {
      const newAttachment = await uploadPageAttachment(pageId, file);

      setAttachments((current) => [newAttachment, ...current]);

      toast.success("File uploaded");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to upload file");
    } finally {
      setUploading(false);
    }
  };

  const handleFileSelect = async (event) => {
    const file = event.target.files?.[0];

    await uploadFile(file);

    event.target.value = "";
  };

  const handleDragOver = (event) => {
    event.preventDefault();

    setDragging(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();

    setDragging(false);
  };

  const handleDrop = async (event) => {
    event.preventDefault();

    setDragging(false);

    const file = event.dataTransfer.files?.[0];

    await uploadFile(file);
  };

  const handleDelete = async (attachmentId) => {
    try {
      await deletePageAttachment(attachmentId);

      setAttachments((current) =>
        current.filter((attachment) => attachment.id !== attachmentId),
      );

      toast.success("Attachment deleted");
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Unable to delete attachment",
      );
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) {
      return "0 KB";
    }

    if (bytes < 1024) {
      return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const getFileIcon = (fileType) => {
    if (fileType?.startsWith("image/")) {
      return "IMG";
    }

    if (fileType === "application/pdf") {
      return "PDF";
    }

    if (fileType?.includes("word")) {
      return "DOC";
    }

    if (fileType === "text/markdown") {
      return "MD";
    }

    if (fileType === "text/plain") {
      return "TXT";
    }

    return "FILE";
  };

  const getAttachmentUrl = (attachment) => {
    const baseUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";

    return `${baseUrl}${attachment.file_url}`;
  };

  if (!open) {
    return null;
  }

  return (
    <aside className="attachments-panel">
      <div className="attachments-header">
        <div>
          <span>PAGE FILES</span>

          <h2>Attachments</h2>

          <p>Add images, PDFs, documents and supporting files to this page.</p>
        </div>

        <button
          type="button"
          className="attachments-close-button"
          onClick={onClose}
        >
          ×
        </button>
      </div>

      <div className="attachments-body">
        <input
          ref={fileInputRef}
          type="file"
          hidden
          accept=".png,.jpg,.jpeg,.webp,.pdf,.txt,.md,.docx"
          onChange={handleFileSelect}
        />

        <div
          className={
            dragging ? "attachment-drop-zone dragging" : "attachment-drop-zone"
          }
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => {
            if (!uploading) {
              fileInputRef.current?.click();
            }
          }}
        >
          <div className="drop-zone-icon">+</div>

          <div className="drop-zone-content">
            <strong>{uploading ? "Uploading..." : "Drop files here"}</strong>

            <span>or click to browse</span>

            <small>PNG, JPG, WEBP, PDF, DOCX, TXT or Markdown</small>
          </div>
        </div>

        <div className="attachment-limit">Maximum file size: 10 MB</div>

        <div className="attachments-section-heading">
          <div>
            <h3>Page files</h3>

            <p>Files attached to this document.</p>
          </div>

          <span>{attachments.length}</span>
        </div>

        {loading ? (
          <div className="attachments-message">Loading attachments...</div>
        ) : attachments.length === 0 ? (
          <div className="attachments-empty">
            <div>📎</div>

            <h3>No attachments yet</h3>

            <p>Drag a file here or click the upload area above.</p>
          </div>
        ) : (
          <div className="attachments-list">
            {attachments.map((attachment) => (
              <div className="attachment-card" key={attachment.id}>
                <div className="attachment-icon">
                  {getFileIcon(attachment.file_type)}
                </div>

                <div className="attachment-info">
                  <strong title={attachment.file_name}>
                    {attachment.file_name}
                  </strong>

                  <div>
                    <span>{formatFileSize(attachment.file_size)}</span>

                    <span>•</span>

                    <span>
                      {attachment.created_at
                        ? new Date(attachment.created_at).toLocaleDateString()
                        : "Recently"}
                    </span>
                  </div>
                </div>

                <div className="attachment-actions">
                  <a
                    href={getAttachmentUrl(attachment)}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Open
                  </a>

                  <button
                    type="button"
                    onClick={() => handleDelete(attachment.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </aside>
  );
}

export default AttachmentsPanel;
