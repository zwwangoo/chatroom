/**
 * Created by smart on 2017/7/21.
 */
$("body").on("click", "input[name='submit']", function () {
    roomname = $("input[name=roomname]").val();
    password = $("input[name=password]").val();
    if(roomname == ""){
        return false;
    }
    $.ajax({
        url: "/createroom",
        type: "post",
        dataType: "json",
        data:{
            "_xsrf": $("input[name='_xsrf']").val(),
            "roomname": roomname,
            "password": password
        },
        success: function (data) {
            var str = "<tr><td>" + data.roomId + "</td>";
            str += "<td>" + data.roomname + "</td>";
            str += "<td>" + data.username + "</td>";
            str += "<td>" + data.created_time + "</td>";
            str += "<td>" + 10 + "</td>";
            str += "<td><a href='/chatroom/"+ data.roomId +"'>立即加入</a></td>";
            $(".allRoom").append(str);
            $(".mineRoom").append(str);
            $(".close-box").click();
        },
        error:function (data) {
            console.log(data);
            return false;
        }
    })
});
function resetForm() {
    $("input[typt=text], input[tpye=password]").val("");
}