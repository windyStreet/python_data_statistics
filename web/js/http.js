//异步请求获取数据
function asyncRequest(data, callback,callback2) {
    $.ajax({
        type: "post",
        url: "service",
        data: data,
        dataType: "json",
        async:"true",
        success: function (data) {
            //var result = JSON.parse(data);
            callback(data);
        },
        failure:function (data) {
            callback2(data)
        },
    });
}