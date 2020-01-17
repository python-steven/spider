//设备保养得数据分页
var page_maintain = {'page':'1','num':'10'}
//选择一页显示数量
$(document).ready(function(){
     $("#setup_main").change(function(){
        var page_main_num = $(this).children('option:selected').val()
        page_maintain['num']=page_main_num.toString()
        page_maintain['page'] = '1'
        if(page_main_num == 'All'){
            $("#previous_m").parent().addClass("disabled")
            $("#next_m").parent().addClass("disabled")
        }
        if(page_main_num != 'All'){
            $("#previous_m").parent().removeClass("disabled")
            $("#next_m").parent().removeClass("disabled")
        }
        if(page_maintain['page'] == '1'){
            $("#previous_m").parent().addClass("disabled")
        }
        if(JSON.stringify(query_information) == '{}'){
            maintain_ajax();
        }else{
            maintain_query();
        }
     })
})
//上一页页码的转换
function previous_main(){
    if(page_maintain['page'] != '1' && page_maintain['num'] != 'All'){
        page_maintain['page']= (Number(page_maintain['page'])-1).toString()
        $("#next_m").parent().removeClass("disabled")
        if(JSON.stringify(query_information) == '{}'){
            maintain_ajax();
        }else{
            maintain_query();
        }
    }
    if(page_maintain['page'] == '1'){
        $("#previous_m").parent().addClass("disabled")
    }
}
//下一页的页面转换
function next_main(){
    if(page_maintain['num'] != 'All'){
        page_maintain['page']= (Number(page_maintain['page'])+1).toString()
        $("#previous_m").parent().removeClass("disabled")
        if(JSON.stringify(query_information) == '{}'){
            maintain_ajax();
        }else{
            maintain_query();
        }
    }
}

//获取数据的加载main_monitor
function maintain(){
    $(".maintain").removeClass("yc")
    $(".budget").addClass("yc")
    $(".user").addClass("yc")
    $(".budgetform").addClass("yc")
    $(".merge").addClass("yc")
    $(".detail").addClass("yc")
    $(".ng").addClass("yc")
    $(".statistic").addClass("yc")
    $(".modifypwd").addClass("yc")
    $(".main_monitor").addClass("yc")
    $(".result").addClass("yc")
    $("#main_query_select")[0].reset();

    if(JSON.stringify(query_information) != '{}'){
    query_information={}
    }
    page_maintain = {'page':'1','num':'10'}
    maintain_ajax();

}
function maintain_ajax(){
    $.ajax({
        'type':'GET',
        'data':page_maintain,
        'url':'/maintain/maintain-equipment-info/',
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            var Spec_title =""
            if(result['code'] === 200){
                $("#maintain_tr").empty();
                maintain_data = result['data'].data
                console.log(maintain_data)
                for(var i=0; i<maintain_data.length; i++){
//                    if(maintain_data[i].Location== null){(maintain_data[i].Location=""}
                    if(maintain_data[i].NextCheckDate == null){
                        maintain_data[i].NextCheckDate =""
                    }else{
                        maintain_data[i].NextCheckDate = (maintain_data[i].NextCheckDate).split("T")[0]
                    }
                    if(maintain_data[i].Maintainer == null){maintain_data[i].Maintainer = ""}

                    var equip_spec =  maintain_data[i].Spec;
                    if(equip_spec && equip_spec.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_spec = equip_spec.substring(0,10);
                        equip_spec_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_spec +"\">" + sub_equip_spec + ellipsis + "</span>";
                    }
                    else
                        equip_spec_show = equip_spec;

                    var maintain_add = "<tr>"
                    +"<td class='yc'>"+maintain_data[i].Id+"</td>"
                    +"<td><span data-toggle='modal' data-target='#maintain_sn' onclick='maintain_sn($(this))'>"
                    +"<img alt='Add' src='/static/images/icon_modify.gif' style='padding-right:10px;'></span></td>"
                    +"<td>"+maintain_data[i].SN+"</td>"
                    +"<td>"+maintain_data[i].PN+"</td>"
                    +"<td>"+maintain_data[i].PartName+"</td>"
                    +"<td>"+equip_spec_show+"</td>"
                    +"<td>"+maintain_data[i].CheckCycleCount+"</td>"
                    +"<td>"+maintain_data[i].UsedTimes+"</td>"
                    +"<td>"+maintain_data[i].CheckCycle+"</td>"
                    +"<td>"+maintain_data[i].NextCheckDate+"</td>"
                    +"<td>"+maintain_data[i].Maintainer+"</td>"
                    +"<td>"+maintain_data[i].Location+"</td>"
                    +"<td>"+Status_CN_ENG(maintain_data[i].UseStatus)+"</td>"
                    +"</tr>"
                    $("#maintain_tr").append(maintain_add)
                    popover_show();
                }

                data_count = result['data'].page_count
                if(page_maintain['page'] == '1'){
                    $("#previous_m").parent().addClass("disabled")
                }
                if(Number(page_maintain['page']) == data_count){
                    $("#next_m").parent().addClass("disabled")
                }
                if(Number(page_maintain['page']) < data_count){
                    $("#next_m").parent().removeClass("disabled")
                }
            }else{
                $("#next_m").parent().addClass("disabled")
                $("#previous_m").parent().addClass("disabled")
            }
        }
    })
}


