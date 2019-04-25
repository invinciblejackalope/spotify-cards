// to adjust the way the boxes are distributed if the screen is very small. see
// also index.html and index.css
$(window).on('resize', function() {
    if ($(window).width() > 1000) {
        $('.card-box').addClass('half');
    } else {
        $('.card-box').removeClass('half');
    }
})
