const path = require('path');

const config = require('./config');

const dir = {};

dir.project = path.join(__dirname, '..');
dir.scripts = path.join(__dirname, 'scripts');
dir.tmp = path.join(dir.project, 'tmp');
dir.data = path.join(dir.project, 'data', 'problem');

if (config.judger.sandbox_rootfs.startsWith('/')) {
	dir.chroot = config.judger.sandbox_rootfs;
} else {
	dir.chroot = path.join(dir.project, config.judger.sandbox_rootfs);
}

module.exports = dir;
