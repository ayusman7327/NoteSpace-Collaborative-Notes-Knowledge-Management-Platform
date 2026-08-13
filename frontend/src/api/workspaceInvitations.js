import api from "./axios";

export async function createWorkspaceInvitation(workspaceId, email, role) {
  const response = await api.post(
    `/workspace-invitations/workspace/${workspaceId}`,
    {
      email,
      role,
    },
  );

  return response.data;
}

export async function getWorkspaceInvitations(workspaceId) {
  const response = await api.get(
    `/workspace-invitations/workspace/${workspaceId}`,
  );

  return response.data;
}

export async function getMyInvitations() {
  const response = await api.get("/workspace-invitations/my");

  return response.data;
}

export async function acceptWorkspaceInvitation(invitationId) {
  const response = await api.post(
    `/workspace-invitations/${invitationId}/accept`,
  );

  return response.data;
}

export async function rejectWorkspaceInvitation(invitationId) {
  const response = await api.post(
    `/workspace-invitations/${invitationId}/reject`,
  );

  return response.data;
}

export async function cancelWorkspaceInvitation(invitationId) {
  const response = await api.post(
    `/workspace-invitations/${invitationId}/cancel`,
  );

  return response.data;
}
