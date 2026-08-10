import api from "./axios";

export async function searchWorkspacePages(workspaceId, query) {
  const response = await api.get(`/pages/workspace/${workspaceId}/search`, {
    params: {
      q: query,
    },
  });

  return response.data;
}
