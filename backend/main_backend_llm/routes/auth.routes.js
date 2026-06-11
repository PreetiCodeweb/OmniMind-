const express = require("express");
const router = express.Router();
const { register, login, getMe, updateMe } = require("../controllers/auth.controller");
const { protect } = require("../middleware/auth.middleware");
const { authLimiter } = require("../middleware/rateLimiter");
const {
  validate,
  registerRules,
  loginRules,
} = require("../middleware/validate.middleware");

// Public
router.post("/register", authLimiter, registerRules, validate, register);
router.post("/login", authLimiter, loginRules, validate, login);

// Protected
router.get("/me", protect, getMe);
router.patch("/me", protect, updateMe);

module.exports = router;
