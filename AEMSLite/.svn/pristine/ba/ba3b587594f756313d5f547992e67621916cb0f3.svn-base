//检查之前有没有设定参数，有的就映射到页面上
function before_setup(){
    $.ajax({
    type:'GET',
    data:{},
    url:'/maintain_monitor/setup-range-before/',
    beforeSend :function(xmlHttp){
                xmlHttp.setRequestHeader("If-Modified-Since","0");
                xmlHttp.setRequestHeader("Cache-Control","no-cache");
            },
    success:function(result){
    if(result['code'] === 200){
        console.log(result['data'])
        $("#maintain_count").empty()
        $("#maintain_date").empty()
        $('#maintain_receiver').empty()
        $("#maintain_count").val(result['data'][0].Max)
        $("#maintain_date").val(result['data'][1].Max)
        console.log(result['data'][1].Reminders)
        var data=result['data']
        var str=result['data'][1].Reminders.split(',')
        for(var i=2; i<data.length; i++){
            user_mail = (data[i].Email.split('@'))[0]
            $("#maintain_receiver").append('<option value='+user_mail+'>'+user_mail+'</option>')
        }
        $('#maintain_receiver').selectpicker('val',str);
        $('#maintain_receiver').selectpicker('refresh');
        $('#maintain_receiver').selectpicker('render');
    }else{
        alert(result['message'])
    }
    }
    })
}

//设置保养次数和保养周期时间
function setup_maintain(){
    var maintain_count = $("#maintain_count").val()
    var maintain_date = $("#maintain_date").val()
    var maintain_receiver = $("#maintain_receiver").val()
    var Regx =  /^[A-Za-z]*$/;
    if(maintain_count == ""){
        window.message.showError("maintain count can't be empty")
        return false;}
    if(Regx.test(maintain_count)){
        window.message.showError("maintain count is digital")
        return false;}
    if(maintain_date == ""){
        window.message.showError("maintain date can't be empty")
        return false;}
    if(Regx.test(maintain_date)){
        window.message.showError("maintain date is digital")
        return false;}

    if(maintain_receiver == ""){
        window.message.showError("maintain mail receive can't be empty")
        return false;}
    data = {
        'maintain_count':maintain_count,
        'maintain_date':maintain_date,
        'maintain_receiver':maintain_receiver,
    }
//    console.log(data)
    $.ajax({
        type:'POST',
        data:data,
        url:'/maintain_monitor/maintain-monitor-info/',
        beforeSend :function(xmlHttp){
                xmlHttp.setRequestHeader("If-Modified-Since","0");
                xmlHttp.setRequestHeader("Cache-Control","no-cache");
            },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                main_monitor();
            }else{
                alert(result['message'])
            }
        }
    })
}