function query_maintain_selector(){
    page_maintain = {'page':'1','num':'10'};
    $("#setup_main").val(10);

}
//定义全局的查询变量
var query_information={}
//筛选功能的实现运用
function maintain_query(){
    var main_start_time = $("#maintain_start_time").val()
    var main_end_time = $("#maintain_end_time").val()
    var main_sn = $("#maintain_q_sn").val()
    var main_partname = $("#maintain_q_partname").val()
    var main_user = $("#maintain_q_user").val()

    var main_location = $("#maintain_q_location").val()
    var main_UseStatus = $("#maintain_q_UseStatus").val()

    if(main_start_time=="" && main_end_time=="" && main_sn=="" && main_partname =="" && main_user ==""){
        query_information = {}
    }
    if(main_start_time == main_end_time && main_start_time !="" && main_end_time !=""){
        main_end_time = main_end_time+" 23:59:59";
    }
    main_partname= main_partname.toUpperCase();
    data = {
        'main_start_time':main_start_time,
        'main_end_time':main_end_time,
        'main_sn':main_sn,
        'main_partname':main_partname,
        'main_user':main_user,
        'main_location':main_location,
        'main_UseStatus':main_UseStatus,
    }
    query_information=data //这里是把筛选的条件变成全局条件给视图查询做准备
    data['page']=page_maintain['page']
    data['num']=page_maintain['num']
    console.log(data)
    $.ajax({
    'type':'POST',
    'data':data,
    'url':'/maintain/maintain-query-partname-data/',
        success:function(result){
        var Spec_title=""
            if(result['code'] === 200){
                console.log(result['data'])
                $("#maintain_tr").empty();
                maintain_data = result['data'].data

                for(var i=0; i<maintain_data.length; i++){
                    if(maintain_data[i][8] == null){maintain_data[i][8] =""}else{
                    maintain_data[i][8] = (maintain_data[i][8]).split("T")[0]}
                    if(maintain_data[i][9] == null){maintain_data[i][9] =""}
                    var equip_spec =  maintain_data[i][4];
                    if(equip_spec && equip_spec.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_spec = equip_spec.substring(0,10);
                        equip_spec_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_spec +"\">" + sub_equip_spec + ellipsis + "</span>";
                    }
                    else
                        equip_spec_show = equip_spec;
                    var maintain_add = "<tr>"
                    +"<td class='yc'>"+maintain_data[i][0]+"</td>"
                    +"<td><span data-toggle='modal' data-target='#maintain_sn' onclick='maintain_sn($(this))'>"
                    +"<img alt='Add' src='/static/images/icon_modify.gif' style='padding-right:10px;'></span></td>"
                    +"<td>"+maintain_data[i][1]+"</td>"
                    +"<td>"+maintain_data[i][2]+"</td>"
                    +"<td>"+maintain_data[i][3]+"</td>"
                    +"<td>"+equip_spec_show+"</td>"
                    +"<td>"+maintain_data[i][5]+"</td>"
                    +"<td>"+maintain_data[i][6]+"</td>"
                    +"<td>"+maintain_data[i][7]+"</td>"
                    +"<td>"+maintain_data[i][8]+"</td>"
                    +"<td>"+maintain_data[i][9]+"</td>"
                    +"<td>"+maintain_data[i][12]+"</td>"
                    +"<td>"+Status_CN_ENG(maintain_data[i][11])+"</td>"
                    +"</tr>"
                    $("#maintain_tr").append(maintain_add)
                    popover_show();
                }

                data_count = result['data'].page_count
                if(page_maintain['page'] == '1' && data_count<=1){
                    $("#previous_m").parent().addClass("disabled")
                    $("#next_m").parent().addClass("disabled")
                }
                if(Number(page_maintain['page']) == data_count ){
                    $("#next_m").parent().addClass("disabled")
                }
                if(Number(page_maintain['page']) < data_count ){
//                    $("#previous_m").parent().addClass("disabled")
                    $("#next_m").parent().removeClass("disabled")
                }
                if(Number(page_maintain['page']) > data_count && data_count>1){
                    $("#previous_m").parent().addClass("disabled")
                    $("#next_m").parent().removeClass("disabled")
                }

            }else{
//                window.message.showError(result['message'])
                $("#maintain_tr").empty();
                $("#next_m").parent().addClass("disabled")
            }
        }
    })


}
////针对某一个BY_PN进行修改动作的设定参数
function setup_by_PN(){
    var main_partname = $("#setup_main_partname").val()
    if($("#rt_count").is(":checked")){
        var main_count =    $("#setup_main_count").val()
    }else{var main_count = ""}
    if($("#rt_day").is(":checked")){
        var main_day =      $("#setup_main_day").val()
    }else{var main_day = ""}
    if($("#rt_date").is(":checked")){
        var main_date =     $("#setup_main_date").val()
    }else{var main_date = ""}
    if($("#rt_user").is(":checked")){
        var main_user =     $("#setup_main_user").val()
    }else{var main_user = ""}

    if($("#rt_days").is(":checked")){
        var main_days =     $("#setup_main_days").val()
    }else{var main_days = ""}
    if($("#rt_times").is(":checked")){
        var main_times =     $("#setup_main_times").val()
    }else{var main_times = ""}
    if($("#rt_maintainers").is(":checked")){
        var main_maintainers =$("#setup_main_maintainers").val()
    }else{var main_maintainers = ""}
    var Regx =  /^[0-9]*$/;
    if(main_partname == ""){
        window.message.showError("PN can't empty")
        return false;
    }
    if(main_count =="" && main_day =="" && main_date =="" && main_user =="" && main_days ==""&& main_times ==""&& main_maintainers ==""){
        window.message.showError("only for one value for PN")
        return false;
    }
    if(!Regx.test(main_count)){
        alert("maintain count is digital")
        return false;
    }
    if(!Regx.test(main_day)){
        alert("maintain cycle is digital")
        return false;
    }
    if(!Regx.test(main_days)){
        alert("maintain days is digital")
        return false;
    }
    if(!Regx.test(main_times)){
        alert("maintain times is digital")
        return false;
    }
//    if(Regx.test(main_count) && Regx.test(main_day)){
    data={
    'main_partname':main_partname,
    'main_count':main_count,
    'main_day':main_day,
    'main_date':main_date,
    'main_user':main_user,
    'main_days':main_days,
    'main_times':main_times,
    'main_maintainers':main_maintainers,
    }
    console.log(data)
    $.ajax({
    'type':'POST',
    'data':data,
    'url':'/maintain/maintain-setup-by-pn/',
    beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
    success:function(result){
        if(result['code'] === 200){
            maintain();
            window.message.showSuccess(result['message'])
        }else{
            window.message.showError(result['message'])
        }
    }
    })

//    }else{
//        window.message.showError("main_count is digital")
//        return false;
//    }
}
//对一个做处理之前获取信息

