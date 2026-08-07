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
