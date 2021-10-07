const ws = require('ws');
const chalk = require('chalk');

const config = require('./config');
const queue = require('./queue');

const logger = function () {
	console.log(chalk.cyanBright('[y3oj-judger]'), ...arguments);
}


async function main() {
	const wss = new ws.WebSocketServer({ port: config.judger.port });
	logger('ws server is created at :' + config.judger.port);

	wss.on('connection', function connection(ws) {
		logger('connected!');

		ws.on('message', async (plaintext) => {
			const msg = JSON.parse(plaintext);
			logger(`message TYPE=${msg.type}`);

			if (msg.type == 'submit') {
				const result = await queue.push(msg.data);
				ws.send(JSON.stringify(result));
			}
		});
	});
}

const terminationHandler = () => {
	process.exit(1);
};

process.on('SIGTERM', terminationHandler);
process.on('SIGINT', terminationHandler);

main();
