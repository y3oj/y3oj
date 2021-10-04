const fs = require('fs').promises;
const path = require('path');
const YAML = require('yaml');

const sandbox = require('../simple-sandbox/lib');
const base_dir = require('./dir');
const base_config = require('./config').problem.defaults;

let testlib_source = null;

const terminationHandler = () => {
	process.exit(1);
};

process.on('SIGTERM', terminationHandler);
process.on('SIGINT', terminationHandler);

async function readLibFile(relative_path) {
	return (await fs.readFile(path.join(base_dir.scripts, relative_path))).toString();
}

function parseTestlibResponse() {

}

async function runInSandbox(config, dir) {
	try {
		const options = {
			hostname: "y3oj-judge-server",
			chroot: dir.chroot,
			time: config.time_limit,
			memory: 1024 * 1024 * config.memory_limit,
			mounts: [{
				src: dir.working,
				dst: "/sandbox/working",
				limit: 10240 * 1024
			}],
			workingDirectory: "/sandbox/working",
			executable: "/usr/bin/python",
			parameters: ["/usr/bin/python", '-c', '"print(\'hello\')"'],
			environments: ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
			stdin: "/dev/stdin",
			stdout: "/dev/stdout",
			stderr: "/dev/stdout",
			mountProc: true,
			redirectBeforeChroot: true,
			process: 30,
			user: sandbox.getUidAndGidInSandbox(dir.chroot, "y3oj"),
			cgroup: "asdf",
		};
		console.log(options);
		const sandboxed_process = sandbox.startSandbox(options);
		const result = await sandboxed_process.waitForStop();
		console.log("Your sandbox finished!" + JSON.stringify(result));
	} catch (ex) {
		console.log("Whooops! " + ex.toString());
	}
}

async function run(task) {
	if (testlib_source === null) {
		testlib_source = await readLibFile('testlib.py');
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
	await writeFile('sol.py', code);

	if (config.judge == 'testlib-multi') {
		await Promise.all([
			writeFile('judge.py', await readFile('judge.py')),
			writeFile('testlib.py', testlib_source),
		]);
		await runInSandbox(config, dir);
	}
}

module.exports = {
	run,
};

if (require.main === module) {
	run({
		id: 0,
		user: 'memset0',
		problem: 'a_plus_b',
		code: 'a,b=map(int,input().split());print(a+b)'
	});
}