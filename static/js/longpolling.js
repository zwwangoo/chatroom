/**
 * Created by smart on 2017/7/23.
 */
var updater = {
    poll: function(){
        $.ajax({
            url: "/longpolling",
            type: "POST",
            dataType: "json",
            data:{"_xsrf":$("input[name='_xsrf']").val()},
            success: updater.onSuccess,
            error: updater.onError});
        },
    onSuccess: function(data){
        try{
            if (data.msg !== "") {
                var str = "";
                if (data.type === 1) {
                    str = " <div class='msg msg-title'>" + data.username + ":" + data.msg + "</div>";
                }
                else {
                    if (data.belong === 1) {
                        str += "<div class='msg msg-right'>";
                    } else {
                        str += "<div class='msg msg-left'>";
                    }
                    str += "<span class='msg-head'>" + data.username + "</span>";
                    str += "<span class='msg-time'>" + data.created_time + "</span>";
                    str += "<div class='msg-body'>" + data.msg + "</div>";
                }
                var msg_list = $(".msg-list");
                msg_list.append(str);
                msg_list.animate({scrollTop: msg_list[0].scrollHeight + "px"}, 100);
            }
        }
        catch(e){
            updater.onError(e);
            return;
        }
        updater.poll();
    },
    onError: function(e){
        if (e.message)
            console.log("Poll Error" + e.message);
        else
            console.log(e);
        }
    };

updater.poll();