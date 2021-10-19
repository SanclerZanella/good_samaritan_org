let countrySelected = $('#id_default_country').val();
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
