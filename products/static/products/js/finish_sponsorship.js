// Show and Hide Modal
function open_modal(trigger, modal, closeBtn) {
    trigger.click(() => {
        modal.show(500);
    });

    closeBtn.click(() => {
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