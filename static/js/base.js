// Mobile nav icon
$('#expand-menu-icon').click(() => {
    $('.mobile-nav').removeClass('display-mobile-nav');
    $('.mobile-nav').show(300);
    $('.mobile-nav').children().show(300);
});

// Cole mobile nav bar
$('.close-menu').click(() => {
    $('.mobile-nav').addClass('display-mobile-nav')
    $('.mobile-nav').hide(300);
    $('.mobile-nav').children().hide(300);
});

// Bootstrap Message (from Boutique Ado)
$('.toast').toast('show');

// Update footer year
var currentYear= new Date().getFullYear(); 
$('#copyright-year').text(currentYear)
