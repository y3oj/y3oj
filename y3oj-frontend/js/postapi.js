(function () {
	const $ = mdui.$;
	const data = window.postapi_data;
	let is_first_request = true;
	let viewer_lastline = null;
	let viewer_line_counter = 0;

	function viewerUpdateState(state) {
		if (state == 'default') {
			$('#postapi-viewer').css('background', '#F5F5F5');
		}
		if (state == 'waiting') {
			$('#postapi-viewer').css('background', '#FFFDE7');
			$('#postapi-viewer').css('color', '#F57F17');
		}
		if (state == 'success') {
			$('#postapi-viewer').css('background', '#E8F5E9');
			$('#postapi-viewer').css('color', '#1B5E20');
		}
		if (state == 'warning') {
			$('#postapi-viewer').css('background', '#FFF3E0');
			$('#postapi-viewer').css('color', '#E65100');
		}
		if (state == 'error') {
			$('#postapi-viewer').css('background', '#FFCDD2');
			$('#postapi-viewer').css('color', '#B71C1C');
		}
	}

	function viewerPushLine(line) {
		viewer_lastline = line;
		viewer_line_counter += 1;

		const $line = document.createElement('pre');
		$line.classList = ['postapi-viewer-line'];
		$line.innerHTML = line;

		const $viewer = document.getElementById('postapi-viewer');
		$viewer.appendChild($line);
		$viewer.scrollTop = $viewer.scrollHeight; // scroll to bottom
	}

	function viewerWrite(source) {
		for (const line of source.split('\n')) {
			viewerPushLine(line);
		}
	}

	$('#postapi-submit').on('click', function () {
		$('#postapi-submit').attr('disabled', true);
		const form_data = {};
		for (const name of Object.keys(data.args)) {
			form_data[name] = $('#postapi-data-' + name).val();
		}

		if (is_first_request) {
			is_first_request = false;
			$('#postapi-viewer').empty();
		} else {
			viewerPushLine('\n');
		}

		const current_date = new Date();
		const current_month = current_date.getMonth() + 1;
		const current_time = current_date.getFullYear() + '-' + current_month + '-' + current_date.getDate() + ' ' + current_date.getHours() + ':' + current_date.getMinutes() + ':' + current_date.getSeconds();
		viewerUpdateState('waiting');
		viewerPushLine('[' + current_time + '] [POST] ' + data.api);
		viewerWrite(JSON.stringify(form_data, null, 2));

		$.ajax({
			method: 'POST',
			url: data.api,
			data: form_data,
			success: function (res_plain) {
				const res = JSON.parse(res_plain);
				if (res.code) {
					viewerUpdateState('warning');
				} else {
					viewerUpdateState('success');
				};
				viewerPushLine('[' + current_time + '] [RECEIVE]');
				viewerWrite(JSON.stringify(res, null, 2));
				$('#postapi-submit').removeAttr('disabled');
			},
			error: function (error) {
				console.error(error);
				viewerUpdateState('error');
				viewerPushLine('[' + current_time + '] [ERROR]');
				viewerWrite(JSON.stringify(error, null, 2));
				$('#postapi-submit').removeAttr('disabled');
			}
		});
	});

	$(function () {
		viewerUpdateState('default');
		viewerWrite('This is the log terminal, click the POST button above to send a request...');

		for (const [name, label] of Object.entries(data.args)) {
			$('#postapi-form').append('<div class="mdui-textfield"><label class="mdui-textfield-label">' + label + '</label><input id="postapi-data-' + name + '"class="mdui-textfield-input" type="text"/></div>');
		}
	});
})();