function maintain_sn(obj){
     var id = obj.parent().parent().find("td").eq(2).text()
     $("#item_sn").html(id)
    data = {
        'SN':id,
    }
    $.ajax({
    'type':'POST',
    'data':data,
    'url':'/maintain/maintain-query-SN/',
        success:function(result){
            if(result['code'] === 200){
                data=result['data'][0]
                console.log(result['data'])
                $("#main_count").val(data.CheckCycleCount)
                $("#main_cycle").val(data.CheckCycle)
                $("#main_date").val(data.NextCheckDate.split('T')[0])
                $("#main_user").val(data.Maintainer)

            }else{
//            alert(result['message'])
            }
        }
    })
}
//针对一个SN的进行设置修改保养的次数和周期 下次保养的时间设定 第一个函数执行之后的设置作用。。
function setup_restart(){
    if($("#ret_count").is(":checked")){
        var main_count =    $("#main_count").val()
    }else{var main_count = ""}
    if($("#ret_day").is(":checked")){
        var main_cycle = $("#main_cycle").val()
    }else{var main_cycle = ""}
    if($("#ret_date").is(":checked")){
        var main_date = $("#main_date").val()
    }else{var main_date = ""}
    if($("#ret_user").is(":checked")){
        var main_user = $("#main_user").val()
    }else{var main_user = ""}

    if($("#ret_rdays").is(":checked")){
        var main_days = $("#main_days").val()
    }else{var main_days = ""}
    if($("#ret_rtimes").is(":checked")){
        var main_times = $("#main_times").val()
    }else{var main_times = ""}
    if($("#ret_maintainers").is(":checked")){
        var main_maintainers = $("#reset_maintainers").val()
    }else{var main_maintainers = ""}
    var main_sn = $("#item_sn").text()
    var Regx =  /^[0-9]*$/;
    var Regx =  /^[0-9]*$/;
    if(main_count =="" && main_cycle =="" && main_date =="" && main_user =="" && main_days ==""&& main_times ==""&& main_maintainers ==""){
        alert("no change of this info?")
        return false;
    }
    if(!Regx.test(main_days)){
        alert("days is digital")
        return false;
    }
    if(!Regx.test(main_times)){
        alert("times is digital")
        return false;
    }
    if(!Regx.test(main_count)){
        alert("maintain count is digital")
        return false;
    }
    if(!Regx.test(main_cycle)){
        alert("maintain cycle is digital")
        return false;
    }
//    if(Regx.test(main_count) && Regx.test(main_cycle)){
    data={
        'main_count':main_count,
        'main_cycle':main_cycle,
        'main_date':main_date,
        'main_sn':main_sn,
        'main_user':main_user,
        'main_days':main_days,
        'main_times':main_times,
        'main_maintainers':main_maintainers,
    }
    console.log(data)
    $.ajax({
    'type':'POST',
    'data':data,
    'url':'/maintain/maintain-setup-info/',
    beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
    success:function(result){
        if(result['code'] === 200){
            window.message.showSuccess(result['message'])
            maintain();
        }else{
           alert(result['message'])
        }
    }
    })

//    }else{
//        alert("main_count is digital")
//    }
}

//进入添加设备的页面的时候做添加动作的函数
function add_equipment(){
    var SN = $("#add_SN").val()
    var USN = $("#add_USN").val()
    var OSN = $("#add_OSN").val()
    var Asset = $("#add_Asset").val()
    var PN = $("#add_PN").val()
    var PartName = $("#add_PartName").val()
    var Spec = $("#add_spec").val()
    var CheckCycleCount = $("#add_main_count").val()
    var CheckCycle = $("#add_main_date").val()
    var UsedTimes = $("#add_usedtimes").val()
    var NextCheckDate = $("#add_next_main_date").val()
    var Maintainer = $("#add_Maintainer").val()
    var location = $("#location_select").val()
    var usestatus = $("#use_status").val()
    var maintain_days = $("#maintain_days").val()
    var maintain_times = $("#maintain_times").val()
    var maintainers = $("#user_select").val()
    var Regx =  /^[0-9]*$/;
    if(SN ==""){
        window.message.showError("SN can't empty")
        return false;
    }
    if(PN =="" ){
        window.message.showError("PN can't empty")
        return false;
    }
    if(PartName=="" ){
        window.message.showError("PartName can't empty")
        return false;
    }
    if(Spec == "" ){
        window.message.showError("Spec can't empty")
        return false;
    }
    if(UsedTimes == ""){
        window.message.showError("UsedTimes can't empty")
        return false;
    }
    if(location ==""){
        window.message.showError("location can't empty")
        return false;
    }
    if(!Regx.test(CheckCycleCount)){
        alert("CheckCycleCount is digital")
        return false;
    }
    if(!Regx.test(CheckCycle)){
        alert("CheckCycle days is digital")
        return false;
    }
    if(!Regx.test(maintain_days)){
        alert("maintain days is digital")
        return false;
    }
    if(!Regx.test(maintain_times)){
        alert("maintain times is digital")
        return false;
    }
    if((isNaN(NextCheckDate)&&!isNaN(Date.parse(NextCheckDate))) || NextCheckDate == ""){
    data = {
        'SN':SN,
        'USN':USN,
        'OSN':OSN,
        'Asset':Asset,
        'PN':PN,
        'PartName':PartName,
        'Spec':Spec,
        'CheckCycleCount':CheckCycleCount,
        'CheckCycle':CheckCycle,
        'UsedTimes':UsedTimes,
        'NextCheckDate':NextCheckDate,
        'Maintainer':Maintainer,
        'location':location,
        'usestatus':usestatus,
        'maintain_days':maintain_days,
        'maintain_times':maintain_times,
        'maintainers':maintainers,
    }
    console.log(data)
    $.ajax({
        type:"POST",
        data:data,
        url:'/maintain/maintain-add-equipment/',
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                add_log();
                li_active();
                document.getElementById("add_equipment_info").reset();
            }else{
                alert(result['message'])
            }
        }
    })
    }else{
        window.message.showError('maintain time need date')
    }
}
//表格导入数据的方式实现批量插入数据到DB里面
function openBrowse(){
    var ie = navigator.appName == "Microsoft Internet Explorer" ? true : false;
    if(ie){
        document.getElementById("file").click();
    }else{
        var a=document.createEvent("MouseEvents");//FF的处理
        a.initEvent("click", true, true);
        document.getElementById("file").dispatchEvent(a);
    }

}
//上传文件的数据实现批量的插入表格里面的数据
function add_equipment_file(){
    var formData=new FormData();
    var file = $("#file")[0].files[0]
    formData.append('file',file);
//    console.log(formData.get('file'))
    $('#mask_div').show_mask();
    $.ajax({
        type:'POST',
        url:'/maintain/maintain-add-equipment-ex/',
        data:formData,
        processData:false,
        contentType:false,
        success:function(result){
            if(result['code'] === 200){
                $(".result").removeClass("yc")
                $(".add_main").addClass("yc")
                $("#add_result").empty()
                add_data = result['data']
//                console.log(add_data)
                var status
                for(var i=0; i<add_data.length; i++){
                    if(add_data[i].PN == null){add_data[i].PN =""}
                    if(add_data[i].Spec == null){add_data[i].Spec =""}
                    if(add_data[i].CheckCycleCount == null){add_data[i].CheckCycleCount =""}
                    if(add_data[i].CheckCycle == null){add_data[i].CheckCycle =""}
                    if(add_data[i].Maintainer == null){add_data[i].Maintainer =""}
                    if(add_data[i].NextCheckDate == null){add_data[i].NextCheckDate =""}else{
                    add_data[i].NextCheckDate = add_data[i].NextCheckDate.split("T")[0]}
                    if(add_data[i].result == "Success"){
                        status = "green"
                    }else{
                        status = "red"
                    }
                    var equip_spec =  add_data[i].Spec;
                    if(equip_spec && equip_spec.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_spec = equip_spec.substring(0,10);
                        equip_spec_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_spec +"\">" + sub_equip_spec + ellipsis + "</span>";
                    }
                    else
                        equip_spec_show = equip_spec;
                    var maintain_add = "<tr>"
                    +"<td>"+add_data[i].SN+"</td>"
                    +"<td>"+add_data[i].PN+"</td>"
                    +"<td>"+equip_spec_show+"</td>"
                    +"<td>"+add_data[i].CheckCycleCount+"</td>"
                    +"<td>"+add_data[i].UsedTimes+"</td>"
                    +"<td>"+add_data[i].CheckCycle+"</td>"
                    +"<td>"+add_data[i].NextCheckDate+"</td>"
                    +"<td>"+add_data[i].Maintainer+"</td>"
                    +"<td><font size='0' color=\""+status+"\">"+add_data[i].result+"</font></td>"
                    +"</tr>"
                    $("#add_result").append(maintain_add)
                    popover_show();
                    $("#file").val("")
                }
            }else{
                alert(result['message'])
            }
            $('#mask_div').hide_mask();
        }
    })
}




