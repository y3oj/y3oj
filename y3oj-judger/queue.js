const judger = require('./judger');

class Task {
	constructor(data) {
		this.id = data.id;
		this.user = data.user;
		this.problem = data.problem;
		this.code = data.code;
		this.callback = data.callback;
	}
};

class TaskQueue {
	size() {
		return this.tasks.length;
	}

	pop() {
		return this.tasks.shift();
	}

	push(task) {
		this.tasks.push(task);
		if (!this.busy) {
			judge()
		}
	}

	constructor() {
		this.busy = false;
		this.tasks = [];
	}
}

const q = new TaskQueue();

async function judge() {
	if (q.busy || !q.size()) {
		return;
	}

	q.busy = true;
	while (q.size()) {
		const task = q.pop();
		let res;

		try {
			res = { type: 'judge-result', id: task.id, code: 0, data: await judger.run(task) };
		} catch (error) {
			res = { type: 'judge-result', id: task.id, code: 1, error };
		}

		task.callback(res);
	}
	q.busy = false;
}

function push(data) {
	return new Promise((resolve) => {
		q.push(new Task({ ...data, callback: resolve }));
	});
}

module.exports = {
	Task,
	TaskQueue,
	judge,
	push,
};
