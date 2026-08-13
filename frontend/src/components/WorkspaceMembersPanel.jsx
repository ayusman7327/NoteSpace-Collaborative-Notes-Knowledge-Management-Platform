import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import {
  getWorkspaceMembers,
  removeWorkspaceMember,
  updateWorkspaceMemberRole,
} from "../api/workspaceMembers";

import "./WorkspaceMembersPanel.css";

function WorkspaceMembersPanel({ open, onClose, workspaceId, currentUserId }) {
  const [members, setMembers] = useState([]);

  const [loading, setLoading] = useState(false);

  const [updatingMemberId, setUpdatingMemberId] = useState(null);

  useEffect(() => {
    if (!open || !workspaceId) {
      return;
    }

    const loadMembers = async () => {
      setLoading(true);

      try {
        const data = await getWorkspaceMembers(workspaceId);

        setMembers(data);
      } catch (error) {
        toast.error(
          error.response?.data?.detail || "Unable to load workspace members",
        );
      } finally {
        setLoading(false);
      }
    };

    loadMembers();
  }, [open, workspaceId]);

  const handleRoleChange = async (member, role) => {
    setUpdatingMemberId(member.id);

    try {
      const updatedMember = await updateWorkspaceMemberRole(
        workspaceId,
        member.id,
        role,
      );

      setMembers((current) =>
        current.map((item) =>
          item.id === updatedMember.id ? updatedMember : item,
        ),
      );

      toast.success("Member role updated");
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Unable to update member role",
      );
    } finally {
      setUpdatingMemberId(null);
    }
  };

  const handleRemoveMember = async (memberId) => {
    try {
      await removeWorkspaceMember(workspaceId, memberId);

      setMembers((current) =>
        current.filter((member) => member.id !== memberId),
      );

      toast.success("Member removed");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to remove member");
    }
  };

  if (!open) {
    return null;
  }

  return (
    <aside className="members-panel">
      <div className="members-panel-header">
        <div>
          <span>COLLABORATION</span>

          <h2>Workspace members</h2>

          <p>Manage people who can access this workspace.</p>
        </div>

        <button type="button" onClick={onClose}>
          ×
        </button>
      </div>

      <div className="members-panel-body">
        <div className="members-summary">
          <div>
            <strong>{members.length}</strong>

            <span>Members</span>
          </div>

          <div>
            <strong>
              {members.filter((member) => member.role === "editor").length}
            </strong>

            <span>Editors</span>
          </div>

          <div>
            <strong>
              {members.filter((member) => member.role === "viewer").length}
            </strong>

            <span>Viewers</span>
          </div>
        </div>

        {loading ? (
          <div className="members-message">Loading members...</div>
        ) : members.length === 0 ? (
          <div className="members-empty">
            <div>👥</div>

            <h3>No members yet</h3>

            <p>Invite teammates using the Share button.</p>
          </div>
        ) : (
          <div className="members-list">
            {members.map((member) => {
              const isCurrentUser =
                Number(member.user_id) === Number(currentUserId);

              return (
                <div className="member-card" key={member.id}>
                  <div className="member-avatar">
                    {String(member.user_id).slice(-2).toUpperCase()}
                  </div>

                  <div className="member-info">
                    <strong>
                      {isCurrentUser ? "You" : `User ${member.user_id}`}
                    </strong>

                    <span>
                      Joined{" "}
                      {member.joined_at
                        ? new Date(member.joined_at).toLocaleDateString()
                        : "recently"}
                    </span>
                  </div>

                  <div className="member-controls">
                    <select
                      value={member.role}
                      disabled={updatingMemberId === member.id}
                      onChange={(event) =>
                        handleRoleChange(member, event.target.value)
                      }
                    >
                      <option value="editor">Editor</option>

                      <option value="viewer">Viewer</option>
                    </select>

                    {!isCurrentUser && (
                      <button
                        type="button"
                        onClick={() => handleRemoveMember(member.id)}
                      >
                        Remove
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </aside>
  );
}

export default WorkspaceMembersPanel;
