$('#expand-menu-icon').click(() => {
    $('.mobile-nav').show(300);
    $('.mobile-nav').children().show(300);
});

$('.close-menu').click(() => {
    $('.mobile-nav').hide(300);
    $('.mobile-nav').children().hide(300);
});

var currentYear= new Date().getFullYear(); 
$('#copyright-year').text(currentYear)
