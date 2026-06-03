// API Service - Frontend integration with backend

const API_BASE = "http://localhost:8000/api";

// ============ USER ENDPOINTS ============

export const createUser = async (name, email) => {
  try {
    const response = await fetch(`${API_BASE}/users/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email }),
    });
    return await response.json();
  } catch (error) {
    console.error("Error creating user:", error);
    throw error;
  }
};

export const getUser = async (userId) => {
  try {
    const response = await fetch(`${API_BASE}/users/${userId}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching user:", error);
    throw error;
  }
};

export const updateUser = async (userId, userData) => {
  try {
    const response = await fetch(`${API_BASE}/users/${userId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    return await response.json();
  } catch (error) {
    console.error("Error updating user:", error);
    throw error;
  }
};

// ============ MEMORY ENDPOINTS ============

export const createMemory = async (userId, memoryData) => {
  try {
    const response = await fetch(`${API_BASE}/memories/?user_id=${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(memoryData),
    });
    return await response.json();
  } catch (error) {
    console.error("Error creating memory:", error);
    throw error;
  }
};

export const getUserMemories = async (userId, skip = 0, limit = 100) => {
  try {
    const response = await fetch(
      `${API_BASE}/memories/${userId}?skip=${skip}&limit=${limit}`
    );
    return await response.json();
  } catch (error) {
    console.error("Error fetching memories:", error);
    throw error;
  }
};

export const getMemory = async (userId, memoryId) => {
  try {
    const response = await fetch(`${API_BASE}/memories/${userId}/${memoryId}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching memory:", error);
    throw error;
  }
};

export const updateMemory = async (userId, memoryId, memoryData) => {
  try {
    const response = await fetch(
      `${API_BASE}/memories/${userId}/${memoryId}`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(memoryData),
      }
    );
    return await response.json();
  } catch (error) {
    console.error("Error updating memory:", error);
    throw error;
  }
};

export const deleteMemory = async (userId, memoryId) => {
  try {
    const response = await fetch(
      `${API_BASE}/memories/${userId}/${memoryId}`,
      { method: "DELETE" }
    );
    return await response.json();
  } catch (error) {
    console.error("Error deleting memory:", error);
    throw error;
  }
};

// ============ CHAT ENDPOINTS ============

export const saveChatMessage = async (userId, messageData) => {
  try {
    const response = await fetch(`${API_BASE}/chat/${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(messageData),
    });
    return await response.json();
  } catch (error) {
    console.error("Error saving chat message:", error);
    throw error;
  }
};

export const getChatHistory = async (userId, limit = 50) => {
  try {
    const response = await fetch(`${API_BASE}/chat/${userId}?limit=${limit}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching chat history:", error);
    throw error;
  }
};

// ============ KNOWLEDGE GRAPH ENDPOINTS ============

export const createNode = async (userId, nodeData) => {
  try {
    const response = await fetch(`${API_BASE}/knowledge/nodes/${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(nodeData),
    });
    return await response.json();
  } catch (error) {
    console.error("Error creating node:", error);
    throw error;
  }
};

export const getUserNodes = async (userId) => {
  try {
    const response = await fetch(`${API_BASE}/knowledge/nodes/${userId}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching nodes:", error);
    throw error;
  }
};

export const deleteNode = async (userId, nodeId) => {
  try {
    const response = await fetch(
      `${API_BASE}/knowledge/nodes/${userId}/${nodeId}`,
      { method: "DELETE" }
    );
    return await response.json();
  } catch (error) {
    console.error("Error deleting node:", error);
    throw error;
  }
};

// ============ ACTIVITY ENDPOINTS ============

export const logActivity = async (userId, activityData) => {
  try {
    const response = await fetch(`${API_BASE}/activity/${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(activityData),
    });
    return await response.json();
  } catch (error) {
    console.error("Error logging activity:", error);
    throw error;
  }
};

export const getUserActivity = async (userId, limit = 20) => {
  try {
    const response = await fetch(
      `${API_BASE}/activity/${userId}?limit=${limit}`
    );
    return await response.json();
  } catch (error) {
    console.error("Error fetching activity:", error);
    throw error;
  }
};

// ============ AI ROUTER ENDPOINTS ============

export const createRouterRule = async (userId, routerData) => {
  try {
    const response = await fetch(`${API_BASE}/router/${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(routerData),
    });
    return await response.json();
  } catch (error) {
    console.error("Error creating routing rule:", error);
    throw error;
  }
};

export const getRouterRules = async (userId) => {
  try {
    const response = await fetch(`${API_BASE}/router/${userId}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching router rules:", error);
    throw error;
  }
};

// ============ NOTIFICATIONS ENDPOINTS ============

export const createNotification = async (userId, notificationData) => {
  try {
    const response = await fetch(`${API_BASE}/notifications/${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(notificationData),
    });
    return await response.json();
  } catch (error) {
    console.error("Error creating notification:", error);
    throw error;
  }
};

export const getNotifications = async (userId, unreadOnly = false) => {
  try {
    const response = await fetch(
      `${API_BASE}/notifications/${userId}?unread_only=${unreadOnly}`
    );
    return await response.json();
  } catch (error) {
    console.error("Error fetching notifications:", error);
    throw error;
  }
};

export const markNotificationAsRead = async (userId, notificationId) => {
  try {
    const response = await fetch(
      `${API_BASE}/notifications/${userId}/${notificationId}/read`,
      { method: "PUT" }
    );
    return await response.json();
  } catch (error) {
    console.error("Error marking notification as read:", error);
    throw error;
  }
};

// ============ STATS ENDPOINTS ============

export const getUserStats = async (userId) => {
  try {
    const response = await fetch(`${API_BASE}/stats/${userId}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching user stats:", error);
    throw error;
  }
};

// ============ HEALTH CHECK ============

export const healthCheck = async () => {
  try {
    const response = await fetch("http://localhost:8000/health");
    return await response.json();
  } catch (error) {
    console.error("Backend is not reachable:", error);
    return { status: "offline" };
  }
};
