const YAML = require('yaml');
const fs = require('fs').promises;

const dir = require('./dir');

async function load(basename) {
	const filepath = path.join(dir.project, basename + '.yml');
	const plaintext = (await fs.readFile(filepath)).toString();
	return YAML.parse(plaintext);
};

function merge(obj_a, obj_b) {
	obj = JSON.parse(JSON.stringify(obj_a));
	for (const k in Object.keys(obj_b)) {
		if (Object.keys(obj_a).includes(k)) {
			obj[k] = merge(obj_a[k], obj_b[k]);
		} else {
			obj[k] = JSON.parse(JSON.stringify(obj_b[k]));
		}
	}
	return obj;
};

module.exports = merge(load('config.sample'), load('config'));
