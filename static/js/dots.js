/**
 * Created by bogdan on 18.05.17.
 */

function title() {
  var elem, size, text;
  var elem = document.getElementsByClassName('tit');
  var text = elem.innerHTML;
  var size = 100;
  var n = 100;
  for(var i = 0; i < elem.length; i++) { /* необходимо вставить цикл, чтоб получить все блоки с классом tit */
    if(elem[i].innerHTML.length > size) {
      text = elem[i].innerHTML.substr(0,n);
    }
	else {
      text = elem[i].innerHTML;
    }
    elem[i].innerHTML = text + '...';
  }
}
title();