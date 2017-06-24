/**
 * Created by bogdan on 23.06.17.
 */

var mySwiper = new Swiper ('.swiper-container', {

  direction: 'horizontal',
  slidesPerView:5,
  mousewheelControl:true,
  keyboardControl:true,
  autoplay: 2500,
  autoHeight:true,
  paginationType:'progress',
  speed:800,

  pagination: '.swiper-pagination',

  nextButton: '.swiper-button-next',
  prevButton: '.swiper-button-prev',


  breakpoints: {
    767: {
      slidesPerView: 3,
    },
    992: {
    slidesPerView: 4,
    },
  }
});


$("a > .img-circle").click(function(){
  var groupId = $(this).attr('id');

  $.get('/currentGroup/get/' + groupId + '/', {id: groupId}, function(data){
    $('#selected_group_add').html(data)
  });
});


