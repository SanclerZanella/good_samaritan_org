$('#expand-menu-icon').click(() => {
    $('.mobile-nav').show(300);
    $('.mobile-nav').children().show(300);
});

$('.close-menu').click(() => {
    $('.mobile-nav').hide(300);
    $('.mobile-nav').children().hide(300);
});

// Bootstrap Message (from Boutique Ado)
$('.toast').toast('show');

var currentYear= new Date().getFullYear(); 
$('#copyright-year').text(currentYear)
