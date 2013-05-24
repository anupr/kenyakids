$(document).ready(function() {
	$('head', document).append('<link rel="stylesheet" type="text/css" media="screen" href="/site/media/wymeditor/skins/default/screen.css" />');
	$("textarea").wymeditor({
		updateSelector: "input:submit",
		    updateEvent:    "click"    
		    });
    });
