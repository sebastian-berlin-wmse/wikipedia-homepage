var ajaxCallTimeout = 5000;
var suggestTimeout = null;
var delay = 100;
var searchLang = "de";
var lastSearch = "";
var searchPath = 'go';

function triggerSuggestLater( lang ) {
	if ( suggestTimeout ) clearTimeout( suggestTimeout ); //kill suggestion timer
	suggestTimeout = setTimeout( "searchSuggest('" + lang + "')", delay );
}

function searchSuggest( lang ) {
	searchLang = lang;
	var str = $( '#txtSearch' ).val();

	if ( str == lastSearch ) return;
	lastSearch = str;

	if ( str == "" ) {
		hideSuggest();
	} else {
		$.ajax( 'suggest', {
			data: {
				lang: searchLang,
				search: str
			},
			success: function( response ) {
				handleSearchSuggest( str, response )
			},
			timeout: ajaxCallTimeout
		} );
	}
}

function hideSuggest() {
	$( '#search-suggestion-list' ).hide();
	lastSearch = "";
}

function getSearchLink( query, language, provider ) {
	var queryParams = {
		l: language,
		q: query
	};

	if ( typeof provider === 'string' ) {
		queryParams.e = provider;
		queryParams.s = 'search';
	}

	return searchPath + '?' + $.param( queryParams );
}

function handleSearchSuggest( term, suggestions ) {
	var searchString = lastSearch;
    let $suggestions = $(".search-suggestion");
    $suggestions.hide();
    $("#search-suggestion-list").show();
    $("#search-for").attr("href", getSearchLink( term, searchLang ));
    $("#search-term").text(term);

    let i = 0;
    for(let suggestion of suggestions) {
        let $element = $suggestions.eq(i);
        let $link = $element.find("a");
        $element
            .text(suggestion)
            .attr("href", getSearchLink( suggestion, searchLang ))
            .show();
        i ++;
	}
};

$( '#search-suggestion-list' ).on( 'keydown', function(event) {
    if(event.key === "ArrowDown") {
        $(document.activeElement).next().focus();
        event.preventDefault();
    } else if(event.key === "ArrowUp") {
        let newFocus;
        if($(document.activeElement).index() === 0) {
            newFocus = $("#txtSearch");
        } else {
            newFocus = $(document.activeElement).prev();
        }
        newFocus.focus();
        event.preventDefault();
    }
} );

$( '#frmSearch' ).on( 'keydown', function(event) {
    if(event.key === "ArrowDown") {
        $(".search-suggestion").eq(0).focus();
        event.preventDefault();
    }
} );

// let focusLost = false;

// $( '#txtSearch' ).on( 'focusout', (e) => {
//     console.log("focusout:", e.target, "=>", e.relatedTarget);
//     focusLost = true;
// } );

// $( 'body' ).on( 'focusin', (e) => {
//     console.log("focusin:", e.target);
//     if(focusLost) {
// 	    $( '#search-suggestion-list' ).hide();
//     }
//     focusLost = false;
// } );

// $( 'body' ).on( 'focus', (e) => {
//     console.log("focus:", e.target);
// } );

let searchControls = "#txtSearch, #cmdSearch, .search-item";

$( searchControls ).on( 'focus', (e) => {
    if(lastSearch) {
        $( '#search-suggestion-list' ).show();
    }
} );

$( searchControls ).on( 'blur', (e) => {
    // console.log(e);
    if(e.relatedTarget === null || !e.relatedTarget.matches(searchControls)) {
        $( '#search-suggestion-list' ).hide();
    }
} );
