const ws = require('ws');

const config = require('./config');
const queue = require('./queue');

async function initWebsocketServer(config) {
	return new Promise((resolve) => {
		const wss = new WebSocketServer({ port: config.judger.port });

		wss.on('connection', function connection(ws) {
			resolve(ws);
		});
	});
}

async function main() {
	ws = await initWebsocketServer(config);

	ws.on('message', function on_message(msg) {
		json = JSON.parse(msg);

		if (msg.type == 'submit') {
			ws.send(JSON.stringify(await queue.push(msg.data)));
		}
	});
}

main();
