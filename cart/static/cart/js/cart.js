// Increase or Decrease products quantity in the shopping cart
$('.add-qty').each((key, value) => {
    $(value).click((e) => {
        e.preventDefault();

        let id = $(value).attr('id');
        let product_id = id.split('_')[1];
        let field_id = `#quantity-field_${product_id}`;
        let qty_field = $(field_id);
        let field_actual_val = parseInt(qty_field.val());

        if(id == `button-minus_${product_id}`) {
            if(field_actual_val != 1) {
                new_val = field_actual_val - 1;
                qty_field.val(new_val);
            }
        } else if(id == `button-plus_${product_id}`) {
            new_val = field_actual_val + 1;
            qty_field.val(new_val);
        }
    });
});

// Fix product quantity to 1
$('.quantity-field').each((key, value) => {

    $(value).change(() => {
        let field_val = parseInt($(value).val());
        if(field_val == 0) {
            let default_val = 1;
            $(value).val(default_val);
        }
    });

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

// Remove all products from cart modal and prevent double submission
$('.remove_all_trigger').each((key, value) => {
    $(value).click(() => {
        $('#remove-all-modal-btn').prop("disabled", true);
        let openButton = $(value);
        let modal = $('#modal_clear');
        let closeBtn = $('.closeBtn');
        
        open_modal(openButton, modal, closeBtn);

    });
});

// Disable button on form submission to prevent double submission 
$('.submit-form').submit(() => {
    $('.submit-trigger').prop("disabled", true);
});