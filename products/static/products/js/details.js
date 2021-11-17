// Increase quantity input in details page
$('.add-qty').each((key, value) => {
    $(value).click((e) => {
        e.preventDefault();

        let id = $(value).attr('id');
        let qty_field = $('#quantity-field');
        let field_actual_val = parseInt(qty_field.val());

        if(id == 'button-minus') {
            if(field_actual_val != 1) {
                new_val = field_actual_val - 1;
                qty_field.val(new_val);
            }
        } else if(id == 'button-plus') {
            new_val = field_actual_val + 1;
            qty_field.val(new_val);
        }
    });
});

// Keep quantity always in 1
$('#quantity-field').change(() => {
    let field_val = parseInt($('#quantity-field').val());
    if(field_val == 0 || field_val <= 0) {
        let default_val = 1;
        $('#quantity-field').val(default_val);
    }
});

// Show and Hide Modal
function open_modal(trigger, modal, closeBtn) {
    trigger.click(() => {
        modal.show(500);
    });

    closeBtn.click(() => {
        modal.hide(500);
    });
}

// Remove a product from cart modal and prevent double submission
$('.remove-item-btn').each((key, value) => {
    $(value).click(() => {
        $(value).prop("disabled", true);
        let openButton = $(value);
        let openButton_id = $(value).attr('id');
        let item_id = openButton_id.split('_')[1];
        let modal_id = `#modal_${item_id}`;
        let modal = $(modal_id);
        let closeBtn = $('.closeBtn');
        
        open_modal(openButton, modal, closeBtn);

    });
});