//我添加的设备的页面的分页动作的展示部分
var page_log_add ={'page':'1','num':'10'}
$(document).ready(function(){
     $("#add_log_page_setup").change(function(){
        var page_num_log_add = $(this).children('option:selected').val()
        page_log_add['num']=page_num_log_add.toString()
        page_log_add['page'] = '1'
        if(page_num_log_add == 'All'){
            $("#previous_add_log").parent().addClass("disabled")
            $("#next_add_log").parent().addClass("disabled")
        }
        if(page_num_log_add != 'All'){
            $("#previous_add_log").parent().removeClass("disabled")
            $("#next_add_log").parent().removeClass("disabled")
        }
        if(page_log_add['page'] == '1'){
            $("#previous_add_log").parent().addClass("disabled")
        }
        if(JSON.stringify(add_log_query_data) == '{}'){
            add_log_ajax();
        }else{
            query_log_info();
        }
     })
})
//上一页页码的转换
function previous_add_log(){
    if(page_log_add['page'] != '1' && page_log_add['num'] != 'All'){
        page_log_add['page']= (Number(page_log_add['page'])-1).toString()
        $("#next_add_log").parent().removeClass("disabled")
        if(JSON.stringify(add_log_query_data) == '{}'){
            add_log_ajax();
        }else{
            query_log_info();
        }
    }
    if(page_log_add['page'] == '1'){
        $("#previous_add_log").parent().addClass("disabled")
    }
}
//下一页的页面转换
function next_add_log(){
    if(page_log_add['num'] != 'All'){
        page_log_add['page']= (Number(page_log_add['page'])+1).toString()
        $("#previous_add_log").parent().removeClass("disabled")
        if(JSON.stringify(add_log_query_data) == '{}'){
            add_log_ajax();
        }else{
            query_log_info();
        }
    }
}


//我添加的设备的页面的展示信息//设备保养操作界面切换
function add_log(){
    $(".add_log").removeClass("yc")
    $(".modify_log").addClass("yc")
    $(".query_log").addClass("yc")
    $(".add_main").addClass("yc")
    $(".maintain_index").addClass("yc")
    $(".operation").addClass("yc")
    $(".result").addClass("yc")
    $("#my_add_query")[0].reset();

    if(JSON.stringify(add_log_query_data) != '{}'){
        add_log_query_data = {}
    }
    page_log_add ={'page':'1','num':'10'}
    add_log_ajax();
}
function add_log_ajax(){
     $.ajax({
        type:'GET',
        url:'/maintain/maintain-add-equipment-log/',
        data:page_log_add,
        success:function(result){
            var OSN_title
            var Spec_title
            if(result['code'] === 200){
                $("#add_equipment_log").empty()
                add_data_info = result['data'].data
                console.log(add_data_info)
                for(var i=0; i<add_data_info.length; i++){
                    if(add_data_info[i].USN == null){add_data_info[i].USN =""}
                    if(add_data_info[i].OSN == null){add_data_info[i].OSN =""}
                    if(add_data_info[i].Asset == null){add_data_info[i].Asset =""}
                    if(add_data_info[i].Maintainer == null){add_data_info[i].Maintainer =""}
                    if(add_data_info[i].NextCheckDate == null){add_data_info[i].NextCheckDate =""}else{
                    add_data_info[i].NextCheckDate = add_data_info[i].NextCheckDate.split("T")[0]}
                    var equip_osn =  add_data_info[i].OSN;
                    if(equip_osn && equip_osn.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_osn = equip_osn.substring(0,10);
                        equip_osn_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_osn +"\">" + sub_equip_osn + ellipsis + "</span>";
                    }
                    else
                        equip_osn_show = equip_osn;
                    var equip_spec =  add_data_info[i].Spec;
                    if(equip_spec && equip_spec.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_spec = equip_spec.substring(0,10);
                        equip_spec_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_spec +"\">" + sub_equip_spec + ellipsis + "</span>";
                    }
                    else
                        equip_spec_show = equip_spec;
                    var maintain_add_log = "<tr>"
                    +'<td>'
                        +'<span onclick="modify_log($(this));"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                        +'<span data-toggle="modal" data-target="#delete_log" onclick="del_log();"><img  alt="Delete" src="/static/images/icon_del.gif"></span>'
                    +'</td>'
                    +'<td class="yc">'+add_data_info[i].Id+'</td>'
                    +"<td>"+add_data_info[i].SN+"</td>"
                    +"<td>"+add_data_info[i].USN+"</td>"
                    +"<td>"+equip_osn_show+"</td>"
                    +"<td>"+add_data_info[i].Asset+"</td>"
                    +"<td>"+add_data_info[i].PN+"</td>"
                    +"<td>"+add_data_info[i].PartName+"</td>"
                    +"<td>"+equip_spec_show+"</td>"
                    +"<td>"+add_data_info[i].CheckCycleCount+"</td>"
                    +"<td>"+add_data_info[i].CheckCycle+"</td>"
                    +"<td>"+add_data_info[i].UsedTimes+"</td>"
                    +"<td>"+add_data_info[i].NextCheckDate+"</td>"
                    +"<td>"+add_data_info[i].Maintainer+"</td>"
                    +"<td>"+add_data_info[i].Location+"</td>"
                    +"<td>"+Status_CN_ENG(add_data_info[i].UseStatus)+"</td>"
                    +"<td>"+add_data_info[i].WarningBeforeDays+"</td>"
                    +"<td>"+add_data_info[i].WarningBeforeTimes+"</td>"
                    +"<td>"+add_data_info[i].SubMaintainers+"</td>"
                    +"</tr>"
                    $("#add_equipment_log").append(maintain_add_log)
                    popover_show();
                }

                data_count = result['data'].page_count
                if(page_log_add['page'] == '1' ){
                    $("#previous_add_log").parent().addClass("disabled")
                }
                if(Number(page_log_add['page']) == data_count){
                    $("#next_add_log").parent().addClass("disabled")
                }
                if(Number(page_log_add['page']) < data_count){
                    $("#next_add_log").parent().removeClass("disabled")
                }
            }else{
                $("#add_equipment_log").empty()
                $("#next_add_log").parent().addClass("disabled")
                $("#previous_add_log").parent().addClass("disabled")
            }
        }
    })
}


