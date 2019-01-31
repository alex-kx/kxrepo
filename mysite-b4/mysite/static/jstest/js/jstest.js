
    $(document).ready(function() {
        $("#button1").click(function () {
                $("#负荷数据选择").attr("value", 3)
            }
        );
    });

    $(document).ready(function() {
        $("#负荷数据选择").change(function () {
            $.ajax({
                type: "POST",
                dataType: "json",
                headers: {"X-CSRFToken": $.cookie('csrftoken')},
                url: "/jstest/jstest1/",
                data: {

                    url: "test",
                    input1: $("#负荷数据选择").val()
                },
                success: function (json, status, xhr) {
                    alert(json.发电机台数);
                }
            })
        });
    });


    $(document).ready(function() {
        //点击打开文件选择器

        $("#upload1").click(function () {
            //选择文件之后执行上传

            $.ajaxFileUpload({
                csrfmiddlewaretoken: '{{ csrf_token }}',
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                url: '/jstest/UploadExcel/', //url自己写
                secureuri: false, //这个是啥没啥用
                type: 'post',

                fileElementId: 'fileToUpload',//file标签的id
                dataType: 'json',//返回数据的类型
                //data:{name:'logan'},//一同上传的数据
                success: function (response, status) {
                    $("p").html(response);
                },
                error: function (data, status, e) {
                    alert(e);
                }
            });
        });
    });

