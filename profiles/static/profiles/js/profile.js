// Add style to contry options
var countrySelected = $('#id_default_country').val();
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});

// Show and Hide Modal
function open_modal(trigger, modal, closeBtn) {
    trigger.click(() => {
        modal.show(500);
    });

    closeBtn.click(() => {
        $('.finish-sponsor-btn').prop("disabled", false);
        modal.hide(500);
    });
};

// Finish sponsorship and prevent double submission
$('.finish-sponsor-btn').click(() => {
    $('.finish-sponsor-btn').prop("disabled", true);
    let openButton = $('.finish-sponsor-btn');
    let modal = $('#modal_finish-sponsor');
    let closeBtn = $('.closeBtn');
    
    open_modal(openButton, modal, closeBtn);

});

// Redeem form input fields validation
var form = $('#redeem-form');
var subs_id = $('#redeem-subs');
var last4 = $('#last-digits');

// Subscription id input validation
subs_id.keyup(() => {
    check_sub = subs_id.val().split("_")[0];

    if(subs_id.val() == "" || check_sub != 'sub') {
        subs_id.addClass('alert');
    } else {
        subs_id.removeClass('alert');
    }
});

// Last 4 digits input validation
last4.keyup(() => {
    if(last4.val().length != 4) {
        last4.addClass('alert');
    } else {
        last4.removeClass('alert');
    }
});

// Redeem form validation
form.submit((e) => {
    e.preventDefault();
    check_sub = subs_id.val().split("_")[0];
    
    if(last4.val().lengh != 4 && subs_id.val() == "" && check_sub != 'sub') {
        subs_id.addClass('alert');
        last4.addClass('alert');
    } else if(last4.val().length != 4) {
        last4.addClass('alert');
    } else if(subs_id.val() == "") {
        subs_id.addClass('alert');
    } else if(check_sub != 'sub') {
        subs_id.addClass('alert');
    } else {
        e.currentTarget.submit();
    }
});
