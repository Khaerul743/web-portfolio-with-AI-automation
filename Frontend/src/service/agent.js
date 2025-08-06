import agentAxios from "../config/axios";

export async function sendAgentMessage(message) {
  try {
    const response = await agentAxios.post("", { message });
    return response.data;
  } catch (error) {
    // Optionally handle error more gracefully
    return { error: error.response?.data || error.message };
  }
}
