$(function() {
    $("#datepicker1" ).datepicker({
        minDate: new Date()
    });
    $("#datepicker2").datepicker({
        minDate: new Date()
    });
    $("#datepicker3").datepicker({
    });
    $("#datepicker4").datepicker({
    });
    $("#setup_main_date").datepicker({
    });
    $("#main_date").datepicker({
    });
    $("#query_main_next_time").datepicker({
    });
    $("#min").datepicker({
    });
    $("#max").datepicker({
    });
});
$(document).ready(function() {
    $("li").each(function(index) {
        $("li").eq(index).click(function() {
            var a = $(this).siblings()
            var c = a.children()
            c.removeClass("active")
            var b = $(this).children()
            b.addClass("active")
            
        });
    });
}); 
//主页的目录切换控制
//function budget(){
//    $(".budget").removeClass("yc")
//    $(".user").addClass("yc")
//    $(".ng").addClass("yc")
//    $(".budgetform").addClass("yc")
//    $(".merge").addClass("yc")
//}
function check_ng(){
   $(".ng").removeClass("yc")
   $(".budget").addClass("yc")
   $(".user").addClass("yc")
   $(".budgetform").addClass("yc")
   $(".merge").addClass("yc")
   $(".detail").addClass("yc")
}
//function chart_tab(){
//    $(".statistic").removeClass("yc")
//    $(".budget").addClass("yc")
//    $(".user").addClass("yc")
//    $(".budgetform").addClass("yc")
//    $(".merge").addClass("yc")
//    $(".detail").addClass("yc")
//    $(".ng").addClass("yc")
//    $(".maintain").addClass("yc")
//}
function maintain(){
    $(".maintain").removeClass("yc")
    $(".budget").addClass("yc")
    $(".user").addClass("yc")
    $(".budgetform").addClass("yc")
    $(".merge").addClass("yc")
    $(".detail").addClass("yc")
    $(".ng").addClass("yc")
    $(".statistic").addClass("yc")
    $(".operation").addClass("yc")

    maintain_ajax();
}
//预算编码页面的内部控制
function apply(){
    $(".apply").removeClass("yc")
    $(".signing").addClass("yc")
    $(".signed").addClass("yc")
    $(".statement").addClass("yc")
    $(".ongoing").addClass("yc")
}
//function signing(){
//    $(".signing").removeClass("yc")
//    $(".apply").addClass("yc")
//    $(".signed").addClass("yc")
//    $(".statement").addClass("yc")
//}
//function signed(){
//    $(".signed").removeClass("yc")
//    $(".apply").addClass("yc")
//    $(".statement").addClass("yc")
//    $(".signing").addClass("yc")
//}
//function statement(){
//    $(".statement").removeClass("yc")
//    $(".apply").addClass("yc")
//    $(".signing").addClass("yc")
//    $(".signed").addClass("yc")
//}

