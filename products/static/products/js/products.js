// Stick categories col in the page side
if($(document).height() < 1000){
    let catg_col = $('.categories-col');
    let product_col = $('.products-col');
    catg_col.css({
        'position': 'static',
    });
    product_col.css({
        'margin-left': '0',
    });
} else {
    $(window).scroll(function() {
        /*
        Rezises and repositions the categories list sticked on page side
         */
    
        let start_sticky = ($(document).height() - ($(document).height() - 1)) + 309;
        let doc_end = $(document).height() - 1000;
        let catg_col = $('.categories-col');
        
        if($(window).scrollTop() > start_sticky && $(window).scrollTop() < doc_end){
            catg_col.css({
                'top': '0',
                'height': '98vh',
            });
        } else if($(window).scrollTop() > doc_end) {
            catg_col.css({
                'top': '0',
                'height': '70vh',
            });
        } else {
            catg_col.css({
                'top': '349px',
                'height': '70vh',
            });
        }
    
     });
}

//  Infinite Loading from https://simpleisbetterthancomplex.com/tutorial/2017/03/13/how-to-create-infinite-scroll-with-django.html
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
      $('.loading').show();
    },
    onAfterPageLoad: function ($items) {
      $('.loading').hide();
    }
});

// Sort products
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

        if (slt_id == 'sort-lg'){
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
};

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