//定义查询的数据的函数的全局变量
var NG_query = {}
//NG率监控的页面的数据的分页显示效果函数
var page_train = {'page':'1','num':'10'}
//选择一页显示数量
$(document).ready(function(){
     $("#setup_maintainer").change(function(){
        var page_train_number = $(this).children('option:selected').val()
        page_train['num']=page_train_number.toString()
        page_train['page'] = '1'
        if(page_train_number == 'All'){
            $("#mon_previous").parent().addClass("disabled")
            $("#mon_next").parent().addClass("disabled")
        }
        if(page_train_number != 'All'){
            $("#mon_previous").parent().removeClass("disabled")
            $("#mon_next").parent().removeClass("disabled")
        }
        if(page_train['page'] == '1'){
            $("#mon_previous").parent().addClass("disabled")
        }
        if(JSON.stringify(NG_query) == '{}' && JSON.stringify(visual_monitor_post) == '{}'){
            main_monitor_ajax()
        }
        if(JSON.stringify(NG_query) != '{}' && JSON.stringify(visual_monitor_post) == '{}'){
//            main_m_query();
            main_m_query_ajax();
        }
        if(JSON.stringify(NG_query) != '{}' && JSON.stringify(visual_monitor_post) != '{}'){
            maintain_monitor_visual(visual_monitor_post['status']);
        }
     })
})
//上一页页码的转换
function Maintainer_previous(){
    if(page_train['page'] != '1' && page_train['num'] != 'All'){
        page_train['page']= (Number(page_train['page'])-1).toString()
        $("#mon_next").parent().removeClass("disabled")
        if(JSON.stringify(NG_query) == '{}' && JSON.stringify(visual_monitor_post) == '{}'){
            main_monitor_ajax();
        }
        if(JSON.stringify(NG_query) != '{}' && JSON.stringify(visual_monitor_post) == '{}'){
//            main_m_query();
            main_m_query_ajax();
        }
        if(JSON.stringify(NG_query) != '{}' && JSON.stringify(visual_monitor_post) != '{}'){
            maintain_monitor_visual(visual_monitor_post['status']);
        }
    }
    if(page_train['page'] == '1'){
        $("#mon_previous").parent().addClass("disabled")
    }
}
//下一页的页面转换
function Maintainer_Next(){
    if(page_train['num'] != 'All'){
        page_train['page']= (Number(page_train['page'])+1).toString()
        $("#mon_previous").parent().removeClass("disabled")
        if(JSON.stringify(NG_query) == '{}' && JSON.stringify(visual_monitor_post) == '{}'){
            main_monitor_ajax();
        }
        if(JSON.stringify(NG_query) != '{}' && JSON.stringify(visual_monitor_post) == '{}'){
//            main_m_query();
            main_m_query_ajax();
        }
        if(JSON.stringify(NG_query) != '{}' && JSON.stringify(visual_monitor_post) != '{}'){
            maintain_monitor_visual(visual_monitor_post['status']);
        }
    }
}

