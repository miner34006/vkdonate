/**
 * Created by bogdan on 23.06.17.
 */

    $("a > .img-circle").click(function(){
      var groupId = $(this).attr('id');

      $.get('/currentGroup/get/' + groupId + '/', {id: groupId}, function(data){
        $('#add').html(data)
        $("#add").removeClass("hidden");
     });


    });
