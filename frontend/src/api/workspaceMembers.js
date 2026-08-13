import api from "./axios";

export async function getWorkspaceMembers(workspaceId) {
  const response = await api.get(`/workspace-members/workspace/${workspaceId}`);

  return response.data;
}

export async function updateWorkspaceMemberRole(workspaceId, memberId, role) {
  const response = await api.patch(
    `/workspace-members/workspace/${workspaceId}/member/${memberId}`,
    {
      role,
    },
  );

  return response.data;
}

export async function removeWorkspaceMember(workspaceId, memberId) {
  const response = await api.delete(
    `/workspace-members/workspace/${workspaceId}/member/${memberId}`,
  );

  return response.data;
}

export async function leaveWorkspace(workspaceId) {
  const response = await api.post(
    `/workspace-members/workspace/${workspaceId}/leave`,
  );

  return response.data;
}