////设备保养监控获取的函数 主页的目录切换控制
function main_monitor(){
    $(".main_monitor").removeClass("yc")
    $(".user").addClass("yc")
    $(".ng").addClass("yc")
    $(".budgetform").addClass("yc")
    $(".merge").addClass("yc")
    $(".detail").addClass("yc")
    $(".maintain").addClass("yc")
    $(".statistic").addClass("yc")
    $(".modifypwd").addClass("yc")
    $(".budget").addClass("yc")
    $("#main_eq_data")[0].reset();
    //初始化界面的设定页码：
    NG_query = {};
    visual_monitor_post = {};
    page_train = {'page':'1','num':'10'}
    $("#setup_maintainer").val(10);
     $.ajax({
    'type':'GET',
    'data':page_train,
    'url':'/maintain_monitor/maintain-monitor-info/',
    beforeSend :function(xmlHttp){
                xmlHttp.setRequestHeader("If-Modified-Since","0");
                xmlHttp.setRequestHeader("Cache-Control","no-cache");
            },
     success:function(result){
            if(result['code'] === 200){
                $("#m_monitor").empty();
                maintain_get_data = result['data']
                console.log(maintain_get_data)
                maintain_data = maintain_get_data.data
                //时间传输
                start_end=(result['data'].select_end.split('T'))[0]
                start_time=(result['data'].select_start.split('T'))[0]
                //饼状图需要的函数调用，输入数据
                monitor(maintain_get_data.normal,maintain_get_data.warning,maintain_get_data.danger,maintain_get_data.None,start_time,start_end);
                //柱状图需要的函数调用，输入数据;
                monitor_name(maintain_get_data.tab_data);

                for(var i=0; i<maintain_data.length; i++){
                    if(maintain_data[i].Maintainer == null){maintain_data[i].Maintainer = ""}
                    if(maintain_data[i].NextCheckDate == null){maintain_data[i].NextCheckDate =""}else{
                    maintain_data[i].NextCheckDate = (maintain_data[i].NextCheckDate).split("T")[0]}
                    var status
                    var status_class
                    if(maintain_data[i].stand == 'none'){
                        status = "未设定"
                        status_class = "badge badge-info";
                    }
                    if(maintain_data[i].stand == 'normal'){
                        status = "正常"
                        status_class = "badge badge-success";
                    }
                    if(maintain_data[i].stand == "warning"){
                        status = "预警"
                        status_class = "badge badge-warning";
                    }
                    if(maintain_data[i].stand == "danger"){
                        status = "超标"
                        status_class = "badge badge-danger";
                    }
                    var maintain_add = "<tr>"
                    +"<td class=\"yc\">"+maintain_data[i].Id+"</td>"
                    +"<td>"+maintain_data[i].SN+"</td>"
                    +"<td>"+maintain_data[i].PartName+"</td>"
                    +"<td>"+maintain_data[i].CheckCycleCount+"</td>"
                    +"<td>"+maintain_data[i].UsedTimes+"</td>"
                    +"<td>"+maintain_data[i].CheckCycle+"</td>"
                    +"<td>"+maintain_data[i].NextCheckDate+"</td>"
                    +"<td>"+maintain_data[i].Maintainer+"</td>"
                    +"<td><span class='"+status_class+"'>"+status+"</span></td>"
                    +"<td>"+maintain_data[i].location+"</td>"
                    +"</tr>"
                    $("#m_monitor").append(maintain_add)
                }

                data_count = result['data'].page_count
                if(page_train['page'] == '1' ){
                    $("#mon_previous").parent().addClass("disabled")
                }
                if(Number(page_train['page']) == data_count ){
                    $("#mon_next").parent().addClass("disabled")
                }
                if(Number(page_train['page'])<data_count){
                    $("#mon_next").parent().removeClass("disabled")
                }
                if(Number(page_train['page'])>data_count && data_count>1){
                    page_train['page']='1'
                    $("#mon_previous").parent().addClass("disabled")
                    $("#mon_next").parent().removeClass("disabled")
                }
            }else{
                $("#m_monitor").empty()
                $("#mon_previous").parent().addClass("disabled")
                $("#mon_next").parent().addClass("disabled")
            }
        }
    })
}
function main_monitor_ajax(){
    $.ajax({
    'type':'GET',
    'data':page_train,
    'url':'/maintain_monitor/maintain-monitor-info/',
    beforeSend :function(xmlHttp){
                xmlHttp.setRequestHeader("If-Modified-Since","0");
                xmlHttp.setRequestHeader("Cache-Control","no-cache");
            },
     success:function(result){
            if(result['code'] === 200){
                $("#m_monitor").empty();
                maintain_get_data = result['data']
                console.log(maintain_get_data)
                maintain_data = maintain_get_data.data
                //时间传输
                start_end=(result['data'].select_end.split('T'))[0]
                start_time=(result['data'].select_start.split('T'))[0]
                for(var i=0; i<maintain_data.length; i++){
                    if(maintain_data[i].Maintainer == null){maintain_data[i].Maintainer = ""}
                    if(maintain_data[i].NextCheckDate == null){maintain_data[i].NextCheckDate =""}else{
                    maintain_data[i].NextCheckDate = (maintain_data[i].NextCheckDate).split("T")[0]}
                    var status
                    var status_class
                    if(maintain_data[i].stand == 'none'){
                        status = "未设定"
                        status_class = "badge badge-info";
                    }
                    if(maintain_data[i].stand == 'normal'){
                        status = "正常"
                        status_class = "badge badge-success";
                    }
                    if(maintain_data[i].stand == "warning"){
                        status = "预警"
                        status_class = "badge badge-warning";
                    }
                    if(maintain_data[i].stand == "danger"){
                        status = "超标"
                        status_class = "badge badge-danger";
                    }
                    var maintain_add = "<tr>"
                    +"<td class=\"yc\">"+maintain_data[i].Id+"</td>"
                    +"<td>"+maintain_data[i].SN+"</td>"
                    +"<td>"+maintain_data[i].PartName+"</td>"
                    +"<td>"+maintain_data[i].CheckCycleCount+"</td>"
                    +"<td>"+maintain_data[i].UsedTimes+"</td>"
                    +"<td>"+maintain_data[i].CheckCycle+"</td>"
                    +"<td>"+maintain_data[i].NextCheckDate+"</td>"
                    +"<td>"+maintain_data[i].Maintainer+"</td>"
                    +"<td><span class='"+status_class+"'>"+status+"</span></td>"
                    +"<td>"+maintain_data[i].location+"</td>"
                    +"</tr>"
                    $("#m_monitor").append(maintain_add)
                }

                data_count = result['data'].page_count
                if(page_train['page'] == '1' ){
                    $("#mon_previous").parent().addClass("disabled")
                }
                if(Number(page_train['page']) == data_count ){
                    $("#mon_next").parent().addClass("disabled")
                }
                if(Number(page_train['page'])<data_count){
                    $("#mon_next").parent().removeClass("disabled")
                }
                if(Number(page_train['page'])>data_count && data_count>1){
                    page_train['page']='1'
                    $("#mon_previous").parent().addClass("disabled")
                    $("#mon_next").parent().removeClass("disabled")
                }
            }else{
                 $("#m_monitor").empty()
                $("#mon_previous").parent().addClass("disabled")
                $("#mon_next").parent().addClass("disabled")
            }
        }
    })
}

