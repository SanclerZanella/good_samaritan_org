// Highlight chosen sponsorship and change url to related sponsorship option
$(document).ready(() => {

    let currentUrl = new URL(window.location);
    
    $('.sponsor-card').each((key, value) => {
        $(value).click(() => {
            let sponsor_id = $(value).attr('id');
    
            currentUrl.searchParams.set("sponsor", sponsor_id);
    
            window.location.replace(currentUrl);
        });
    });
    
    param = currentUrl.searchParams.get('sponsor')
    if(param == 'sponsor-prod_KTO0rZ3DSbX6cu' || param == null) {
        $('#sponsor-prod_KTO0rZ3DSbX6cu').css({
            'border': '2px solid #e72b37'
        });
        $('#check_prod_KTO0rZ3DSbX6cu').css({
            'visibility': 'visible',
        });
    } else if(param == 'sponsor-prod_KTO2NqA3YSYuwN') {
        $('#sponsor-prod_KTO2NqA3YSYuwN').css({
            'border': '2px solid #e72b37'
        });
        $('#check_prod_KTO2NqA3YSYuwN').css({
            'visibility': 'visible',
        });
    } else if(param == 'sponsor-prod_KTO3PepAZNLNtl') {
        $('#sponsor-prod_KTO3PepAZNLNtl').css({
            'border': '2px solid #e72b37'
        });
        $('#check_prod_KTO3PepAZNLNtl').css({
            'visibility': 'visible',
        });
    }
});