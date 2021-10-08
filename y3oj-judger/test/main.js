const fs = require('fs');
const path = require('path');
const assert = require('assert');

const judger = require('../judger');


async function main() {
	const problem_list = [
		'a-plus-b',
		'intro-bh',
	];

	const status_list = [
		'Accepted',
		'WrongAnswer',
		'SystemError',
		'TimeLimitExceeded',
		'MemoryLimitExceeded',
	];

	for (const problem of problem_list) {
		for (const status of status_list) {
			const filepath = path.join(__dirname, 'problems', problem, 'code', status + '.py');
			if (!fs.existsSync(filepath)) { continue; }

			const result = await judger.run({
				id: 0,
				user: 'memset0',
				problem: problem,
				code: fs.readFileSync(filepath).toString(),
			});
			console.log('[y3oj-judger-test]', status, '=>', result.status);
			assert.equal(status, result.status);
		}
	}
}


if (require.main == module) {
	main();
}