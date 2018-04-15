jQuery(document).ready(function(){

	// $(window).scroll(function() {
	//     if ($(".navbar").offset().top > 50) {
	//         $(".navbar-fixed-top").addClass("top-nav-collapse");
	//     } else {
	//         $(".navbar-fixed-top").removeClass("top-nav-collapse");
	//     }
	// });

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

		var images = ["demo-pic.jpeg", "demo-pic1.jpeg", "demo-pic2.jpeg"]
		var i = 0;
		var imageHead = document.getElementById("search-slide");
		setInterval(function() {
		      imageHead.style.backgroundImage = "url(" + images[i] + ")";
		      i = i + 1;
		      if (i == images.length) {
		        i =  0;
		      }
		}, 5000);

		$(window).scroll(function () {
		if ($(document).scrollTop() >= 50) {
		$('.navbar').css('background','#37b0e9');
		$('.navbar-collapse').css('background','#37b0e9');

		} else {
		$('.navbar').css('background','transparent');
		$('.navbar-collapse').css('background','transparent');

		}
		});

	});

	//jQuery to collapse the navbar on scroll
	$(window).scroll(function () {
	if ($(document).scrollTop() >= 50) {
	$('.navbar').css('background','#37b0e9');

	} else {
	$('.navbar').css('background','transparent');

	}
	});

	$("#goButton").click(function() {
	    // event.preventDefault();

	    $('html, body').animate({
	        scrollTop: $("#output").offset().top
	    }, 2000);
	});

	//jQuery for page scrolling feature - requires jQuery Easing plugin
	// $(function() {
	//     $('.btn').bind('click', function(event) {
	//         var $anchor = $(this);
	//         $('html, body').stop().animate({
	//             scrollTop: $('.output-container').offset().top
	//         }, 1500, 'easeInOutExpo');
	//         event.preventDefault();
	//     });
	// });
