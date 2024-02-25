const path = require("path");
const { spawn } = require("child_process");
const fastify = require("fastify")({ logger: false });

const winston = require('winston');

const logger = winston.createLogger({
  level: 'error',
  format: winston.format.simple(),
  transports: [
    new winston.transports.Console(),
  ],
});

fastify.get("/", (request, reply) => {
  return reply.view("/src/pages/index.hbs", {});
});

fastify.post("/", (request, reply) => {
  return reply.view("/src/pages/index.hbs", {});
});

function runPythonScript() {
  const pythonProcess = spawn("python", [
    path.join(__dirname, "thebegin_bot.py"),
    "--port",
    "8080",
  ]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python stdout: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    logger.error(`Python stderr: ${data}`);
  });
}

runPythonScript();

fastify.listen({ port: process.env.PORT, host: "0.0.0.0" }, (err, address) => {
  if (err) {
    logger.error(err);
    process.exit(1);
  }
  console.log(`Your app is listening on ${address}`);
});
