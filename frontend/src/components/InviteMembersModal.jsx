import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import {
  cancelWorkspaceInvitation,
  createWorkspaceInvitation,
  getWorkspaceInvitations,
} from "../api/workspaceInvitations";

import "./InviteMembersModal.css";

function InviteMembersModal({ open, onClose, workspaceId }) {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("viewer");

  const [invitations, setInvitations] = useState([]);

  const [loading, setLoading] = useState(false);

  const [submitting, setSubmitting] = useState(false);

  const loadInvitations = async () => {
    if (!workspaceId) {
      return;
    }

    setLoading(true);

    try {
      const data = await getWorkspaceInvitations(workspaceId);

      setInvitations(data);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to load invitations");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!open) {
      return;
    }

    loadInvitations();
  }, [open, workspaceId]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const cleanedEmail = email.trim().toLowerCase();

    if (!cleanedEmail) {
      toast.error("Enter an email address");

      return;
    }

    setSubmitting(true);

    try {
      const invitation = await createWorkspaceInvitation(
        workspaceId,
        cleanedEmail,
        role,
      );

      setInvitations((current) => [invitation, ...current]);

      setEmail("");
      setRole("viewer");

      toast.success("Invitation created");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to invite member");
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancelInvitation = async (invitationId) => {
    try {
      const updated = await cancelWorkspaceInvitation(invitationId);

      setInvitations((current) =>
        current.map((invitation) =>
          invitation.id === updated.id ? updated : invitation,
        ),
      );

      toast.success("Invitation cancelled");
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Unable to cancel invitation",
      );
    }
  };

  if (!open) {
    return null;
  }

  return (
    <div className="invite-modal-overlay" onMouseDown={onClose}>
      <div
        className="invite-modal"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="invite-modal-header">
          <div>
            <span>COLLABORATION</span>

            <h2>Invite members</h2>

            <p>Invite teammates to collaborate in this workspace.</p>
          </div>

          <button type="button" onClick={onClose}>
            ×
          </button>
        </div>

        <form className="invite-form" onSubmit={handleSubmit}>
          <div className="invite-field">
            <label>Email address</label>

            <input
              type="email"
              placeholder="teammate@example.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </div>

          <div className="invite-field">
            <label>Role</label>

            <select
              value={role}
              onChange={(event) => setRole(event.target.value)}
            >
              <option value="viewer">Viewer</option>

              <option value="editor">Editor</option>
            </select>
          </div>

          <button
            type="submit"
            className="invite-submit-button"
            disabled={submitting}
          >
            {submitting ? "Sending..." : "Send invitation"}
          </button>
        </form>

        <div className="invite-role-info">
          <div>
            <strong>Editor</strong>

            <span>Can create and edit workspace pages.</span>
          </div>

          <div>
            <strong>Viewer</strong>

            <span>Can read workspace content without editing.</span>
          </div>
        </div>

        <div className="invite-list-section">
          <div className="invite-list-heading">
            <div>
              <h3>Invitations</h3>

              <p>Pending and previous invitations.</p>
            </div>

            <span>{invitations.length}</span>
          </div>

          {loading ? (
            <div className="invite-message">Loading invitations...</div>
          ) : invitations.length === 0 ? (
            <div className="invite-empty">
              <div>✉</div>

              <h4>No invitations yet</h4>

              <p>Invite someone using their email address.</p>
            </div>
          ) : (
            <div className="invite-list">
              {invitations.map((invitation) => (
                <div className="invite-item" key={invitation.id}>
                  <div className="invite-avatar">
                    {invitation.email.charAt(0).toUpperCase()}
                  </div>

                  <div className="invite-details">
                    <strong>{invitation.email}</strong>

                    <div>
                      <span>{invitation.role}</span>

                      <span>•</span>

                      <span className={`invite-status ${invitation.status}`}>
                        {invitation.status}
                      </span>
                    </div>
                  </div>

                  {invitation.status === "pending" && (
                    <button
                      type="button"
                      className="cancel-invite-button"
                      onClick={() => handleCancelInvitation(invitation.id)}
                    >
                      Cancel
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default InviteMembersModal;
