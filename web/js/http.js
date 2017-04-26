 //获取数据
    function request(name,data, callback) {
        $.ajax({
            type: "post",
            url: "web/"+name,
            data: data,
            dataType: "json",
            async:"true",
            success: function (data) {
                //var result = JSON.parse(data);
                callback(data);
            }
        });
    }