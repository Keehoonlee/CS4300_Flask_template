jQuery(document).ready(function(){
	$(".dropdown-menu li a").click(function(){
		$('#city').val($(this).attr("data-value"));
	  $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
	  $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
	});


	var neighborhoods = [ "East End", "Hazelwood","Hill District","Homewood", "Lawrenceville", "North Side", "Oakland", "South Side", "Squirrel Hill", "West End"];
	var availableTags = [
	      "ActionScript",
	      "AppleScript",
	      "Asp",
	      "BASIC",
	      "C",
	      "C++",
	      "Clojure",
	      "COBOL",
	      "ColdFusion",
	      "Erlang",
	      "Fortran",
	      "Groovy",
	      "Haskell",
	      "Java",
	      "JavaScript",
	      "Lisp",
	      "Perl",
	      "PHP",
	      "Python",
	      "Ruby",
	      "Scala",
	      "Scheme"
	    ];
	$('#neighborhood').autocomplete({
		source: availableTags
	});
});