//查询之前做页码初始化的设定
function monitor_initial_page(){
    page_train={'page':'1','num':'10'};
    $("#setup_maintainer").val(10);
    visual_monitor_post = {};
    $.ajax({
        type:"GET",
        url:'/maintain/maintain-location/',
        success:function(result){
            if(result['code'] === 200){
                var select_location = $("#main_query_location option:selected").text()
                console.log(result['data'])
                console.log(select_location)
                data=result['data']
                $("#main_query_location").empty()
                $("#main_query_location").append('<option value=""></option>')
                for(var i=0; i<data.length; i++){
                    if(select_location == data[i].Location){
                        var local1 = "<option value="+data[i].Id+" selected>"+data[i].Location+"</option>"
                    }else{
                        var local2 = "<option value="+data[i].Id+">"+data[i].Location+"</option>"
                    }
                    $("#main_query_location").append(local1)
                    $("#main_query_location").append(local2)
                }
            }else{
                alert(result['message'])
            }
        }
    })
}

//对设备保养监控的查询数据函数
function main_m_query(){
    var s_time = $("#main_start_time").val()
    var e_time = $("#main_end_time").val()
    var sn = $("#main_query_sn").val()
    var partname = $("#main_query_partname").val()
    var user = $("#main_query_user").val()
    var status= $("#main_query_status").val()
    var location= $("#main_query_location").val()
    var start_time=""
    var start_end=""
    if(sn=="" && partname=="" && status=="" && s_time =="" && e_time =="" && user ==""){
        NG_query = {};
        main_monitor();
        return false;
    }
    if(s_time !=""){start_time =s_time}//else{start_time=""}
    if(e_time !=""){
        start_end=e_time
        e_time = e_time+" 23:59:59";
    }//else{start_end =""}
    partname= partname.toUpperCase();
    data = {
        'sn':sn,
        'partname':partname,
        'status':status,
        's_time':s_time,
        'e_time':e_time,
        'user':user,
        'location':location,
    }
    console.log(data)
    console.log(start_time,start_end)
    data['page'] = page_train['page']
    data['num'] = page_train['num']
    NG_query=data
    $.ajax({
    type:'POST',
    data:data,
    url:'/maintain_monitor/maintain-query/',
        success:function(result){
            if(result['code'] === 200){
                $("#m_monitor").empty();
                maintain_get_data = result['data']

                console.log(maintain_get_data)
                monitor(maintain_get_data.normal,maintain_get_data.warning,maintain_get_data.danger,maintain_get_data.None,start_end,start_time);
                monitor_name(maintain_get_data.tab_data);

                maintain_data =maintain_get_data.data
                for(var i=0; i<maintain_data.length; i++){
                    if(maintain_data[i].Maintainer == null){maintain_data[i].Maintainer = ""}
                    if(maintain_data[i].NextCheckDate == null){maintain_data[i].NextCheckDate =""}else{
                    maintain_data[i].NextCheckDate = (maintain_data[i].NextCheckDate).split("T")[0]}
                    var status
                    var status_class
                    if(maintain_data[i].stand == "normal"){
                        status = "正常"
                        status_class = "badge badge-success";
                    }
                    if(maintain_data[i].stand == "warning"){
                        status = "预警"
                        status_class = "badge badge-warning";
                    }
                    if(maintain_data[i].stand == "danger"){
                        status = "超标"
                        status_class = "badge badge-danger";
                    }
                    if(maintain_data[i].stand == "none"){
                        status = "未设定"
                        status_class = "badge badge-info";
                    }
                    var maintain_add = "<tr>"
                    +"<td class=\"yc\">"+maintain_data[i].Id+"</td>"
                    +"<td>"+maintain_data[i].SN+"</td>"
                    +"<td>"+maintain_data[i].PartName+"</td>"
                    +"<td>"+maintain_data[i].CheckCycleCount+"</td>"
                    +"<td>"+maintain_data[i].UsedTimes+"</td>"
                    +"<td>"+maintain_data[i].CheckCycle+"</td>"
                    +"<td>"+maintain_data[i].NextCheckDate+"</td>"
                    +"<td>"+maintain_data[i].Maintainer+"</td>"
                    +"<td><span class='"+status_class+"'>"+status+"</span></td>"
                    +"<td>"+maintain_data[i].location+"</td>"
                    +"</tr>"
                    $("#m_monitor").append(maintain_add)
                }

                data_count = result['data'].page_count
                if(page_train['page'] == '1' ){
                    $("#mon_previous").parent().addClass("disabled")
                }
                if(Number(page_train['page']) == data_count ){
                    $("#mon_next").parent().addClass("disabled")
                }
                if(Number(page_train['page'])<data_count){
                    $("#mon_next").parent().removeClass("disabled")
                }
                if(Number(page_train['page'])>data_count && data_count>1){
                    page_train['page']='1'
                    $("#mon_previous").parent().addClass("disabled")
                    $("#mon_next").parent().removeClass("disabled")
                }
            }else{
                alert(result['message'])
                $("#mon_next").parent().addClass("disabled")
            }
        }
    })
}
function main_m_query_ajax(){
    var s_time = $("#main_start_time").val()
    var e_time = $("#main_end_time").val()
    var sn = $("#main_query_sn").val()
    var partname = $("#main_query_partname").val()
    var user = $("#main_query_user").val()
    var status= $("#main_query_status").val()
    var location= $("#main_query_location").val()
    var start_time=""
    var start_end=""
    if(sn=="" && partname=="" && status=="" && s_time =="" && e_time =="" && user ==""){
        NG_query = {};
        main_monitor();
        return false;
    }
    if(s_time !=""){start_time =s_time}//else{start_time=""}
    if(e_time !=""){
        start_end=e_time
        e_time = e_time+" 23:59:59";
    }//else{start_end =""}
    partname= partname.toUpperCase();
    data = {
        'sn':sn,
        'partname':partname,
        'status':status,
        's_time':s_time,
        'e_time':e_time,
        'user':user,
        'location':location,
    }
    console.log(data)
    console.log(start_time,start_end)
    data['page'] = page_train['page']
    data['num'] = page_train['num']
    NG_query=data
    $.ajax({
    type:'POST',
    data:data,
    url:'/maintain_monitor/maintain-query/',
        success:function(result){
            if(result['code'] === 200){
                $("#m_monitor").empty();
                maintain_get_data = result['data']
                console.log(maintain_get_data)
                maintain_data =maintain_get_data.data
                for(var i=0; i<maintain_data.length; i++){
                    if(maintain_data[i].Maintainer == null){maintain_data[i].Maintainer = ""}
                    if(maintain_data[i].NextCheckDate == null){maintain_data[i].NextCheckDate =""}else{
                    maintain_data[i].NextCheckDate = (maintain_data[i].NextCheckDate).split("T")[0]}
                    var status
                    var status_class
                    if(maintain_data[i].stand == "normal"){
                        status = "正常"
                        status_class = "badge badge-success";
                    }
                    if(maintain_data[i].stand == "warning"){
                        status = "预警"
                        status_class = "badge badge-warning";
                    }
                    if(maintain_data[i].stand == "danger"){
                        status = "超标"
                        status_class = "badge badge-danger";
                    }
                    if(maintain_data[i].stand == "none"){
                        status = "未设定"
                        status_class = "badge badge-info";
                    }
                    var maintain_add = "<tr>"
                    +"<td class=\"yc\">"+maintain_data[i].Id+"</td>"
                    +"<td>"+maintain_data[i].SN+"</td>"
                    +"<td>"+maintain_data[i].PartName+"</td>"
                    +"<td>"+maintain_data[i].CheckCycleCount+"</td>"
                    +"<td>"+maintain_data[i].UsedTimes+"</td>"
                    +"<td>"+maintain_data[i].CheckCycle+"</td>"
                    +"<td>"+maintain_data[i].NextCheckDate+"</td>"
                    +"<td>"+maintain_data[i].Maintainer+"</td>"
                    +"<td><span class='"+status_class+"'>"+status+"</span></td>"
                    +"<td>"+maintain_data[i].location+"</td>"
                    +"</tr>"
                    $("#m_monitor").append(maintain_add)
                }

                data_count = result['data'].page_count
                if(page_train['page'] == '1' ){
                    $("#mon_previous").parent().addClass("disabled")
                }
                if(Number(page_train['page']) == data_count ){
                    $("#mon_next").parent().addClass("disabled")
                }
                if(Number(page_train['page'])<data_count){
                    $("#mon_next").parent().removeClass("disabled")
                }
                if(Number(page_train['page'])>data_count && data_count>1){
                    page_train['page']='1'
                    $("#mon_previous").parent().addClass("disabled")
                    $("#mon_next").parent().removeClass("disabled")
                }
            }else{
                alert(result['message'])
                $("#mon_next").parent().addClass("disabled")
            }
        }
    })
}

