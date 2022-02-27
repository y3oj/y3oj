(function () {
	const $ = mdui.JQ || mdui.$;
	const config = window.$$autorefresh;
	const isArrayLike = (x) => (x && typeof x.length === 'number');

	if (!config.elementId || !config.interval) {
		alert('[autorefresh] ERR: Wrongly configured!')
	}
	if (!isArrayLike(config.elementId)) {
		config.elementId = [config.elementId];
	}

	setInterval(() => {
		if ((!window.hidden || config.activeWhenHidden) && (!config.checker || config.checker())) {
			$.ajax({
				method: 'GET',
				url: window.location.pathname,
				success: (html) => {
					console.log('[autorefresh]', 'refreshed!');

					// const $page = $('<div id="html">' + html + '</div>');   // --> Illegal, but the next line works.
					const $page = $('<div id="html">' + html + '</div>');

					for (const elementId of config.elementId) {
						const $old = $('#' + elementId);
						const $new = $page.find('#' + elementId);
						$old.html($new.html());
					}

					if (config.callback) {
						const response = config.callback(html, $page);
						console.log('[autorefresh]', 'callback returned', response);
					}
				}
			})
		};
	}, 5000);
})();