const path = require('path');

const dir = {};

dir.project = path.join(__dirname, '..');
dir.scripts = path.join(__dirname, 'scripts');
dir.tmp = path.join(dir.project, 'tmp');
dir.data = path.join(dir.project, 'data', 'problem');

module.exports = dir;
