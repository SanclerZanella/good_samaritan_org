$(window).scroll(function() {
    /*
    Rezises and repositions the categories list sticked on page side
     */

    let start_sticky = ($(document).height() - ($(document).height() - 1)) + 309;
    let doc_end = $(document).height() - 1000;
    let catg_col = $('.categories-col');
    
    if($(window).scrollTop() > start_sticky && $(window).scrollTop() < doc_end){
        catg_col.css({
            'top': '0',
            'height': '98vh',
        });
    } else if($(window).scrollTop() > doc_end) {
        catg_col.css({
            'top': '0',
            'height': '73vh',
        });
    } else {
        catg_col.css({
            'top': '349px',
            'height': '70vh',
        });
    }

 });

//  Infinite Loading from https://simpleisbetterthancomplex.com/tutorial/2017/03/13/how-to-create-infinite-scroll-with-django.html
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
      $('.loading').show();
    },
    onAfterPageLoad: function ($items) {
      $('.loading').hide();
    }
});

 
