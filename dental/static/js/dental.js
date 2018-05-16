$().ready(function(){
    // the body of this function is in assets/material-kit.js
    window_width = $(window).width();
    if(window_width <=420){
        $('.overlap-text .initial-six').each(function(){
            if($(this).text() == '大象家庭口腔'){
                $(this).addClass('initial-six-bold');
            }
        })
    }
});