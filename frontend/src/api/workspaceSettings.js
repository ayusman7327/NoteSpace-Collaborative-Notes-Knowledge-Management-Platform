import api from "./axios";

export async function getWorkspace(workspaceId) {
  const response = await api.get(`/workspaces/${workspaceId}`);

  return response.data;
}

export async function updateWorkspace(workspaceId, data) {
  const response = await api.patch(`/workspaces/${workspaceId}`, data);

  return response.data;
}

export async function deleteWorkspace(workspaceId) {
  const response = await api.delete(`/workspaces/${workspaceId}`);

  return response.data;
}