//生成保养报表的数据函数
function maintain_file(){
    //下载当前数据
//    var maintain_li = $("#m_monitor tr").length
//    var maintain_data = []
//    for(var j=0; j<maintain_li; j++){
//        value = $("#m_monitor tr").eq(j).find("td:first").html();
//        maintain_data.push(value)
//    }
//    data ={'maintain_id':maintain_data,}
//    console.log(data)
//    $.ajax({
//    'type':'POST',
//    'data':data,
//    'url':'/maintain_monitor/maintain-record/',
//        success:function(result){
//            if(result['code'] === 200){
//                window.location.href = result['data'][0]
//            }else{
//                window.message.showError(result['message'])
//            }
//        }
//    })
    //下载筛选的数据

    var s_time = $("#main_start_time").val()
    var e_time = $("#main_end_time").val()
    var sn = $("#main_query_sn").val()
    var partname = $("#main_query_partname").val()
    var user = $("#main_query_user").val()
    var status= $("#main_query_status").val()
    var location= $("#main_query_location").val()
    if(e_time !=""){e_time = e_time+" 23:59:59";}
    partname= partname.toUpperCase();
    data = {
        'sn':sn,
        'partname':partname,
        'status':status,
        's_time':s_time,
        'e_time':e_time,
        'user':user,
        'location':location,
    }
    if(JSON.stringify(data) == '{}'){ return false;alert("need select value")}
    console.log(data)
    $('#mask_div').show_mask();
    $.ajax({
        'type':'POST',
        'data':data,
        'url':'/maintain_monitor/maintain-record/',
        success:function(result){
            if(result['code'] === 200){
                window.location.href = result['data'][0]
            }else{
                window.message.showError(result['message'])
            }
            $('#mask_div').hide_mask();
        }
//        $('#mask_div').hide_mask();
    })
}

