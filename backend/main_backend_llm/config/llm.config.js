const llmConfig = {
  provider: process.env.LLM_PROVIDER || "anthropic",

  anthropic: {
    model: process.env.ANTHROPIC_MODEL || "claude-sonnet-4-20250514",
    maxTokens: 2048,
  },

  openai: {
    model: process.env.OPENAI_MODEL || "gpt-4o",
    maxTokens: 2048,
  },

  getSystemPrompt() {
    const name = process.env.AI_NAME || "OmniMind";
    const persona =
      process.env.AI_PERSONA ||
      `You are ${name}, a highly intelligent AI assistant. You are helpful, thoughtful, and concise.`;
    return persona;
  },
};

module.exports = llmConfig;
