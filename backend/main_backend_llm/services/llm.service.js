const Anthropic = require("@anthropic-ai/sdk");
const OpenAI = require("openai");
const llmConfig = require("../config/llm.config");

// Lazy-init clients
let anthropicClient = null;
let openaiClient = null;

const getAnthropicClient = () => {
  if (!anthropicClient) {
    anthropicClient = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });
  }
  return anthropicClient;
};

const getOpenAIClient = () => {
  if (!openaiClient) {
    openaiClient = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }
  return openaiClient;
};

/**
 * Send a message to the LLM and get a complete response.
 * @param {Array} messages  - Array of { role, content } objects
 * @param {Object} options  - Optional overrides
 * @returns {Object} { content, inputTokens, outputTokens }
 */
const sendMessage = async (messages, options = {}) => {
  const provider = options.provider || llmConfig.provider;

  if (provider === "anthropic") {
    return sendAnthropic(messages, options);
  } else if (provider === "openai") {
    return sendOpenAI(messages, options);
  } else {
    throw new Error(`Unknown LLM provider: ${provider}`);
  }
};

/**
 * Stream a response from the LLM, calling onChunk for each delta.
 * @param {Array}    messages  - Array of { role, content }
 * @param {Function} onChunk   - Called with each text chunk string
 * @param {Object}   options   - Optional overrides
 * @returns {Object} { content, inputTokens, outputTokens }
 */
const streamMessage = async (messages, onChunk, options = {}) => {
  const provider = options.provider || llmConfig.provider;

  if (provider === "anthropic") {
    return streamAnthropic(messages, onChunk, options);
  } else if (provider === "openai") {
    return streamOpenAI(messages, onChunk, options);
  } else {
    throw new Error(`Unknown LLM provider: ${provider}`);
  }
};

// ─── Anthropic ────────────────────────────────────────────

const sendAnthropic = async (messages, options = {}) => {
  const client = getAnthropicClient();
  const cfg = llmConfig.anthropic;

  // Anthropic takes system separately
  const systemPrompt = options.systemPrompt || llmConfig.getSystemPrompt();
  const filteredMessages = messages.filter((m) => m.role !== "system");

  const response = await client.messages.create({
    model: options.model || cfg.model,
    max_tokens: options.maxTokens || cfg.maxTokens,
    system: systemPrompt,
    messages: filteredMessages,
  });

  return {
    content: response.content[0].text,
    inputTokens: response.usage?.input_tokens || 0,
    outputTokens: response.usage?.output_tokens || 0,
  };
};

const streamAnthropic = async (messages, onChunk, options = {}) => {
  const client = getAnthropicClient();
  const cfg = llmConfig.anthropic;

  const systemPrompt = options.systemPrompt || llmConfig.getSystemPrompt();
  const filteredMessages = messages.filter((m) => m.role !== "system");

  let fullContent = "";
  let inputTokens = 0;
  let outputTokens = 0;

  const stream = client.messages.stream({
    model: options.model || cfg.model,
    max_tokens: options.maxTokens || cfg.maxTokens,
    system: systemPrompt,
    messages: filteredMessages,
  });

  for await (const event of stream) {
    if (
      event.type === "content_block_delta" &&
      event.delta?.type === "text_delta"
    ) {
      const chunk = event.delta.text;
      fullContent += chunk;
      onChunk(chunk);
    }
    if (event.type === "message_delta" && event.usage) {
      outputTokens = event.usage.output_tokens || 0;
    }
    if (event.type === "message_start" && event.message?.usage) {
      inputTokens = event.message.usage.input_tokens || 0;
    }
  }

  return { content: fullContent, inputTokens, outputTokens };
};

// ─── OpenAI ───────────────────────────────────────────────

const sendOpenAI = async (messages, options = {}) => {
  const client = getOpenAIClient();
  const cfg = llmConfig.openai;

  // Inject system prompt if not already there
  const systemPrompt = options.systemPrompt || llmConfig.getSystemPrompt();
  const hasSystem = messages.some((m) => m.role === "system");
  const allMessages = hasSystem
    ? messages
    : [{ role: "system", content: systemPrompt }, ...messages];

  const response = await client.chat.completions.create({
    model: options.model || cfg.model,
    max_tokens: options.maxTokens || cfg.maxTokens,
    messages: allMessages,
  });

  return {
    content: response.choices[0].message.content,
    inputTokens: response.usage?.prompt_tokens || 0,
    outputTokens: response.usage?.completion_tokens || 0,
  };
};

const streamOpenAI = async (messages, onChunk, options = {}) => {
  const client = getOpenAIClient();
  const cfg = llmConfig.openai;

  const systemPrompt = options.systemPrompt || llmConfig.getSystemPrompt();
  const hasSystem = messages.some((m) => m.role === "system");
  const allMessages = hasSystem
    ? messages
    : [{ role: "system", content: systemPrompt }, ...messages];

  let fullContent = "";

  const stream = await client.chat.completions.create({
    model: options.model || cfg.model,
    max_tokens: options.maxTokens || cfg.maxTokens,
    messages: allMessages,
    stream: true,
  });

  for await (const chunk of stream) {
    const delta = chunk.choices[0]?.delta?.content || "";
    if (delta) {
      fullContent += delta;
      onChunk(delta);
    }
  }

  return { content: fullContent, inputTokens: 0, outputTokens: 0 };
};

module.exports = { sendMessage, streamMessage };
