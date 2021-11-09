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
