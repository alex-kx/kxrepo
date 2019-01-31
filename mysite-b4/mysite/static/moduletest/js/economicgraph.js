 // $("#main").hide();

var myChart = echarts.init(document.getElementById('main'));
var series1 =  [
    {
        name: '利润总额',
        data: [],
        type: 'line',
         yAxisIndex: 0,
    },
    {
        name: '内部收益率',
        data: [],
        type: 'line',
         yAxisIndex: 1,
    },
];

option = {

legend: {
    show: true,
    data: ['利润总额', '内部收益率']
},

grid:{
    x:50,
    y:70,
    x2:50,
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
    data: []
},
yAxis: [

    {
        type: 'value',
        name: '利润总额(万元)',
        position: 'left',
        min :0,
    },
    {
        type: 'value',
        name: '内部收益率',
        position: 'right',
        min: 0,
        offset:0,
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

