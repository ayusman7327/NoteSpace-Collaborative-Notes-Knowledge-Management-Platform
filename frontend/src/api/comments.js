import api from "./axios";

export async function getPageComments(pageId) {
  const response = await api.get(`/comments/page/${pageId}`);

  return response.data;
}

export async function createComment(pageId, content) {
  const response = await api.post(`/comments/page/${pageId}`, {
    content,
  });

  return response.data;
}

export async function updateComment(commentId, content) {
  const response = await api.patch(`/comments/${commentId}`, {
    content,
  });

  return response.data;
}

export async function resolveComment(commentId) {
  const response = await api.post(`/comments/${commentId}/resolve`);

  return response.data;
}

export async function reopenComment(commentId) {
  const response = await api.post(`/comments/${commentId}/reopen`);

  return response.data;
}

export async function deleteComment(commentId) {
  const response = await api.delete(`/comments/${commentId}`);

  return response.data;
}