//预算编码的申请页面的控制
//function budgetform(){
//    $(".budgetform").removeClass("yc")
//    $(".budget").addClass("yc")
//}
function rebudget(){
    $(".budgetform").addClass("yc")
    $(".budget").removeClass("yc")
}
////合并开单的页面控制
//function merge(){
//    $(".budget").addClass("yc")
//    $(".merge").removeClass("yc")
//}
function remerge(){
    $(".merge").addClass("yc")
    $(".budget").removeClass("yc")
}
//budget的图标操作
function modify_budget(obj){
        var id = obj.parent().parent().find("td").eq(1).text()
        $("#modify_budget").modal("show")
}
function delete_budget(){
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var b = $(this).find("td")
            $("#delete_id_form").val(b[1].innerHTML)
        });
    });
}
function copy_budget(){
    $("table tr").click(function() {
        var td = $(this).find("td");// 找到td元素
        $("#budget_form_id_copy").val(td[1].innerHTML)
        });
}
//全编辑
function modify_form(obj){
        var modify_unique_id = obj.parent().parent().find("td").eq(1).text()
         data ={
            'modify_unique_id':modify_unique_id,
        }
        alert("data")
        console.log(data);
        $.ajax({
            type:'POST',
            url:'/index/budget-modify-unique/',
            data:data,
            success:function(result){
                if(result['code'] === 200){
                       console.log(result['data'])
                       var a = result['data'][0]
                       budgetform()
                    $("#budgetId").val(a['Id'])
                    $("#depart_selector").val(a['Department'])
                    $("#Remark").val(a['Remark'])
                    $("#bud_num_type").val(a['Unit'])
                    $("#bud_principal").val(a['Pic'])
                    $("#bud_machine_name").val(a['ProductName'])
                    $("#bud_machine_type").val(a['Model'])
                    $("#p_price").val(a['UnitPrice'])
                    $("#p_qty").val(a ['Quantity'])
                    return false;
                }else{
                    window.message.showError(result['message'])
                    return false;
                }
            }
        })
}
function to_html(num){
    if(num == 1){
        $(".detail").addClass("yc")
        $(".budget").removeClass("yc")
        $(".apply").addClass("yc")
        $(".signing").removeClass("yc")
    }
    if (num == 2){
        $(".detail").addClass("yc")
        $(".budget").removeClass("yc")
        $(".apply").addClass("yc")
        $(".signed").removeClass("yc")
    }
    if(num == 3){
        $(".detail").addClass("yc")
        $(".budget").removeClass("yc")
        $(".apply").addClass("yc")
        $(".statement").removeClass("yc")
    }
} 
//设备保养操作界面切换
function operation(){
    $(".maintain").addClass("yc")
    $(".operation").removeClass("yc")
}
function re_maintain(){
    $(".operation").addClass("yc")
    $(".maintain").removeClass("yc")
    
}
//统计分析的图表切换
function picture(){
    $(".chart_pic").removeClass("yc")
    $(".data_tab").addClass("yc")
}
//function number_tab(){
//    $(".data_tab").removeClass("yc")
//    $(".chart_pic").addClass("yc")
//}
//checkbox全选
$(function () {
    //全选,设置chheckbox name='all' tbody id=tb
    $("input[name=all]").click(function () {
        if (this.checked) {
            $("#statement_detail :checkbox").prop("checked", true);
        } else {
            $("#statement_detail :checkbox").prop("checked", false);
        }
    });
});

