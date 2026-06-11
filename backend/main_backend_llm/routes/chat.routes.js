const express = require("express");
const router = express.Router();
const { sendMessage, streamMessage } = require("../controllers/chat.controller");
const { protect } = require("../middleware/auth.middleware");
const { chatLimiter } = require("../middleware/rateLimiter");
const { validate, chatRules } = require("../middleware/validate.middleware");

// All chat routes require auth
router.use(protect);
router.use(chatLimiter);

// Standard response
router.post("/", chatRules, validate, sendMessage);

// Streaming response (SSE)
router.post("/stream", chatRules, validate, streamMessage);

module.exports = router;
