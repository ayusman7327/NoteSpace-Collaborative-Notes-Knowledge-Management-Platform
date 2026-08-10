import api from "./axios";

export async function getWorkspacePages(workspaceId) {
  const response = await api.get(`/pages/workspace/${workspaceId}`);

  return response.data;
}

export async function createPage(
  workspaceId,
  title = "Untitled",
  parentPageId = null,
) {
  const response = await api.post("/pages", {
    workspace_id: Number(workspaceId),
    parent_page_id: parentPageId,
    title,
    content: "",
  });

  return response.data;
}

export async function getPage(pageId) {
  const response = await api.get(`/pages/${pageId}`);

  return response.data;
}

export async function updatePage(pageId, data) {
  const response = await api.patch(`/pages/${pageId}`, data);

  return response.data;
}

export async function deletePage(pageId) {
  const response = await api.delete(`/pages/${pageId}`);

  return response.data;
}

export async function getTrash(workspaceId) {
  const response = await api.get(`/pages/workspace/${workspaceId}/trash`);

  return response.data;
}

export async function restorePage(pageId) {
  const response = await api.post(`/pages/${pageId}/restore`);

  return response.data;
}

export async function favoritePage(pageId) {
  const response = await api.post(`/pages/${pageId}/favorite`);

  return response.data;
}

export async function unfavoritePage(pageId) {
  const response = await api.delete(`/pages/${pageId}/favorite`);

  return response.data;
}

export async function getFavoritePages(workspaceId) {
  const response = await api.get(`/pages/workspace/${workspaceId}/favorites`);

  return response.data;
}

export async function openPage(pageId) {
  const response = await api.post(`/pages/${pageId}/open`);

  return response.data;
}

export async function getRecentPages(workspaceId) {
  const response = await api.get(`/pages/workspace/${workspaceId}/recent`);

  return response.data;
}

export async function searchWorkspacePages(workspaceId, query) {
  const response = await api.get(`/pages/workspace/${workspaceId}/search`, {
    params: {
      q: query,
    },
  });

  return response.data;
}

export async function getPageVersions(pageId) {
  const response = await api.get(`/pages/${pageId}/versions`);

  return response.data;
}

export async function restorePageVersion(pageId, versionId) {
  const response = await api.post(
    `/pages/${pageId}/versions/${versionId}/restore`,
  );

  return response.data;
}