//可视化
function visua(number1,number2,number3){
    var datas = new Array()
    for(var i = 0;i < number1.length;i ++){
        var map = {"value":number1[i][1], "name":number1[i][0],"itemStyle":{color: '#28a745'}}
        datas.push(map)
    }
    for(var i = 0;i < number2.length;i ++){
        var map = {"value":number2[i][1], "name":number2[i][0],"itemStyle":{color: '#ffc107'}}
        datas.push(map)
    }
    for(var i = 0;i < number3.length;i ++){
        var map = {"value":number3[i][1], "name":number3[i][0],"itemStyle":{color: '#dc3545'}}
        datas.push(map)
    }
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('main'));

    // 指定图表的配置项和数据
    var option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}:{c}({d}%)"
        },
        series: [
            {
                name:'数值样本',
                type:'pie',
                radius: ['30%', '60%'],
                center: ['50%', '50%'],
                label: {
                    normal: {
                        formatter: '{b|{b}：}{c}pcs{per|{d}%}',
                        rich: {
                            c: {
                                fontSize: 10,
                                lineHeight:25
                            },
                            per: {
                                padding:[2,4],
                                borderRadius:2
                            }
                        }
                    }
                },
                data:datas,
            }
        ] 
    }; 
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    myChart.on('click', function (params) {
        // 控制台打印数据的名称
        visual_data(params.name,params.color);
    });
}
//统计分析可视化
function visua_pic(num1,num2){
    //SN数据解析
    var data1 = new Array()
    for(var i = 0;i < num2.length;i ++){
        var map = {"value":num2[i][0], "name":num2[i][1]}
        data1.push(map)
    }
    //FAll次数数据解析
    var data2 = new Array()
    for(var i = 0;i < num1.length;i ++){
        var map = {"value":num1[i][0], "name":num1[i][1]}
        data2.push(map)
    } 
    // 基于准备好的dom，初始化echarts实例
    var myChart3 = echarts.init(document.getElementById('threemain'));
    var myChart4 = echarts.init(document.getElementById('fourmain'));

    // 指定图表的配置项和数据
    var option2 = {
        title: {
            text: 'FAll次数 依据已使用次数范围',
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        series : [
            {
                name: '数值样本',
                type: 'pie',
                radius : ['30%','60%'],
                center: ['50%', '50%'],
                label: {
                    normal: {
                        formatter: '{b|{b}：}{c}pcs{per|{d}%}',
                        rich: {
                            c: {
                                fontSize: 10,
                                lineHeight:25
                            },
                            per: {
                                padding:[2,4],
                                borderRadius:2
                            }
                        }
                    }
                },
                data:data2,
            }
        ]
    };
    var option3 = {
        title: {
            text: 'NG数量(按设备名称)',
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        series : [
            {
                name: '数值样本',
                type: 'pie',
                radius : ['30%','60%'],
                center: ['50%', '50%'],
                label: {
                    normal: {
                        formatter: '{b|{b}：}{c}pcs{per|{d}%}',
                        rich: {
                            c: {
                                fontSize: 10,
                                lineHeight:25
                            },
                            per: {
                                padding:[2,4],
                                borderRadius:2
                            }
                        }
                    }
                },
                data:data1,
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart3.setOption(option2);
    myChart4.setOption(option3);
}
function ErrorCode(num){
    var dataValue = new Array()
    var dataName = new Array()
    var datas = new Array()
    var sum = 0;
    for(var i = 0;i < num.length;i ++){
        dataName.push(num[i][0])
        dataValue.push(num[i][1])
        datas.push(sum)
        sum = sum + num[i][1]
        }
    dataValue.push(sum)
    dataName.push("总计")
    datas.push(0)
    var myChart1 = echarts.init(document.getElementById('onemain'));
     var option = {
         title: {
            text: '问题分布图',
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function (params) {
                var tar = params[1];
                return tar.name + '<br/>' + tar.seriesName + ' : ' + tar.value;
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type : 'category',
            splitLine: {show:false},
            data :dataName
        },
        yAxis: {
            type : 'value'
        },
        series: [
            {
                name: '辅助',
                type: 'bar',
                stack:  '总量',
                itemStyle: {
                    normal: {
                        barBorderColor: 'rgba(0,0,0,0)',
                        color: 'rgba(0,0,0,0)'
                    },
                    emphasis: {
                        barBorderColor: 'rgba(0,0,0,0)',
                        color: 'rgba(0,0,0,0)'
                    }
                },
                data:datas
            },
            {
                name: '样本数据',
                type: 'bar',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'inside'
                    }
                },
                data:dataValue
            }
        ]
    }; 
    myChart1.setOption(option);
    myChart1.on('click', function (params) {

    });
}
function pic_partname(num){
    var datas = new Array()
    for(var i = 0;i < num.length;i ++){
        var map = {"value":num[i][1], "name":num[i][0]}
        datas.push(map)
    }
    var myChart2 = echarts.init(document.getElementById('twomain'));
    var option1 = {
        title: {
            text: '问题设备分布图',
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        series : [
            {
                name: '数值样本',
                type: 'pie',
                radius : ['30%','60%'],
                center: ['50%', '50%'],
                label: {
                    normal: {
                        formatter: '{b|{b}：}{c}pcs{per|{d}%}',
                        rich: {
                            c: {
                                fontSize: 10,
                                lineHeight:25
                            },
                            per: {
                                padding:[2,4],
                                borderRadius:2
                            }
                        }
                    }
                },
                data:datas,
            }
        ]
    };
    myChart2.setOption(option1);
}
function maintain_sn(obj){
    $("#item_sn").html(obj)
}
