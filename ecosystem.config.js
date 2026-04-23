module.exports = {
  apps: [
    {
      name: "lmsk-scraper",
      script: "main.py",
      interpreter: "uv",
      interpreter_args: "run",
      env: {
        PYTHONUNBUFFERED: "1",
      },
    },
  ],
};
