var myChart = echarts.init(document.getElementById('main'));
var xlist = new Array();
for (i=0; i<方案标识列表.length; i++){
    xlist.push('方案' + (i+1).toString())
}
        var series1 =  [
            {
                name: '建设投资',
                data: 建设投资列表,
                type: 'bar',
                barCategoryGap :'50%'
            },
            {
                name: '利润总额',
                data: 利润总额列表,
                type: 'bar',
                 yAxisIndex: 1,
                barCategoryGap :'50%'
            },
            {
                name: '内部收益率',
                data: 内部收益率列表,
                type: 'bar',
                 yAxisIndex: 2,
                barCategoryGap :'50%'
            },
            // {
            //     name: '投资回收期',
            //     data: 投资回收期列表,
            //     type: 'bar',
            //      yAxisIndex: 3,
            //     barCategoryGap :'50%'
            //
            // }

        ];

        option = {

        legend: {
            show: true,
            data: ['建设投资', '利润总额', '投资回收期', '内部收益率']
        },

        grid:{
            x:50,
            y:70,
            x2:200,
            y2:40,
            borderWidth:1
        },

        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },

        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },

        xAxis: {
            type: 'category',
            data: 方案标识列表
        },
        yAxis: [
            {
                type: 'value',
                name: '建设投资(万元)',
                position: 'left'
            },
            {
                type: 'value',
                name: '利润总额(万元)',
                position: 'right',
                min :0
            },
            {
                type: 'value',
                name: '内部收益率',
                position: 'right',
                min :0,
                offset:80
            },
            // {
            //     type: 'value',
            //     name: '投资回收期',
            //     position: 'right',
            //     offset:160
            // }
        ],
         dataZoom: [
        {   // 这个dataZoom组件，默认控制x轴。
            type: 'slider', // 这个 dataZoom 组件是 slider 型 dataZoom 组件
            start: 0,      // 左边在 10% 的位置。
            end: 100         // 右边在 60% 的位置。
        }
        ],

        series: series1
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);

                    //     $("#btngraph").click(function(){
                    //     var series1 = new Array();
                    //     var str = ["volov"];
                    //     str.push("BMW");
                    //     if ($("#cb1").prop('checked')){
                    //         alert('建设投资');
                    //         series1.push({
                    //             name: '建设投资',
                    //             data: 建设投资列表,
                    //             type: 'bar'
                    //         })
                    //
                    //     }
                    //
                    //      if ($("#cb2").prop('checked')){
                    //         alert('利润总额');
                    //         series1.push({
                    //             name: '利润总额',
                    //             data: 利润总额列表,
                    //             type: 'bar',
                    //              yAxisIndex: 1
                    //             }
                    //         )
                    //     }
                    //
                    //      if ($("#cb3").prop('checked')){
                    //         alert('内部收益率');
                    //         series1.push({
                    //             name: '内部收益率',
                    //             data: 内部收益率列表,
                    //             type: 'bar',
                    //              yAxisIndex: 2
                    //             }
                    //         )
                    //     }
                    //
                    //      if ($("#cb4").prop('checked')){
                    //         series1.push({
                    //             name: '投资回收期',
                    //             data: 投资回收期列表,
                    //             type: 'bar',
                    //              yAxisIndex: 3
                    //             }
                    //         )
                    //     }
                    //
                    //     alert(series1);
                    //     op = myChart.getOption();
                    //     op.series = series1;
                    //     myChart.clear();
                    //     myChart.setOption(op);
                    // });

