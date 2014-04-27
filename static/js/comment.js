$(document).ready(function() {
	var base = $(location).attr('href');
	$("#all tbody").children("tr").each(function() {
		$(this).children("td").eq(1).hover(function() {
			var name = $(this).html();
			$(this).tooltipster({
				content: "<p>Fetching...</p>",
				contentAsHTML: true,
				arrow: false,
				theme: 'tooltip',
				interactive: true,
				trigger: 'click',
				functionBefore: function(origin, continueTooltip) {
					continueTooltip();
					if (origin.data('ajax') !== 'cached') {
						$.ajax({
							type: "GET",
							url: "/view/comment/" + name,
							success: function(data) {
								origin.tooltipster('content', data).data('ajax', 'cached');
							}
						});
					}
				}
			});
		});
	});
});