//筛选之前先初始化
function query_log_equipment(){
    page_log_add={'page':'1','num':'10'}
    $("#add_log_page_setup").val(10)
    add_log_query_data = {}
}
//针对我添加的页面的展示部分的筛功能的实现
var add_log_query_data = {}
function query_log_info(){
    var log_s_time = $("#l_s_time").val()
    var log_e_time = $("#l_e_time").val()
    var log_SN = $("#l_SN").val()
    var log_PN = $("#l_PN").val()
    var log_Spec = $("#l_Spec").val()
    var log_PartName = $("#l_PartName").val()
    var log_maintainer = $("#l_Maintainer").val()
    var log_location = $("#l_location").val()
    var log_UseStatus = $("#l_UseStatus").val()
    if(log_s_time=="" && log_e_time=="" && log_SN=="" && log_PN =="" && log_Spec =="" && log_maintainer ==""&& log_PartName ==""&& log_location ==""&& log_UseStatus ==""){
        add_log_query_data = {}
        return false;
    }
    if(log_s_time == log_e_time && log_s_time !="" && log_e_time !=""){
        log_e_time = log_e_time+" 23:59:59";
    }
    log_Spec= log_Spec.toUpperCase();
    data = {
        'log_s_time':log_s_time,
        'log_e_time':log_e_time,
        'log_SN':log_SN,
        'log_PN':log_PN,
        'log_Spec':log_Spec,
        'log_PartName':log_PartName,
        'log_maintainer':log_maintainer,
        'log_location':log_location,
        'log_UseStatus':log_UseStatus,
    }
    console.log(data)
    add_log_query_data=data //这里是把筛选的条件变成全局条件给视图查询做准备
    data['page']=page_log_add['page']
    data['num']=page_log_add['num']
    $.ajax({
    type:'POST',
    data:data,
    url:'/maintain/maintain-query-my-log/',
        success:function(result){
            var OSN_title
            var Spec_title
            if(result['code'] === 200){
                $("#add_equipment_log").empty();
                data = result['data']
                console.log(data)
                maintain_log_data = result['data'].data
                console.log(maintain_log_data)
                for(var i=0; i<maintain_log_data.length; i++){
                    if(maintain_log_data[i][2] == null){maintain_log_data[i][2] = ""}
                    if(maintain_log_data[i][4] == null){maintain_log_data[i][4] = ""}
                    if(maintain_log_data[i][11] == null){maintain_log_data[i][11] = ""}

                    var equip_osn =  maintain_log_data[i][3];
                    if(equip_osn && equip_osn.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_osn = equip_osn.substring(0,10);
                        equip_osn_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_osn +"\">" + sub_equip_osn + ellipsis + "</span>";
                    }
                    else
                        equip_osn_show = equip_osn;
                    var equip_spec =  maintain_log_data[i][7];
                    if(equip_spec && equip_spec.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_spec = equip_spec.substring(0,10);
                        equip_spec_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_spec +"\">" + sub_equip_spec + ellipsis + "</span>";
                    }
                    else
                        equip_spec_show = equip_spec;
                    var maintain_add = "<tr>"
                    +'<td>'
                        +'<span onclick="modify_log($(this));"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                        +'<span data-toggle="modal" data-target="#delete_log" onclick="del_log();"><img  alt="Delete" src="/static/images/icon_del.gif"></span>'
                    +'</td>'
                    +'<td class="yc">'+maintain_log_data[i][0]+'</td>'
                    +"<td>"+maintain_log_data[i][1]+"</td>"
                    +"<td>"+maintain_log_data[i][2]+"</td>"
                    +"<td>"+equip_osn_show+"</td>"
                    +"<td>"+maintain_log_data[i][4]+"</td>"
                    +"<td>"+maintain_log_data[i][5]+"</td>"
                    +"<td>"+maintain_log_data[i][6]+"</td>"
                    +"<td>"+equip_spec_show+"</td>"
                    +"<td>"+maintain_log_data[i][8]+"</td>"
                    +"<td>"+maintain_log_data[i][9]+"</td>"
                    +"<td>"+maintain_log_data[i][10]+"</td>"
                    +"<td>"+maintain_log_data[i][11]+"</td>"
                    +"<td>"+maintain_log_data[i][12]+"</td>"
                    +"<td>"+maintain_log_data[i][19]+"</td>"
                    +"<td>"+Status_CN_ENG(maintain_log_data[i][15])+"</td>"
                    +"<td>"+maintain_log_data[i][16]+"</td>"
                    +"<td>"+maintain_log_data[i][17]+"</td>"
                    +"<td>"+maintain_log_data[i][18]+"</td>"
                    +"</tr>"
                    $("#add_equipment_log").append(maintain_add)
                    popover_show();
                }

                data_count = result['data'].page_count
                 if(page_log_add['page'] == '1' ){
                    $("#previous_add_log").parent().addClass("disabled")
                    $("#next_add_log").parent().addClass("disabled")
                }
                if(Number(page_log_add['page']) == data_count){
                    $("#next_add_log").parent().addClass("disabled")
                }
                if(Number(page_log_add['page']) < data_count){
//                    $("#previous_add_log").parent().addClass("disabled")
                    $("#next_add_log").parent().removeClass("disabled")
                }
                if(Number(page_log_add['page']) > data_count && data_count>1){
                    page_log_add['page']='1'
                    $("#previous_add_log").parent().addClass("disabled")
                    $("#next_add_log").parent().removeClass("disabled")
                }
            }else{
//                  alert(result['message'])
                $("#add_equipment_log").empty()
                $("#next_add_log").parent().addClass("disabled")
            }
        }
    })
}




