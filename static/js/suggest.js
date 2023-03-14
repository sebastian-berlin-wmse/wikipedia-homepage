var ajaxCallTimeout = 5000;
var suggestTimeout = null;
var delay = 500;
var lastSearch = "";
var searchPath = "go";

var $searchField = $( "#search-field" );
var $suggestions = $( ".search-suggestion" );
var $searchSuggestionList = $( "#search-suggestion-list" );
var $searchTerm = $( "#search-term" );

function triggerSuggestLater( lang ) {
	if ( suggestTimeout ) {
		clearTimeout( suggestTimeout ); //kill suggestion timer
	}
	suggestTimeout = setTimeout( searchSuggest, delay, lang );
}

function searchSuggest( language ) {
	var str = $searchField.val();

	if ( str == lastSearch ) {
		return;
	}

	if ( str === "" ) {
		$searchSuggestionList.hide();
	} else {
		$.ajax( "suggest", {
			data: {
				lang: language,
				search: str
			},
			success: function( response ) {
				handleSearchSuggest( str, response, language )
				lastSearch = str;
			},
			timeout: ajaxCallTimeout
		} );
	}
}

function getSearchLink( query, language, provider ) {
	var queryParams = {
		l: language,
		q: query
	};

	if ( typeof provider === "string" ) {
		queryParams.e = provider;
		queryParams.s = "search";
	}

	return searchPath + "?" + $.param( queryParams );
}

function handleSearchSuggest( term, suggestions, language ) {
	$suggestions.hide();
	$searchSuggestionList.show();
	$searchTerm.text( term );

	var i = 0;
	for ( var suggestion of suggestions ) {
		var $element = $suggestions.eq(i);
		$element.text( suggestion );
		$element.attr( "href", getSearchLink( suggestion, language ) )
		if ( suggestion.toLowerCase() === term.toLowerCase() ) {
			$element.addClass( "exact-match" );
		} else {
			$element.removeClass( "exact-match" );
		}
		$element.show();
		i ++;
	}
};

// Navigate the search suggestions with the arrow keys.
$searchSuggestionList.on( "keydown", function( event ) {
	if ( event.key === "ArrowDown" ) {
		$( document.activeElement ).next().focus();
		event.preventDefault();
	} else if ( event.key === "ArrowUp" ) {
		var newFocus;
		if ( $( document.activeElement ).index() === 0 ) {
			newFocus = $searchField;
		} else {
			newFocus = $( document.activeElement ).prev();
		}
		newFocus.focus();
		event.preventDefault();
	}
} );

$( "#search-form" ).on( "keydown", function( event ) {
	if ( event.key === "ArrowDown" ) {
		$suggestions.eq( 0 ).focus();
		event.preventDefault();
	}
} );

// Hide suggestion list when none of the search controls (search
// field, button or suggestion list) are in focus.
var searchControls = "#search-field, #search-button, .search-item";
$( searchControls ).on( "focus", function() {
	if( lastSearch ) {
		$searchSuggestionList.show();
	}
} );

$( searchControls ).on( "blur", function( event ) {
	if( event.relatedTarget === null || !event.relatedTarget.matches( searchControls ) ) {
		$searchSuggestionList.hide();
	}
} );
