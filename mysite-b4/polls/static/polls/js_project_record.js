


    function show_user_specific_project_record_table(){
        var project_name = $("#user_project_select").val();
        $.ajax({
            type: "POST",
            dataType: "json",
            headers: {"X-CSRFToken": $.cookie('csrftoken')},
            url: "../retrieve_user_specific_project_record/",
            data:{
                'project_name':project_name
            },
            success: function (json) {
                var year_Num_list = json.year_Num_list;
			    var week_Num_list = json.week_Num_list;
			    var user_specific_project_record_list = json.user_specific_project_record_list;
			    var user_specific_project_working_days_list = json.user_specific_project_working_days_list;
			    var arr0 = [
			        year_Num_list,
                    week_Num_list,
                    user_specific_project_working_days_list,
                    user_specific_project_record_list

                ];
			    var dataSet = arr0[0].map(function(col, i) {
                    return arr0.map(function(row) {
                    return row[i];
                   })
                });

                var user_specific_project_record_table = $('#user_specific_project_record_table').DataTable({
                    destroy: true,
                    data : dataSet,
                    "columns": [
                        { "width": "10%" ,title:"年"},
                        { "width": "10%" ,title:"周"},
                        { "width": "10%" ,title:"工时（天）"},
                        { "width": "70%" ,title:"工作事项"}
                    ],
                    dom: 'Bfrtip',
                    buttons: [ {
                        extend: 'excelHtml5',
                        customize: function( xlsx ) {
                            var sheet = xlsx.xl.worksheets['sheet1.xml'];
                            $('row c[r^="C"]', sheet).attr( 's', '2' );
                        }
                    } ]
                } );
                $('#user_specific_project_record_table tbody').on( 'click', 'tr', function () {
                    if ( $(this).hasClass('selected') ) {
                        $(this).removeClass('selected');
                    }
                    else {
                        user_specific_project_record_table.$('tr.selected').removeClass('selected');
                        $(this).addClass('selected');
                    }
                } );

                $('#button_delete_row').click( function () {
                    user_specific_project_record_table.row('.selected').remove().draw( false );
                } );

            }
        });
    }



    $("#user_project_select").change(function () {
        show_user_specific_project_record_table();
    });


      function set_project_list(select_id) {
        $.ajax({
            type: "POST",
            dataType: "json",
            headers: {"X-CSRFToken": $.cookie('csrftoken')},
            url: "/polls/retrieve_project_name_list/",
            data:{},
            success: function (json) {
                var project_name_list = json.project_name_list;
                for(i=0; i<project_name_list.length; i++){
                    $("#"+select_id).append("<option>" + project_name_list[i] + "</option>");
                }
                for(var i=1;i<54;i++){
                    $("#week_Num").append("<option value=" + i + ">" + "第" + i + "周" + "</option>");
                }
            }
        });
      }
      $(document).ready(function(){
          set_project_list("project_name");
          set_project_list("user_project_select");
      });

    var myChart = echarts.init(document.getElementById('user_working_days_chart'));
    var myChart2 = echarts.init(document.getElementById('user_working_days_chart2'));
    $("#v-pills-profile-tab").click(function () {
         $.ajax({
            type: "POST",
            dataType: "json",
            headers: {"X-CSRFToken": $.cookie('csrftoken')},
            url: "/polls/retrieve_user_project_record/",
            data: {},
            success: function (json) {
                var user_working_days_list = json.user_working_days_list;
                var week_Num_list = json.week_Num_list;
                var year_Num_list = json.year_Num_list;
                var date_list = new Array();
                for(var i=0;i<user_working_days_list.length;i++){
                    if (i==0){
                        date_list.push(year_Num_list[i]+'年\n'+week_Num_list[i]+'周')
                    }
                    else if (year_Num_list[i] - year_Num_list[i-1] > 0){
                        date_list.push(year_Num_list[i]+'年\n'+week_Num_list[i]+'周')
                    }
                    else{
                        date_list.push(week_Num_list[i]+'周')
                    }

                }

                setoption_working_days_list( user_working_days_list, date_list);
            }
        });
    });


        function setoption_working_days_list(user_working_days_list, date_list){
            option = {
            color: ['#3398DB'],
            tooltip : {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis : [
                {
                    type : 'category',
                    data : date_list,
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            yAxis : [
                {
                    type : 'value'
                }
            ],
            series : [
                {
                    name:'',
                    type:'bar',
                    barWidth: '60%',
                    data:user_working_days_list
                }
            ]
        };
       myChart.setOption(option);
        myChart2.setOption(option);
        }


