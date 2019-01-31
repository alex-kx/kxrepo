
    function initialize_price_table(){
        var dataSet = [];
        var price_table = $('#price_table').DataTable({
            destroy: true,
            "paging":   false,
            searching : false,
            responsive: false,
            data : dataSet,
            "columns": [
                { "width": "20%" ,title:"设备名称"},
                { "width": "20%" ,title:"设备规模"},
                { "width": "15%" ,title:"单价（万元）"},
                { "width": "15%" ,title:"数量"},
                { "width": "15%" ,title:"设备费（万元）"},
                { "width": "15%" ,title:"安装费（万元）"}
            ],
            dom: 'Bfrtip',
            buttons: [ {
                extend: 'excelHtml5',
                text: '导出excel表格',

                customize: function( xlsx ) {
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="C"]', sheet).attr( 's', '2' );
                }
            } ]
        } );
        $('#price_table tbody').on( 'click', 'tr', function () {
            if ( $(this).hasClass('selected') ) {
                $(this).removeClass('selected');
            }
            else {
                price_table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        } );

        $('#button_delete_row').click( function () {
            price_table.row('.selected').remove().draw( false );
        } );


        $('#addRow').on( 'click', function () {
            var str_ref_installation_fee = $("#ref_installation_fee").val();
            var ref_installation_fee = parseFloat(str_ref_installation_fee)/100;

            price_table.row.add( [
                $("#device").val(),
                $("#capacity").val(),
                $("#ref_unit_price").val() * $("#capacity").val(),
                $("#n_device").val(),
                $("#capacity").val() * $("#ref_unit_price").val() * $("#n_device").val(),
                ($("#capacity").val() * $("#ref_unit_price").val() * $("#n_device").val() * ref_installation_fee).toFixed(2)
            ] ).draw( false );
        } );
    }

    $(document).ready(function () {
        initialize_price_table();
    });



    $("#device").change(function () {
        if ($("#device").val() != "0") {
            if ($("#capacity").val() > 0){
                update_ref_info($("#capacity").val());
            }
            else{
                update_ref_info(1);
            }
        }
    });

    $("#capacity").change(function () {
        if ($("#device").val() != "0") {
            if ($("#capacity").val() > 0) {
                update_ref_info($("#capacity").val());
            }
            else {
                update_ref_info(1);
            }
        }
    });


    function update_ref_info(capacity) {
        $.ajax({
            type: "POST",
            dataType: "json",
            headers: {"X-CSRFToken": $.cookie('csrftoken')},
            url: "/price_evaluation/retrieve_ref_price/",
            data: {
                "device":$("#device").val(),
                "capacity":capacity
            },
            success: function (json) {
                $("#ref_unit_price_info").text("参考取值: " + json.ref_unit_price);
                $("#ref_installation_fee_info").text("参考取值: "+ json.ref_installation_fee);
                $("#capacity_label").text("设备规模（"+ json.unit + ")");
                $("#unit_price_label").text("单位造价（万元/" + json.unit+")");
            }
        })
    }

