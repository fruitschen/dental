$().ready(function(){
    // the body of this function is in assets/material-kit.js
    window_width = $(window).width();
    if(window_width <=420){
        $('.overlap-text .initial-six').each(function(){
            if($(this).text() == '大象家庭口腔'){
                $(this).addClass('initial-six-bold');
                $(this).css('color', '#87b0c9')
            }
        })
    }

    // 小屏幕上，五列图标，把第二行的两个图标居中。
    var current_top = null;
    $('.image-list-5-item').each(function(){
        console.log(current_top)
        if(current_top && $(this).offset().top != current_top){
            $(this).css('margin-left', '16.66666667%')
        }
        current_top = $(this).offset().top;
    })

});