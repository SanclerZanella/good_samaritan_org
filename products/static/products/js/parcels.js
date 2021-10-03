$(document).ready(() => {

    let currentUrl = new URL(window.location);
    
    $('.parcel-card').each((key, value) => {
        $(value).click(() => {
            let parcel_id = $(value).attr('id');
    
            currentUrl.searchParams.set("parcel", parcel_id);
    
            window.location.replace(currentUrl);
        });
    });
    
    param = currentUrl.searchParams.get('parcel')
    if(param == 'parcel_1') {
        $('#parcel_1').css({
            'border': '2px solid #e72b37'
        });
        $('#check_1').css({
            'display': 'block'
        });
    } else if(param == 'parcel_2') {
        $('#parcel_2').css({
            'border': '2px solid #e72b37'
        });
        $('#check_2').css({
            'display': 'block'
        });
    } else if(param == 'parcel_3') {
        $('#parcel_3').css({
            'border': '2px solid #e72b37'
        });
        $('#check_3').css({
            'display': 'block'
        });
    }
});