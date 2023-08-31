var imgs = document.querySelectorAll('.slider img');
var dots = document.querySelectorAll('.dot');
imgs[0].style.opacity = 1;
dots[0].className += ' active';

function changeSlide(pk) {
    for (var i = 0; i < imgs.length; i++) { // reset
        if (imgs[i].id == `img-${pk}`) {
            imgs[i].style.opacity = 1;
            dots[i].className += ' active';
        } else {
            imgs[i].style.opacity = 0;
            dots[i].className = dots[i].className.replace(' active', '');
        }
    } 
}