//设备进行修改动作
function re_add_log(){


    var mo_sn =$("#mo_sn").val()
    var mo_usn =$("#mo_usn").val()
    var mo_osn =$("#mo_osn").val()
    var mo_asset =$("#mo_asset").val()
    var mo_pn =$("#mo_pn").val()
    var mo_partname =$("#mo_partname").val()
    var mo_spec =$("#mo_spec").val()

    var mo_used_time =$("#mo_use_time").val()
    var mo_next_time =$("#mo_next_time").val()
    var mo_name =$("#mo_name").val()
    var mo_location =$("#mo_addr").val()
    var mo_status =$("#mo_status").val()
    var mo_days =$("#mo_days").val()
    var mo_times =$("#mo_times").val()
    var mo_maintainers =$("#mo_maintainers").val()

    var Regx =  /^[0-9]*$/;
    if(mo_sn == "" || mo_pn == "" || mo_partname == "" || mo_spec == "" || mo_used_time == ""|| mo_location == ""|| mo_status == ""){
        window.message.showError("red marked part need values")
        return false;
    }
    if(!Regx.test(mo_used_time)){
        alert("used_times is digital")
        return false;
    }
    if(!Regx.test(mo_days)){
        alert("days is digital")
        return false;
    }
    if(!Regx.test(mo_times)){
        alert("times is digital")
        return false;
    }
    data = {
        'mo_sn':mo_sn,
        'mo_usn':mo_usn,
        'mo_osn':mo_osn,
        'mo_asset':mo_asset,
        'mo_pn':mo_pn,
        'mo_partname':mo_partname,
        'mo_spec':mo_spec,
        'mo_used_time':mo_used_time,
        'mo_next_time':mo_next_time,
        'mo_name':mo_name,
        'mo_location':mo_location,
        'mo_status':mo_status,
        'mo_days':mo_days,
        'mo_times':mo_times,
        'mo_maintainers':mo_maintainers,
    }
    console.log(data)
    $.ajax({
        'type':'POST',
        'url':'/maintain/maintain-modify-log/',
        'data':data,
        success:function(result){
            if(result['code'] === 200){
                add_log();
                window.message.showSuccess(result['message'])
            }else{
                alert(result['message'])
            }
        }
    })
}
//对设备进行删除动作的确认
function delete_add_log(){
    var id = $("#delete_log_id").val()
    data = {
        'id':id,
    }
    console.log(data)
    $.ajax({
        'type':'POST',
        'url':'/maintain/maintain-delete-log/',
        'data':data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                add_log();
                window.message.showSuccess(result['message'])
            }else{
                add_log();
                alert(result['message'])
            }
        }
    })
}





var page_main_log ={'page':'1','num':'10'}
$(document).ready(function(){
     $("#main_lo_setup").change(function(){
        var page_log_num = $(this).children('option:selected').val()
        page_main_log['num']=page_log_num.toString()
        page_main_log['page'] = '1'
        console.log(page_main_log)
        console.log(page_log_num)
        if(page_main_log['num'] == 'All'){
            console.log(page_log_num)
            $("#previous_lo").parent().addClass("disabled")
            $("#next_lo").parent().addClass("disabled")
        }
        if(page_main_log['num'] != 'All'){
            $("#previous_lo").parent().removeClass("disabled")
            $("#next_lo").parent().removeClass("disabled")
        }
        if(page_main_log['page'] == '1'){
            $("#previous_lo").parent().addClass("disabled")
        }
        if(JSON.stringify(main_query_log) == '{}'){
            query_log_ajax();
        }else{
            query_log_fun();
        }
     })
})
//上一页页码的转换
function previous_log(){
    if(page_main_log['page'] != '1' && page_main_log['num'] != 'All'){
        page_main_log['page']= (Number(page_main_log['page'])-1).toString()
        $("#next_lo").parent().removeClass("disabled")
        if(JSON.stringify(main_query_log) == '{}'){
            query_log_ajax();
        }else{
            query_log_fun();
        }
    }
}
//下一页的页面转换
function next_log(){
    if(page_main_log['num'] != 'All'){
        page_main_log['page']= (Number(page_main_log['page'])+1).toString()
        $("#previous_lo").parent().removeClass("disabled")
        if(JSON.stringify(main_query_log) == '{}'){
            query_log_ajax();
        }else{
            query_log_fun();
        }
    }
}

