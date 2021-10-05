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

$('#quantity-field').change(() => {
    let field_val = parseInt($('#quantity-field').val());
    if(field_val == 0) {
        let default_val = 1;
        $('#quantity-field').val(default_val);
    }
});