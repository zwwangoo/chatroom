/**
 * Created by smart on 2017/7/23.
 */
$(document).ready(function() {

    document.getElementsByName("message")[0].focus();

    $(".msg-list").animate({scrollTop:$(".msg-list")[0].scrollHeight + "px"}, 100);  // 将聊天记录滚到最后

	$("input[name='submit']").click(function () {
		sendMsg($("textarea[name='message']").val(), 0)
	});
});

function sendMsg(message, msg_type) {
    $.ajax({
        url:"/sendMsg",
        type:"post",
        dataType:"json",
        data:{
            "message": message,
            "type": msg_type,
            "_xsrf":$("input[name='_xsrf']").val()
        },
        success:function(data){
            document.getElementsByName("message")[0].value = "";
        },
        error:function (data) {
            console.log(data);
        }
    })
}

function on_return(evt){
    evt = evt ? evt : (window.event ? window.event : null);
    if(evt.keyCode == 13){
        if (document.all('submit')!=null){
            document.all('submit').click();
        }
    }
 }

function broadcast(operating) {
    if(operating == "in"){
        message = "加入聊天室";
    }else {
        message = "离开聊天室";
    }
    sendMsg(message, 1);
}