var main_query_log={}
//设备保养记录页面的显示
function query_log(){
    $(".query_log").removeClass("yc")
    $(".add_main").addClass("yc")
    $(".maintain_index").addClass("yc")
    $(".operation").addClass("yc")
    $(".result").addClass("yc")
    $(".add_log").addClass("yc")
    $("#log_add_data")[0].reset();

    if(JSON.stringify(main_query_log) != '{}'){
        main_query_log = {}
        page_main_log ={'page':'1','num':'10'}
    }
    page_main_log ={'page':'1','num':'10'}
    query_log_ajax();
}
function query_log_ajax(){
    $.ajax({
        type:'GET',
        data:page_main_log,
        url:'/maintain/maintain-equipment-log/',
        success:function(result){
            var Spec_title
            if(result['code'] === 200){
                $("#maintain_log").empty();
                data = result['data']
                console.log(data)
                maintain_log_data = result['data'].data
                console.log(maintain_log_data)
                for(var i=0; i<maintain_log_data.length; i++){
                    if(maintain_log_data[i][4] == null){maintain_log_data[i][4] = ""}
                    var equip_spec =  maintain_log_data[i][2];
                    if(equip_spec && equip_spec.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_spec = equip_spec.substring(0,10);
                        equip_spec_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_spec +"\">" + sub_equip_spec + ellipsis + "</span>";
                    }
                    else
                        equip_spec_show = equip_spec;
                    var maintain_add = "<tr>"
                    +"<td>"+maintain_log_data[i][0]+"</td>"
                    +"<td>"+maintain_log_data[i][1]+"</td>"
                    +"<td>"+equip_spec_show+"</td>"
                    +"<td>"+maintain_log_data[i][3]+"</td>"
                    +"<td>"+maintain_log_data[i][4]+"</td>"
                    +"<td>"+maintain_log_data[i][5]+"</td>"
                    +"<td>"+maintain_log_data[i][6]+"</td>"
                    +"<td>"+maintain_log_data[i][10]+"</td>"
                    +"</tr>"
                    $("#maintain_log").append(maintain_add)
                    popover_show();
                }

                data_count = result['data'].page_count
                if(page_main_log['page'] == '1'){
                    $("#previous_lo").parent().addClass("disabled")
                }
                if(Number(page_main_log['page']) == data_count){
                    $("#next_lo").parent().addClass("disabled")
                }
                if(Number(page_main_log['page']) < data_count){
                    $("#next_lo").parent().removeClass("disabled")
                }

            }else{
                $("#next_lo").parent().addClass("disabled")
                $("#previous_lo").parent().addClass("disabled")
            }
        }
    })
}

function query_log_selector(){
    page_main_log = {'page':'1','num':'10'};
    $("#main_lo_setup").val(10);

}
//查询设备保养记录的函数以及显示
function query_log_fun(){
    var log_s_time = $("#log_start_time").val()
    var log_e_time = $("#log_end_time").val()
    var log_SN = $("#log_SN").val()
    var log_PN = $("#log_PN").val()
    var log_Spec = $("#log_Spec").val()
    var log_maintainer = $("#log_maintainer").val()
    var log_content = $("#log_content").val()
    if(log_s_time=="" && log_e_time=="" && log_SN=="" && log_PN =="" && log_Spec =="" && log_maintainer ==""){
        main_query_log = {}
    }
    if(log_s_time == log_e_time && log_s_time !="" && log_e_time !=""){
        log_e_time = log_e_time+" 23:59:59";
    }
    data = {
        'log_s_time':log_s_time,
        'log_e_time':log_e_time,
        'log_SN':log_SN,
        'log_PN':log_PN,
        'log_Spec':log_Spec,
        'log_maintainer':log_maintainer,
        'log_content':log_content,
    }
    main_query_log=data //这里是把筛选的条件变成全局条件给视图查询做准备
    data['page']=page_main_log['page']
    data['num']=page_main_log['num']
    console.log(data)
    $.ajax({
    type:'POST',
    data:data,
    url:'/maintain/maintain-query-log/',
        success:function(result){
            var Spec_title
            if(result['code'] === 200){
                $("#maintain_log").empty();
                data = result['data']
                console.log(data)
                maintain_log_data = result['data'].data
                console.log(maintain_log_data)
                for(var i=0; i<maintain_log_data.length; i++){
                    if(maintain_log_data[i][4] == null){maintain_log_data[i][4] = ""}
                    var equip_spec =  maintain_log_data[i][2];
                    if(equip_spec && equip_spec.length > 10)
                    {
                        var ellipsis = "<font color=\"blue\">...</font>";
                        var sub_equip_spec = equip_spec.substring(0,10);
                        equip_spec_show = "<span data-toggle=\"popover\" data-trigger=\"hover click\" data-content=\""+ equip_spec +"\">" + sub_equip_spec + ellipsis + "</span>";
                    }
                    else
                        equip_spec_show = equip_spec;
                    var maintain_add = "<tr>"
                    +"<td>"+maintain_log_data[i][0]+"</td>"
                    +"<td>"+maintain_log_data[i][1]+"</td>"
                    +"<td>"+equip_spec_show+"</td>"
                    +"<td>"+maintain_log_data[i][3]+"</td>"
                    +"<td>"+maintain_log_data[i][4]+"</td>"
                    +"<td>"+maintain_log_data[i][5]+"</td>"
                    +"<td>"+maintain_log_data[i][6]+"</td>"
                    +"<td>"+maintain_log_data[i][9]+"</td>"
                    +"</tr>"
                    $("#maintain_log").append(maintain_add)
                    popover_show();
                }

                data_count = result['data'].page_count
                if(page_main_log['page'] == '1'){
                    $("#previous_lo").parent().addClass("disabled")
                    $("#next_lo").parent().addClass("disabled")
                }
                if(Number(page_main_log['page']) == data_count){
                    $("#next_lo").parent().addClass("disabled")
                }
                if(Number(page_main_log['page']) < data_count){
                    $("#next_lo").parent().removeClass("disabled")
                }
                if(Number(page_main_log['page']) > data_count && data_count>1){
                    page_main_log['page']='1'
                    $("#previous_lo").parent().addClass("disabled")
                    $("#next_lo").parent().removeClass("disabled")
                }

            }else{
                $("#maintain_log").empty()
                $("#next_lo").parent().addClass("disabled")
            }
        }
    })

}



