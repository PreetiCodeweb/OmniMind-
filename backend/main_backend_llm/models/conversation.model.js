const mongoose = require("mongoose");

const messageSchema = new mongoose.Schema(
  {
    role: {
      type: String,
      enum: ["user", "assistant", "system"],
      required: true,
    },
    content: {
      type: String,
      required: true,
    },
    tokens: {
      type: Number,
      default: 0,
    },
  },
  { timestamps: true }
);

const conversationSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
    title: {
      type: String,
      default: "New Chat",
      maxlength: 200,
    },
    messages: [messageSchema],
    model: {
      type: String,
      default: "",
    },
    totalTokens: {
      type: Number,
      default: 0,
    },
    isArchived: {
      type: Boolean,
      default: false,
    },
    isPinned: {
      type: Boolean,
      default: false,
    },
  },
  { timestamps: true }
);

// Auto-generate title from first user message
conversationSchema.methods.generateTitle = function () {
  const firstUserMsg = this.messages.find((m) => m.role === "user");
  if (firstUserMsg) {
    this.title =
      firstUserMsg.content.length > 60
        ? firstUserMsg.content.substring(0, 60) + "..."
        : firstUserMsg.content;
  }
};

module.exports = mongoose.model("Conversation", conversationSchema);
