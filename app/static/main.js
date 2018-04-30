$(document).ready(function($) {
		// Workaround for bug in mouse item selection
		$.fn.typeahead.Constructor.prototype.blur = function() {
				var that = this;
				setTimeout(function () { that.hide() }, 250);
		};

		$("#neighborhood").typeahead({
				source: function(query, process) {
						return ["Deluxe Bicycle", "Super Deluxe Trampoline", "Super Duper Scooter"];
				}
		});
		$("[data-toggle="tooltip"]").tooltip();
		$("a area").click(function(event){
			event.preventDefault();
			$("#neighborhood").val($(this).attr("title"));
			$("#neighborhood").text($(this).attr("title"));
		})

});