//设备保养的视图的点击事件
var visual_monitor_post ={}
//提供设备保养的视图的点击事件的函数定义， 也是调用函数。。
function maintain_monitor_visual(color){
    visual_monitor_post = NG_query
    visual_monitor_post['status']=color
    visual_monitor_post['page']=page_train['page']
    visual_monitor_post['num']=page_train['num']
    console.log(visual_monitor_post)
    $.ajax({
        'type':'POST',
        'data':visual_monitor_post,
        'url':'/maintain_monitor/maintain-monitor-visual/',
        success:function(result){
            if(result['code'] === 200){
                $("#m_monitor").empty();
                maintain_get_data = result['data']
                console.log(maintain_get_data)
                maintain_data =maintain_get_data.data
                //柱状图需要的函数调用，输入数据;
                monitor_name(maintain_get_data.tab_data);
                for(var i=0; i<maintain_data.length; i++){
                       if(maintain_data[i].Maintainer == null){maintain_data[i].Maintainer = ""}
                    if(maintain_data[i].NextCheckDate == null){maintain_data[i].NextCheckDate =""}else{
                    maintain_data[i].NextCheckDate = (maintain_data[i].NextCheckDate).split("T")[0]}
                    var status
                    var status_class
                    if(maintain_data[i].stand == "normal"){
                        status = "正常"
                        status_class = "badge badge-success";
                    }
                    if(maintain_data[i].stand == "warning"){
                        status = "预警"
                        status_class = "badge badge-warning";
                    }
                    if(maintain_data[i].stand == "danger"){
                        status = "超标"
                        status_class = "badge badge-danger";
                    }
                    if(maintain_data[i].stand == "none"){
                        status = "未设定"
                        status_class = "badge badge-info";
                    }
                    var maintain_add = "<tr>"
                    +"<td class=\"yc\">"+maintain_data[i].Id+"</td>"
                    +"<td>"+maintain_data[i].SN+"</td>"
                    +"<td>"+maintain_data[i].PartName+"</td>"
                    +"<td>"+maintain_data[i].CheckCycleCount+"</td>"
                    +"<td>"+maintain_data[i].UsedTimes+"</td>"
                    +"<td>"+maintain_data[i].CheckCycle+"</td>"
                    +"<td>"+maintain_data[i].NextCheckDate+"</td>"
                    +"<td>"+maintain_data[i].Maintainer+"</td>"
                    +"<td><span class='"+status_class+"'>"+status+"</span></td>"
                    +"<td>"+maintain_data[i].location+"</td>"
                    +"</tr>"
                    $("#m_monitor").append(maintain_add)
                }

                data_count = result['data'].page_count
                if(page_train['page'] == '1' ){
                    $("#mon_previous").parent().addClass("disabled")
                }
                if(Number(page_train['page']) == data_count ){
                    $("#mon_next").parent().addClass("disabled")
                }
                if(Number(page_train['page'])<data_count){
                    $("#mon_next").parent().removeClass("disabled")
                }
                if(Number(page_train['page'])>data_count && data_count>1){
                    page_train['page']='1'
                    $("#mon_previous").parent().addClass("disabled")
                    $("#mon_next").parent().removeClass("disabled")
                }
            }else{
                $("#mon_next").parent().addClass("disabled")
                $("#mon_previous").parent().addClass("disabled")
                alert(result['message'])
            }
        }
    })
}

