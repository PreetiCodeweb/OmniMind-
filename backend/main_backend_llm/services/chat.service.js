const Conversation = require("../models/conversation.model");
const { sendMessage, streamMessage } = require("./llm.service");

/**
 * Get or create a conversation, append user message,
 * get LLM response, save everything, and return.
 */
const chat = async (userId, userMessage, conversationId = null) => {
  // 1. Load or create conversation
  let conversation;
  if (conversationId) {
    conversation = await Conversation.findOne({
      _id: conversationId,
      user: userId,
    });
    if (!conversation) throw new Error("Conversation not found");
  } else {
    conversation = new Conversation({ user: userId, messages: [] });
  }

  // 2. Append user message
  conversation.messages.push({ role: "user", content: userMessage });

  // 3. Build messages array for LLM (only role + content)
  const llmMessages = conversation.messages.map((m) => ({
    role: m.role === "assistant" ? "assistant" : "user",
    content: m.content,
  }));

  // 4. Call LLM
  const { content, inputTokens, outputTokens } = await sendMessage(llmMessages);

  // 5. Append assistant response
  conversation.messages.push({
    role: "assistant",
    content,
    tokens: outputTokens,
  });

  // 6. Update token count & auto-title
  conversation.totalTokens += inputTokens + outputTokens;
  if (conversation.messages.length === 2) {
    conversation.generateTitle();
  }

  await conversation.save();

  return {
    conversationId: conversation._id,
    title: conversation.title,
    message: {
      role: "assistant",
      content,
      tokens: outputTokens,
    },
  };
};

/**
 * Streaming version — writes SSE chunks via res, then saves to DB.
 */
const chatStream = async (userId, userMessage, conversationId, res) => {
  // 1. Load or create conversation
  let conversation;
  if (conversationId) {
    conversation = await Conversation.findOne({
      _id: conversationId,
      user: userId,
    });
    if (!conversation) {
      res.write(`data: ${JSON.stringify({ error: "Conversation not found" })}\n\n`);
      res.end();
      return;
    }
  } else {
    conversation = new Conversation({ user: userId, messages: [] });
  }

  // 2. Append user message
  conversation.messages.push({ role: "user", content: userMessage });

  // 3. Build LLM messages
  const llmMessages = conversation.messages.map((m) => ({
    role: m.role === "assistant" ? "assistant" : "user",
    content: m.content,
  }));

  // 4. Setup SSE headers
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.setHeader("X-Accel-Buffering", "no"); // Disable nginx buffering

  // Send conversation ID immediately so client can track it
  res.write(
    `data: ${JSON.stringify({
      type: "start",
      conversationId: conversation._id,
    })}\n\n`
  );

  // 5. Stream LLM response
  const { content, inputTokens, outputTokens } = await streamMessage(
    llmMessages,
    (chunk) => {
      res.write(`data: ${JSON.stringify({ type: "chunk", content: chunk })}\n\n`);
    }
  );

  // 6. Send done event
  res.write(`data: ${JSON.stringify({ type: "done" })}\n\n`);
  res.end();

  // 7. Save to DB
  conversation.messages.push({
    role: "assistant",
    content,
    tokens: outputTokens,
  });
  conversation.totalTokens += inputTokens + outputTokens;
  if (conversation.messages.length === 2) {
    conversation.generateTitle();
  }
  await conversation.save();
};

module.exports = { chat, chatStream };
