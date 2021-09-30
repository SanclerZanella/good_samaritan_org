$(window).scroll(function() {
    let catg_col = $('.categories-col');
    if($(window).scrollTop() > 310 && $(window).scrollTop() < 10000){
        catg_col.css({
            'top': '0',
            'height': '98vh',
        });
    } else if($(window).scrollTop() > 10000) {
        catg_col.css({
            'top': '0',
            'height': '75vh',
        });
    } else {
        catg_col.css({
            'top': '349px',
            'height': '70vh',
        });
    }
 });