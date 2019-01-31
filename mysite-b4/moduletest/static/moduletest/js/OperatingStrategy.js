 var myChart = echarts.init(document.getElementById('main'));
        var series1 =  [


            {
                name: '发电机产汽量',
                data: 发电机运行列表,
                type: 'line',
                smooth: true
            },
            {
                name: '燃气锅炉产汽量',
                data: 燃气锅炉运行列表,
                type: 'line',
                smooth: true
            },
            {
                name: '备用燃气锅炉产汽量',
                data: 备用燃气锅炉运行列表,
                type: 'line',
                smooth: true
            }
        ];

        if (0>1){
            series1.push(
                {
                    name: '蒸汽负荷',
                    data: 蒸汽负荷,
                    type: 'line',
                    smooth: true
                }
            )
        }


        option = {

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
            data: 时间
        },
        yAxis: {
            type: 'value'

        },
         dataZoom: [
        {   // 这个dataZoom组件，默认控制x轴。
            type: 'slider', // 这个 dataZoom 组件是 slider 型 dataZoom 组件
            start: 0,      // 左边在 10% 的位置。
            end: 0.5,         // 右边在 60% 的位置。
        }
        ],


        series: series1
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);