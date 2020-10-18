$('#spinner_overlay').hide();


$('#configSubmit').click(function(e) {
	e.preventDefault();
	$('#spinner_overlay').show();

	$.ajax({
		type: 'POST',
		url: '/get-quiz/',

		data: {
			"category": $('#categorySelect').val(),
			"difficulty": $('#difficultySelect').val(),
			"csrfmiddlewaretoken": $('#quizConfigCSRF').val(),
		},

		success: function(response) {
			$('#spinner_overlay').hide();
			let data = JSON.parse(response, null);
			if (data != null){
				console.log(data);
			}
		},

		error: function(jqXHR) {
			$('#spinner_overlay').hide();

			if (jqXHR.responseJSON) {
				alert("Status: " + jqXHR.status + " " + jqXHR.statusText
		      +"\nPlease try again later.");
			}
		}
	});
});


function scrollToDiv(id, time, offset) {
	$('html, body').animate({
	  scrollTop: $(`#${id}`).offset().top - offset
	}, time);
}


function demoLoginScroll() {
	scrollToDiv('sampleLoginDiv', 1000, null);
}
