"use server";
import {
  sendMessage,
  pollMessage
} from "@/libs/api";


export const sendMessageAction = async (data) => {
  try {
    const response = await sendMessage(data);

    if (response.error) {
      return { "error": response.error };
    }

    return response;
  } catch (error) {
    console.error("Error sending message:", error);
    return { error: error.message || "Error sending message" };
  }
};

export const pollMessageAction = async (client_id, polling_type) => {
  try {
    const response = await pollMessage(client_id, polling_type);
    if (response.error) {
      return { "error": response.error };
    }
    return response;
  } catch (error) {
    console.error("Error polling message:", error);
    return { error: error.message || "Error polling message" };
  }
};