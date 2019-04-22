$(window).on('resize', function() {
    if ($(window).width() > 1000) {
        $('.card-box').addClass('half');
    } else {
        $('.card-box').removeClass('half');
    }
})
