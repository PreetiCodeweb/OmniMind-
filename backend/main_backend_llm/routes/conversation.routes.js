const express = require("express");
const router = express.Router();
const {
  getConversations,
  getConversation,
  deleteConversation,
  deleteAllConversations,
  updateTitle,
  togglePin,
  toggleArchive,
} = require("../controllers/conversation.controller");
const { protect } = require("../middleware/auth.middleware");

// All routes protected
router.use(protect);

router.get("/", getConversations);
router.delete("/", deleteAllConversations);

router.get("/:id", getConversation);
router.delete("/:id", deleteConversation);
router.patch("/:id/title", updateTitle);
router.patch("/:id/pin", togglePin);
router.patch("/:id/archive", toggleArchive);

module.exports = router;
