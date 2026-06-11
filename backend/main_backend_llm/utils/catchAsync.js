/**
 * Wraps an async express handler so you don't need try/catch.
 * Usage: router.get('/', catchAsync(async (req, res) => { ... }))
 */
const catchAsync = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

module.exports = catchAsync;
