function 读取达产率(){
    var mytable = document.getElementById("达产率表格");
    var data = [];
    for(var i=0,rows=mytable.rows.length; i<rows; i++){
         for(var j=0,cells=mytable.rows[i].cells.length; j<cells; j++){
            if(!data[i]){
                data[i] = new Array();
            }
            data[i][j] = mytable.rows[i].cells[j].innerHTML;
         }
    }

    var str1 = "";
    for(i=1; i<=20; i++){
        str1 = str1 + data[1][i] + ','
    }

    $("#达产率").val(str1);
}

$("#submit1").click(function () {
    读取达产率();
});

$("#btngraph").click(function(){
    $("#main").show();
    读取达产率();
    $.ajax({
        type: "POST",
        dataType: "json",
        headers: {"X-CSRFToken": $.cookie('csrftoken')},
        url: "/moduletest/economicAjax/",
        data: {
            供冷量: $("#供冷量").val(),
            供冷价格: $("#供冷价格").val(),
            供蒸汽量: $("#供蒸汽量").val(),
            蒸汽价格: $("#蒸汽价格").val(),
            售电量: $("#售电量").val(),
            售电价格: $("#售电价格").val(),
            供热量: $("#供热量").val(),
            供热价格: $("#供热价格").val(),
            光伏售电量: $("#光伏售电量").val(),
            光伏售电价格: $("#光伏售电价格").val(),
            天然气额外销售量: $("#天然气额外销售量").val(),
            天然气额外销售价格: $("#天然气额外销售价格").val(),

            天然气成本价格 : $("#天然气成本价格").val(),
            天然气耗量 : $("#天然气耗量").val(),
            水耗量 : $("#水耗量").val(),
            用水价格 : $("#用水价格").val(),
            电耗量 : $("#电耗量").val(),
            用电价格 : $("#用电价格").val(),
            土地租金 : $("#土地租金").val(),
            设备租金 : $("#设备租金").val(),
            维修费 : $("#维修费").val(),
            工资及福利 : $("#工资及福利").val(),
            变压器容量费 : $("#变压器容量费").val(),
            系统备用容量费 : $("#系统备用容量费").val(),
            光伏运维成本 : $("#光伏运维成本").val(),

            建筑费用: $("#建筑费用").val(),
            设备费用: $("#设备费用").val(),
            安装费用: $("#安装费用").val(),
            土地费用: $("#土地费用").val(),
            建设单位管理费: $("#建设单位管理费").val(),
            工程建设其他费用总和: $("#工程建设其他费用总和").val(),
            基本预备费: $("#基本预备费").val(),
            收购费用: $("#收购费用").val(),
            建设投资: $("#建设投资").val(),

            天然气是否先用后付: $("#天然气是否先用后付").val(),
            电费是否先用后付: $("#电费是否先用后付").val(),
            水费是否先用后付: $("#水费是否先用后付").val(),
            工资是否先用后付: $("#工资是否先用后付").val(),
            维修费是否先用后付: $("#维修费是否先用后付").val(),

            达产率: $("#达产率").val(),
            变量选择: $("#变量选择").val(),
            最大值: $("#最大值").val(),
            最小值: $("#最小值").val(),
            步长: $("#步长").val(),
        },
        success: function (json, status, xhr) {
            var x = json.x;
            var investment =  new Array();
            var annualIncome =  new Array();
            var annualCost =  new Array();
            var annualProfit =  new Array();
            var returnPeriod =  new Array();
            var iRR = new Array();
            var netValue =  new Array();

            for (var i = 0; i<json.技经计算结果列表.length; i++){
                // investment.push(json.技经计算结果列表[i].investment);
                // annualIncome.push(json.技经计算结果列表[i].annualIncome);
                // annualCost.push(json.技经计算结果列表[i].annualCost);
                annualProfit.push(json.技经计算结果列表[i].annualProfit);
                // returnPeriod.push(json.技经计算结果列表[i].returnPeriod);

                iRR.push(json.技经计算结果列表[i].iRR);


                // netValue.push(json.技经计算结果列表[i].netValue);
            }

            series1 = [
                {
                    name: '利润总额',
                    data: annualProfit,
                    type: 'line',
                     yAxisIndex: 0,
                },
                {
                    name: '内部收益率',
                    data: iRR,
                    type: 'line',
                     yAxisIndex: 1,
                },
            ];
            op = {
                xAxis: {
                    type: 'category',
                    data: x
                },
                series: series1
            };
            myChart.setOption(op)
        }
    })
});