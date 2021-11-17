// Show and Hide Modal
function open_modal(trigger, modal, closeBtn) {
    trigger.click(() => {
        modal.show(500);
    });

    closeBtn.click(() => {
        modal.hide(500);
    });
}

// Remove a product from parcel and prevent double submission
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

// Mark product as selected to add to parcel
$('.add-items').each((key, value) => {
    $(value).click(() => {
        let item_class = $(value).attr('class');
        let class_list = item_class.split(" ");

        if(class_list.includes('selected')) {
            $(value).removeClass('selected');
        } else {
            $(value).addClass('selected');
        }

    });
    
});

// Add selected products to parcel
$('#add_items_btn').click(() => {

    let parcel_id;
    let product_id_list = [];

    $('.selected').each((key, value) => {
        parcel_id = $(value).data('pcid');
        let pdid = $(value).data('pdid');
        product_id_list.push(pdid);
    });

    let product_id = product_id_list.join(",").toString()

    const csrfToken = $('#token').val();
    let url = `/products/add_product_parcel/`;
    let data = {
                'csrfmiddlewaretoken': csrfToken,
                'parcel_id': parcel_id,
                'product_id': product_id,
               };

    $.post(url, data).done(function() {
         location.reload();
     });

});
