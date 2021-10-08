const fs = require('fs').promises;
const path = require('path');
const YAML = require('yaml');

const base_dir = require('./dir');
const base_config = require('./config').problem.defaults;

const sandbox = require('./simple-sandbox/lib');
/*
	export enum SandboxStatus {
		Unknown = 0,
		OK = 1,
		TimeLimitExceeded = 2,
		MemoryLimitExceeded = 3,
		RuntimeError = 4,
		Cancelled = 5,
		OutputLimitExceeded = 6
	};
*/

let testlib_source = null;
let sandbox_source = null;


function randomString(len) {
	const charset = '0123456789qazxswedcvfrtgbnhyujmkiolpPLOIKMJUYHNBGTRFVCDEWSXZAQ';
	let result = '';
	for (let i = 0; i < len; i++) {
		result += charset[Math.floor(Math.random() * len)];
	}
	return result;
}

async function readLibFile(relative_path) {
	return (await fs.readFile(path.join(base_dir.scripts, relative_path))).toString();
}

function compressResult(result) {
	for (const detail of result.details) {
		if (detail.status == result.status) { delete detail.status; }
		if (detail.time == result.time) { delete detail.time; }
		if (detail.memory == result.memory) { delete detail.memory; }
	}
	if (result.time == 0) delete result.time;
	if (result.memory == 0) delete result.memory;
	return result;
}

function decompressResult(result) {
	if (!result.time) result.time = 0;
	if (!result.memory) result.memory = 0;
	for (const detail of result.details) {
		if (!detail.status) { detail.status = result.status; }
		if (!detail.time) { detail.time = result.time; }
		if (!detail.memory) { detail.memory = result.memory; }
	}
	return result;
}

function mergeResult(a, b) {
	if (a.status == 'Accepted') { a.status = b.status; }
	if (b.time > a.time) { a.time = b.time; }
	if (b.memory > a.memory) { a.memory = b.memory; }
	for (const detail of b.details) { a.details.push(detail); }
	return a;
}

async function runInSandbox(parameters, options) {
	const { hashkey, config, dir } = options;

	const result = {
		status: null,
		details: [{}],
		time: 0,
		memory: 0,
	};

	try {
		const sandbox_options = {
			hostname: "y3oj-judge-server",
			chroot: dir.chroot,
			time: config.time_limit,
			memory: 1024 * 1024 * config.memory_limit,
			mounts: [{
				src: dir.working,
				dst: "/sandbox",
				limit: 10240 * 1024
			}],
			workingDirectory: "/sandbox/working",
			// executable: "/usr/bin/bash",
			// parameters: ["/usr/bin/bash"],
			// stdin: "/dev/stdin",
			// stdout: "/dev/stdout",
			// stderr: "/dev/stderr",
			executable: "/usr/bin/python",
			parameters: ["/usr/bin/python", ...parameters],
			stdin: path.join(dir.working, 'result/' + hashkey + '.stdin'),
			stdout: path.join(dir.working, 'result/' + hashkey + '.stdout'),
			stderr: path.join(dir.working, 'result/' + hashkey + '.stderr'),
			environments: ['PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'],
			mountProc: true,
			redirectBeforeChroot: true,
			process: 30,
			user: sandbox.getUidAndGidInSandbox(dir.chroot, "y3oj"),
			cgroup: "asdf",
		};
		// console.log(sandbox_options);

		const sandboxed_process = sandbox.startSandbox(sandbox_options);
		const sandbox_result = await sandboxed_process.waitForStop();
		result.time = (sandbox_result.time / 1000 / 1000).toFixed(0);       // ms
		result.memory = (sandbox_result.memory / 1024 / 1024).toFixed(0);   // MiB

		if (sandbox_result.status === 0 || sandbox_result.status === 5 || sandbox_result === 6) {
			result.status = 'SystemError';
			result.details[0]['message'] = '[y3oj-judger] Sandbox returned with status: ' + (sandbox_result.status === 0 ?
				'Unknown' : (sandbox_result.status === 5 ?
					'Cancelled' :
					'OutputLimitExceeded'));
		} else if (sandbox_result.status >= 2 && sandbox_result.status <= 4) {
			result.time = result.memory = 0;
			switch (sandbox_result.status) {
				case 2: { result.status = 'TimeLimitExceeded'; break; }
				case 3: { result.status = 'MemoryLimitExceeded'; break; }
				case 4: { result.status = 'RuntimeError'; break; }
			}
		} else {
			result.details = await options.parser();
			result.status = 'Accepted';

			for (const detail of result.details) {
				if (detail.status && detail.status != 'Accepted' && result.status == 'Accepted') {
					result.status = detail.status;
				}
			}
		}

	} catch (error) {
		result.status = 'SystemError';
		result.details = [{ message: '[y3oj-judger] Sandbox ran into an error: ' + error.toString() }];
	}

	return decompressResult(result);
}


async function run(task) {
	if (testlib_source === null) {
		testlib_source = await readLibFile('testlib.py');
		sandbox_source = await readLibFile('sandbox.py');
	}

	const { id, problem, code } = task;
	const dir = JSON.parse(JSON.stringify(base_dir));

	dir.problem = path.join(dir.data, problem);
	dir.working = path.join(dir.tmp, String(id));

	const readFile = async (relative_path) => (await fs.readFile(path.join(dir.problem, relative_path))).toString();
	const writeFile = async (relative_path, content) => await fs.writeFile(path.join(dir.working, relative_path), content);
	const makeDirs = async (relative_path) => await fs.mkdir(path.join(dir.working, relative_path), { recursive: true });

	const config = {
		...base_config,
		...YAML.parse(await readFile('config.yml')),
	};

	await makeDirs('.');
	await makeDirs('working');
	await makeDirs('result');
	await writeFile('working/sol.py', code);

	const hashkey = randomString(16);
	writeFile('result/' + hashkey + '.stdin', '');
	writeFile('result/' + hashkey + '.stdout', '');
	writeFile('result/' + hashkey + '.stderr', '');

	let result;

	if (config.judge.startsWith('testlib')) {
		const parseTestlibResponse = async () => {
			const stdout = (await fs.readFile(path.join(dir.working, 'result/' + hashkey + '.stdout'))).toString();
			const stdout_lines = stdout.split('\n');

			try {
				if (!stdout_lines[0].startsWith('[SUCCESS]')) {
					throw new Error('`stdout_lines[0]` not starts with `[SUCCESS]`');
				}
				const details = JSON.parse(stdout_lines[0].slice(10));
				for (let i = 1; i < details.length; i++) {
					details[i].time = -1;
					details[i].memory = -1;
				}
				return details;

			} catch (error) {
				return [{
					status: 'SystemError',
					message: '[y3oj-judger] Testlib parser ran into an error: ' + error.toString(),
				}];
			}
		}

		if (config.judge == 'testlib-multi') {
			await Promise.all([
				writeFile('working/judge.py', await readFile('judge.py')),
				writeFile('working/testlib.py', testlib_source),
				writeFile('working/sandbox.py', sandbox_source),
			]);
			result = await runInSandbox(
				['judge.py'],
				{ hashkey, config, dir, parser: parseTestlibResponse }
			);
		}
	}

	compressResult(result);
	console.log('[judge]', hashkey, task, result);
	return result;
}


module.exports = {
	run,
};

if (require.main === module) {
	const terminationHandler = () => {
		process.exit(1);
	};

	process.on('SIGTERM', terminationHandler);
	process.on('SIGINT', terminationHandler);

	run({
		id: 0,
		user: 'memset0',
		problem: 'a_plus_b',
		code: 'a,b=map(int,input().split());print(a+b)'
	});
}