var page_main_action ={'page':'1','num':'10'}
$(document).ready(function(){
     $("#setup_Ma").change(function(){
        var page_main_num = $(this).children('option:selected').val()
        page_main_action['num']=page_main_num.toString()
        page_main_action['page'] = '1'
        console.log(page_main_action)
        if(page_main_log['num'] != 'All'){
            $("#Previous_Ma").parent().removeClass("disabled")
            $("#Next_Ma").parent().removeClass("disabled")
        }
        query_main();
     })
})
//上一页页码的转换
function previous_Ma(){
    if(page_main_action['page'] != '1' && page_main_action['num'] != 'All'){
        page_main_action['page']= (Number(page_main_action['page'])-1).toString()
        $("#Next_Ma").parent().removeClass("disabled")
        console.log(page_main_action)
        query_main();
    }
}
//下一页的页面转换
function next_Ma(){
    page_main_action['page']= (Number(page_main_action['page'])+1).toString()
    $("#Previous_Ma").parent().removeClass("disabled")
    console.log(page_main_action)
    query_main();
}


//设备保养的子目录的进入之后通过筛选出来的数据进行保养设置的函数
function query_main(){
    var sn =     $("#query_main_sn").val().trim()
    var pn =     $("#query_main_pn").val().trim()
    var status = $("#query_main_status").val()
    var next_time =$("#query_main_next_time").val()
    var next_time_1 =$("#to_query_main_next_time").val()
    var maintainers =$("#query_maintainer").val()
    var location =$("#query_locations").val()
    if( sn=="" && pn == ""&& status == "" && next_time == ""&& maintainers == ""&& location == ""){
        window.message.showError("Need value to match")
        return false;
    }
    if(next_time_1 != ""){
        var next_time_1 =next_time_1+" 23:59:59"
    }
    data={
        'sn':sn,
        'pn':pn,
        'status':status,
        'next_time':next_time,
        'next_time_1':next_time_1,
        'maintainers':maintainers,
        'location':location,
    }
    data['num']=page_main_action['num']
    data['page']=page_main_action['page']
    console.log(data)
    $.ajax({
    'type':'POST',
    'data':data,
    'url':'/maintain/maintain-query-operation/',
        success:function(result){
            if(result['code'] === 200){
                console.log(result['data'])
                mt_qu_data=result['data'].data
                var status
                var status_class
                if($("#check_enter").is(':checked')){
                    $("#Previous_Ma").parent().addClass("disabled")
                    $("#Next_Ma").parent().addClass("disabled")
                }else{$("#mt_query_detail").empty()}
                for(var i=0; i<mt_qu_data.length; i++){
                    if(mt_qu_data[i][6] == null){mt_qu_data[i][6] =""}else{
                        mt_qu_data[i][6] = (mt_qu_data[i][6]).split("T")[0]}
                    if(mt_qu_data[i][13] == "normal"){
                        status = "正常"
                        status_class = "badge badge-success";
                    }
                    if(mt_qu_data[i][13] == "warning"){
                        status = "预警"
                        status_class = "badge badge-warning";
                    }
                    if(mt_qu_data[i][13] == "danger"){
                        status = "超标"
                        status_class = "badge badge-danger";
                    }
                    if(mt_qu_data[i][13] == "none"){
                        status = "未设定"
                        status_class = "badge badge-info";
                    }
                    var mt_detail_add = "<tr>"
                    +"<td><input type=\"checkbox\" name=\"mt_all\" value=\"true\"><label class='yc'>"+mt_qu_data[i][0]+"</label></td>"
                    +"<td>"+mt_qu_data[i][1]+"</td>"
                    +"<td>"+mt_qu_data[i][2]+"</td>"
                    +"<td>"+mt_qu_data[i][3]+"</td>"
                    +"<td>"+mt_qu_data[i][4]+"</td>"
                    +"<td>"+mt_qu_data[i][5]+"</td>"
                    +"<td>"+mt_qu_data[i][6]+"</td>"
                    +"<td><span class='"+status_class+"'>"+status+"</span></td>"
                    +"</tr>"
                    $("#mt_query_detail").append(mt_detail_add)
                }

                data_count = result['data'].page_count
                console.log(data_count)
                if(page_main_action['page'] == '1'){
                    $("#Previous_Ma").parent().addClass("disabled")
                    $("#Next_Ma").parent().addClass("disabled")
                }
                if(Number(page_main_action['page']) == data_count){
                    $("#Next_Ma").parent().addClass("disabled")
                }
                if(Number(page_main_action['page']) < data_count){
                    $("#Next_Ma").parent().removeClass("disabled")
                }
                if(Number(page_main_action['page']) > data_count && data_count>1){
                    page_main_log['page']='1'
                    $("#Previous_Ma").parent().addClass("disabled")
                    $("#Next_Ma").parent().removeClass("disabled")
                }
            }else{
                alert(result['message'])
            }
        }
    })
}

//checkbox全选 全选函数check盒子
$(function () {
    //全选,设置chheckbox name='all' tbody id=tb
    $("input[name=mt_all]").click(function () {
        if (this.checked) {
            $("#mt_query_detail :checkbox").prop("checked", true);
        } else {
            $("#mt_query_detail :checkbox").prop("checked", false);
        }
    });
});
//对筛选的数据进行保养
function maintain_query_data(){
    var select_box = $("table input[type=checkbox]:checked")
    var maintain_date = $("#maintain_setup_date").val()
    var maintain_operator = $("#maintain_operator").val()
    var maintain_status = $("#maintain_status").val()
    var maintain_text = $("#maintain_text_era").val()
    var maintain_remark = $("#maintain_remark").val()
    var maintain_locations = $("#maintain_locations").val()
    var statement_mt = []
    select_box.each(function(){statement_mt.push($(this).next().html());})
    if(statement_mt[0] == "全选"){statement_mt.splice(0,1)}
    if(statement_mt.length == 0){
        alert("need select more than one");
        return false;
    }
    if(maintain_date == ""){
        alert("maintain time can't empty");
        return false;
    }
    if(maintain_operator == ""){
        alert("maintain_operator can't empty");
        return false;
    }
    if(maintain_text == ""){
        alert("maintain_text can't empty");
        return false;
    }
    data = {
        'statement_mt':statement_mt,
        'maintain_date':maintain_date,
        'maintain_operator':maintain_operator,
        'maintain_status':maintain_status,
        'maintain_text':maintain_text,
        'maintain_remark':maintain_remark,
        'maintain_locations':maintain_locations,
    }
//    console.log(data)
    $.ajax({
        type:'POST',
        url:'/maintain/maintain-query-maintain/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                query_log();
                li_active();
            }else{
                alert(result['message'])
            }
        }
    })
}

