const { chat, chatStream } = require("../services/chat.service");

// POST /api/chat  —  standard (non-streaming) response
const sendMessage = async (req, res, next) => {
  try {
    const { message, conversationId } = req.body;

    if (!message || !message.trim()) {
      return res
        .status(400)
        .json({ success: false, message: "Message cannot be empty" });
    }

    const result = await chat(req.user.id, message.trim(), conversationId || null);

    res.json({
      success: true,
      conversationId: result.conversationId,
      title: result.title,
      message: result.message,
    });
  } catch (err) {
    next(err);
  }
};

// POST /api/chat/stream  —  SSE streaming response
const streamMessage = async (req, res, next) => {
  try {
    const { message, conversationId } = req.body;

    if (!message || !message.trim()) {
      return res
        .status(400)
        .json({ success: false, message: "Message cannot be empty" });
    }

    await chatStream(
      req.user.id,
      message.trim(),
      conversationId || null,
      res
    );
  } catch (err) {
    // If headers not sent yet, return JSON error
    if (!res.headersSent) {
      next(err);
    } else {
      res.write(`data: ${JSON.stringify({ type: "error", error: err.message })}\n\n`);
      res.end();
    }
  }
};

module.exports = { sendMessage, streamMessage };
