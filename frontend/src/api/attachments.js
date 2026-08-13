import api from "./axios";

export async function getPageAttachments(pageId) {
  const response = await api.get(`/attachments/page/${pageId}`);

  return response.data;
}

export async function uploadPageAttachment(pageId, file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(`/attachments/page/${pageId}`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

export async function deletePageAttachment(attachmentId) {
  const response = await api.delete(`/attachments/${attachmentId}`);

  return response.data;
}
