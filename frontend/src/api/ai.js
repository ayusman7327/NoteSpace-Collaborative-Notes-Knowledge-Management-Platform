import api from "./axios";

export async function askAI(prompt) {
  const response = await api.post("/ai/generate", {
    prompt,
  });

  return response.data.response;
}

export async function askWorkspaceAI(workspaceId, question) {
  const response = await api.post(`/ai/workspace/${workspaceId}`, {
    question,
  });

  return response.data.response;
}
