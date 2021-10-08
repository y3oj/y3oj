const fs = require('fs').promises;
const path = require('path');
const assert = require('assert');

const judger = require('../judger');


async function main() {
	const all_status = [
		'Accepted',
		'WrongAnswer',
		'SystemError',
		'TimeLimitExceeded',
		'MemoryLimitExceeded',
	];

	for (const status of all_status) {
		const result = await judger.run({
			id: 0,
			user: 'memset0',
			problem: 'a_plus_b',
			code: (await fs.readFile(path.join(__dirname, 'samples', status + '.py'))).toString(),
		});
		console.log('[y3oj-judger-test]', status, '=>', result.status);
		assert.equal(status, result.status);
	}
}


if (require.main == module) {
	main();
}