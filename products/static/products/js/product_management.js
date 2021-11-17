// Sort products in products management page
$('.sort').each((key, value) => {
    $(value).change(() => {
        function slt(select) {
            selector = $(select);
            let currentUrl = new URL(window.location);

            let selectedVal = selector.val();
            if(selectedVal != "reset"){
                let sort = selectedVal.split("_")[0];
                let direction = selectedVal.split("_")[1];

                currentUrl.searchParams.set("sort", sort);
                currentUrl.searchParams.set("direction", direction);

                window.location.replace(currentUrl);
            } else {
                currentUrl.searchParams.delete("sort");
                currentUrl.searchParams.delete("direction");

                window.location.replace(currentUrl);
            }
        };

        slt_id = $(value).attr('id');

        if (slt_id == 'sort'){
            slt_element = $(value);
            slt(slt_element);
        } else if(slt_id == 'sort-lg') {
            slt_element = $(value);
            slt(slt_element);
        } else if(slt_id == 'sort-md') {
            slt_element = $(value);
            slt(slt_element);
        } else if(slt_id == 'sort-sm') {
            slt_element = $(value);
            slt(slt_element);
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

// Add new product to the shop and prevent double submission
$('.trigger_add_product').each((key, value) => {
    $(value).click(() => {
        $(value).prop("disabled", true);
        let openButton = $(value);
        let modal = $('#modal_add_product');
        let closeBtn = $('.closeBtn');
        
        open_modal(openButton, modal, closeBtn);

    });
});
