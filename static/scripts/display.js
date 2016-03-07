/**
 * Created by Yue Dayu on 2016/3/7.
 */

$('.person').click(function() {
    //alert($(this).attr('id'));
    var user_id = $(this).attr('id');
    var image_src = $('#' + user_id + ' img').attr('src');
    var content = '';
    var name = '';
    for (var x in list) {
        if (list[x].sender_id == parseInt(user_id)) {
            content = list[x].content;
            name = list[x].name;
            break;
        }
    }
    $('#model_avatar').attr('src', image_src);
    $('#myModalLabel').html('留言内容-' + name);
    $('#model_content').html(content);
    $('#myModal').modal();
});