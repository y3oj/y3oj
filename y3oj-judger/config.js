const fs = require('fs');
const path = require('path');
const YAML = require('yaml');

function load(basename) {
	const filepath = path.join(__dirname, '..', basename + '.yml');
	const plaintext = fs.readFileSync(filepath).toString();
	return YAML.parse(plaintext);
};

function merge(obj_a, obj_b) {
	if (obj_a === null || obj_a.constructor !== Object || obj_b.constructor !== Object) {
		return JSON.parse(JSON.stringify(obj_b));
	}
	let obj = JSON.parse(JSON.stringify(obj_a));
	for (const k in obj_b) {
		if (Object.keys(obj_a).includes(k)) {
			obj[k] = merge(obj_a[k], obj_b[k]);
		} else {
			obj[k] = JSON.parse(JSON.stringify(obj_b[k]));
		}
	}
	// console.log('merge\n\t' + JSON.stringify(obj_a) + '\n\t' + JSON.stringify(obj_b) + '\n\t' + JSON.stringify(obj));
	return obj;
};


module.exports = merge(load('config.sample'), load('config'));
