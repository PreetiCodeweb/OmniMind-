const Conversation = require("../models/conversation.model");

// GET /api/conversations  — list all for current user
const getConversations = async (req, res, next) => {
  try {
    const conversations = await Conversation.find({
      user: req.user.id,
      isArchived: false,
    })
      .select("title isPinned totalTokens createdAt updatedAt")
      .sort({ isPinned: -1, updatedAt: -1 });

    res.json({ success: true, conversations });
  } catch (err) {
    next(err);
  }
};

// GET /api/conversations/:id  — get full conversation with messages
const getConversation = async (req, res, next) => {
  try {
    const conversation = await Conversation.findOne({
      _id: req.params.id,
      user: req.user.id,
    });

    if (!conversation) {
      return res
        .status(404)
        .json({ success: false, message: "Conversation not found" });
    }

    res.json({ success: true, conversation });
  } catch (err) {
    next(err);
  }
};

// DELETE /api/conversations/:id  — delete a conversation
const deleteConversation = async (req, res, next) => {
  try {
    const conversation = await Conversation.findOneAndDelete({
      _id: req.params.id,
      user: req.user.id,
    });

    if (!conversation) {
      return res
        .status(404)
        .json({ success: false, message: "Conversation not found" });
    }

    res.json({ success: true, message: "Conversation deleted" });
  } catch (err) {
    next(err);
  }
};

// DELETE /api/conversations  — delete ALL conversations for user
const deleteAllConversations = async (req, res, next) => {
  try {
    await Conversation.deleteMany({ user: req.user.id });
    res.json({ success: true, message: "All conversations deleted" });
  } catch (err) {
    next(err);
  }
};

// PATCH /api/conversations/:id/title  — rename a conversation
const updateTitle = async (req, res, next) => {
  try {
    const { title } = req.body;
    if (!title || !title.trim()) {
      return res
        .status(400)
        .json({ success: false, message: "Title is required" });
    }

    const conversation = await Conversation.findOneAndUpdate(
      { _id: req.params.id, user: req.user.id },
      { title: title.trim() },
      { new: true }
    );

    if (!conversation) {
      return res
        .status(404)
        .json({ success: false, message: "Conversation not found" });
    }

    res.json({ success: true, conversation });
  } catch (err) {
    next(err);
  }
};

// PATCH /api/conversations/:id/pin  — toggle pin
const togglePin = async (req, res, next) => {
  try {
    const conversation = await Conversation.findOne({
      _id: req.params.id,
      user: req.user.id,
    });

    if (!conversation) {
      return res
        .status(404)
        .json({ success: false, message: "Conversation not found" });
    }

    conversation.isPinned = !conversation.isPinned;
    await conversation.save();

    res.json({ success: true, isPinned: conversation.isPinned });
  } catch (err) {
    next(err);
  }
};

// PATCH /api/conversations/:id/archive  — toggle archive
const toggleArchive = async (req, res, next) => {
  try {
    const conversation = await Conversation.findOne({
      _id: req.params.id,
      user: req.user.id,
    });

    if (!conversation) {
      return res
        .status(404)
        .json({ success: false, message: "Conversation not found" });
    }

    conversation.isArchived = !conversation.isArchived;
    await conversation.save();

    res.json({ success: true, isArchived: conversation.isArchived });
  } catch (err) {
    next(err);
  }
};

module.exports = {
  getConversations,
  getConversation,
  deleteConversation,
  deleteAllConversations,
  updateTitle,
  togglePin,
  toggleArchive,
};
