/**
 * Created by bogdan on 23.06.17.
 */


  var mySwiper = new Swiper ('.swiper-container', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    slidesPerView:5,
    mousewheelControl:true,
    keyboardControl:true,
    autoplay: 2500,
    autoHeight:true,
    paginationType:'progress',
    speed:800,

    // If we need pagination
    pagination: '.swiper-pagination',

    // Navigation arrows
    nextButton: '.swiper-button-next',
    prevButton: '.swiper-button-prev',

    // And if we need scrollbar

    breakpoints: {
      767: {
        slidesPerView: 3,
      },
      992: {
      slidesPerView: 4,
    },
  }

  })


