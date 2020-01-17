function user(){
    $(".useres").removeClass("yc")
    $(".customer").addClass("yc")
    $(".partment").addClass("yc")
    $(".address").addClass("yc")
    $(".type").addClass("yc")
    $(".money").addClass("yc")
    $(".money_type").addClass("yc")
    $(".Fee_limit").addClass("yc")
}

//自动触发事件报表页面
//$(function(){   
////    $("#previous_statement").parent().addClass("disabled")
//})
var page_user = {'page':'1','num':'10'}
//选择一页显示数量
$(document).ready(function(){
     $("#user_setup").change(function(){
        var page_user_number = $(this).children('option:selected').val()
        page_user['num']=page_user_number.toString()
        page_user['page'] = '1'
        if(page_user_number == 'All'){
            $("#previous_u").parent().addClass("disabled")
            $("#next_u").parent().addClass("disabled")
        }
        if(page_user_number != 'All'){
            $("#previous_u").parent().removeClass("disabled")
            $("#next_u").parent().removeClass("disabled")
        }
        if(page_user['page'] == '1'){
            $("#previous_u").parent().addClass("disabled")
        }
        manage();
     })
})
//上一页页码的转换
function previous_user(){
    if(page_user['page'] != '1' && page_user['num'] != 'All'){
        page_user['page']= (Number(page_user['page'])-1).toString()
        $("#next_u").parent().removeClass("disabled")
        manage();
    }
    if(page_user['page'] == '1'){
        $("#previous_u").parent().addClass("disabled")
    }
}
//下一页的页面转换
function next_user(){
    if(page_user['num'] != 'All'){
        page_user['page']= (Number(page_user['page'])+1).toString()
        $("#previous_u").parent().removeClass("disabled")
        manage();
    }
}

//侧边栏的click就加载获取的数据
function manage(){
    $(".user").removeClass("yc")
    $(".budget").addClass("yc")
    $(".ng").addClass("yc")
    $(".budgetform").addClass("yc")
    $(".merge").addClass("yc")
    $(".detail").addClass("yc")
    $(".maintain").addClass("yc")
    $(".statistic").addClass("yc")
    $(".modifypwd").addClass("yc")
    $(".main_monitor").addClass("yc")
    $.ajax({
        type:'GET',
        url:'/management/user-data/',
        data:page_user,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                $('#users-in-add').empty();
                data = result['data'].data
//                console.log(data)
                for(var a=0; a<data.length; a++){
                  var users ="<tr>"
                        +"<td>"
                          +"<span data-toggle='modal' onclick='modify_User();' data-target='#modify-user'><img alt='Add' src='/static/images/icon_modify.gif'></span>"
                          +"<span data-toggle='modal' onclick='delete_User();' data-target='#delete-user'><img alt='Delete' src='/static/images/icon_del.gif'></span>"
                        +"</td>"
                        +"<td class='yc'>"+data[a][0]+"</td>"
                        +"<td>"+data[a][1]+"</td>"
                        +"<td>"+data[a][2]+"</td>"
                        +"<td>"+data[a][3]+"</td>"
                        +"<td>"+data[a][4]+"</td>"
                        +"<td>"+data[a][5]+"</td>"
                      +"</tr>"
                   $('#users-in-add').append(users)
                }

                data_count = result['data'].page_count
                if(page_user['page'] == '1'){
                    $("#previous_u").parent().addClass("disabled")
                }
                if(Number(page_user['page']) == data_count){
                    $("#next_u").parent().addClass("disabled")
                }
            }else{
                alert(result['message'])
                $("#next_u").parent().addClass("disabled")
            }
        }
    })
}
//IE机制问题的解决 清除之前的缓冲 代码如下
//beforeSend :function(xmlHttp){
//            xmlHttp.setRequestHeader("If-Modified-Since","0");
//            xmlHttp.setRequestHeader("Cache-Control","no-cache");
//},

//添加用户的功能
function approval(){
    var usernumber = $("#userNum").val().toUpperCase();
    var mail = $("#email").val();
    var username = $("#username").val();
    var department = $("#department").val().toUpperCase();
    var role = $("#Role").val();
    usernumber = usernumber.replace(/\s+/g,"");//去除所有空格
//    username = username.replace(/^\s+|\s+$/g,"");//去除两端的空格
    department = department.replace(/\s+/g,"");
    mail = mail.replace(/^\s+|\s+$/g,"");
    role = role.replace(/\s+/g,"");
    if(usernumber == ""){
        window.message.showError("employee number can not empty")
        return false;
    }
    if(username == ""){
        window.message.showError("user name can not empty")
        return false;
    }
    if(department == ""){
        window.message.showError("department can not empty")
        return false;
    }
    if(mail ==""){
        window.message.showError("mail can not empty")
        return false;
    }
    if(role ==""){
        window.message.showError("role can not empty")
        return false;
    }
    var data={
        'userid':usernumber,
        'username':username,
        'department':department,
        'mail':mail,
        'role':role,
    }
    $.ajax({
        type:'POST',
        url:'/management/user-data/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                manage();
            }else{
            window.message.showError(result['message'])
            }
        }
    })
}

//修改用户信息
function modify_user(){
    var id = $("#modifyId").val()
    var username = $("#modifyName").val()
    var department = $("#modifyPart").val()
    var role = $("#modifyRole").val()
    username = username.replace(/^\s+|\s+$/g,"")
    department = department.replace(/\s+/g,"")
    data ={
        'id':id,
        'username':username,
        'department':department,
        'role':role,
    }
    $.ajax({
        type:'POST',
        url:'/management/user-modify/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                data = result['data']
                if(data.user == "other"){
                    manage();
                    window.message.showSuccess(result['message'])
                }
                if(data.user == "Myself"){
                    window.location.reload();
                }
            }else{
                window.message.showError(result['message'])
            }
        }
    })
}

//删除用户
function del_user(){
    var name = $("#deluser").text()
    data = {'name':name,}
    $.ajax({
        type:'POST',
        url:'/management/user-delete/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                data = result['data']
                console.log(data)
                if(data.user == "other"){
                    manage();
                    window.message.showSuccess(result['message'])
                }
                if(data.user == 'Myself'){
                    window.location.href="/login/"
                }
            }else{
                window.message.showError(result['message'])
            }
        }
    })
}

//客户管理的页面的数据的分页显示效果函数
var page_customer = {'page':'1','num':'10'}
//选择一页显示数量
$(document).ready(function(){
     $("#customer_setup").change(function(){
        var page_customer_number = $(this).children('option:selected').val()
        page_customer['num']=page_customer_number.toString()
        page_customer['page'] = '1'
        if(page_customer_number == 'All'){
            $("#previous_cu").parent().addClass("disabled")
            $("#next_cu").parent().addClass("disabled")
        }
        if(page_customer_number != 'All'){
            $("#previous_cu").parent().removeClass("disabled")
            $("#next_cu").parent().removeClass("disabled")
        }
        if(page_customer['page'] == '1'){
            $("#previous_cu").parent().addClass("disabled")
        }
        customer();
     })
})
//上一页页码的转换
function previous_customer(){
    if(page_customer['page'] != '1' && page_customer['num'] != 'All'){
        page_customer['page']= (Number(page_customer['page'])-1).toString()
        $("#next_cu").parent().removeClass("disabled")
        customer();
    }
    if(page_customer['page'] == '1'){
        $("#previous_cu").parent().addClass("disabled")
    }
}
//下一页的页面转换
function next_customer(){
    if(page_customer['num'] != 'All'){
        page_customer['page']= (Number(page_customer['page'])+1).toString()
        $("#previous_cu").parent().removeClass("disabled")
        customer();
    }
}


//客户的管理获取数据
function customer(){
    $(".customer").removeClass("yc")
    $(".useres").addClass("yc")
    $(".partment").addClass("yc")
    $(".address").addClass("yc")
    $(".type").addClass("yc")
    $(".money").addClass("yc")
    $(".money_type").addClass("yc")
    $(".Fee_limit").addClass("yc")
    $.ajax({
        type:'GET',
        url:'/management/Customer-Info/',
        data:page_customer,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                $('#customer-in-add').empty();
                data = result['data'].data
                for(var a=0; a<data.length; a++){
                    var customer ='<tr>'
                      +'<td>'
                        +'<span data-toggle="modal" onclick="modify_customer();" data-target="#modify-customer"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                        +'<span data-toggle="modal" onclick="delete_customer();" data-target="#delete-customer"><img alt="Delete" src="/static/images/icon_del.gif "></span>'
                      +'</td>'
                      +'<td class="yc">'+data[a].Id+'</td>'
                      +'<td>'+data[a].Customer+'</td>'
                    +'</tr>'
                    $('#customer-in-add').append(customer)
                }

                data_count = result['data'].page_count
                if(page_customer['page'] == '1'){
                    $("#previous_cu").parent().addClass("disabled")
                }
                if(Number(page_customer['page']) >= data_count){
                    $("#next_cu").parent().addClass("disabled")
                }
            }else{
                alert(result['message'])
                $("#next_cu").parent().addClass("disabled")
            }
        }
    })
}

//客户的数据添加
function Customer_add_button(){
    var customer_val = $("#Customer_info_Add").val()
    customer_val = customer_val.replace(/\s+/g,"");
    customer_val = customer_val.toUpperCase();
    if(customer_val == ""){
        window.message.showError("customer can not empty")
        return false;
    }
    if(customer_val.length >30){
        window.message.showError("customer name too longer")
        return false;
    }
    var data ={'customer_val':customer_val,}
    $.ajax({
        type:'POST',
        url:'/management/Customer-Info/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                customer();
            }else{
                window.message.showError(result['message'])
            }
        }
    })
}

//客户数据修改
function modify_cus(){
    var customer_name = $("#modifyCusName").val()
    var customer_id = $("#modifyCusId").val()
    customer_name = customer_name.replace(/\s+/g,"");
    customer_name = customer_name.toUpperCase();
    customer_id = customer_id.replace(/\s+/g,"");
    if(customer_name.length >30){
        window.message.showError("Customer name too longer")
        return false;
    }
    data = {
        'customer_name':customer_name,
        'customer_id':customer_id,
    }
    $.ajax({
        type:'POST',
        url:'/management/Customer-modify/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                customer();
            }else{
                window.message.showError(result['message'])
            }
        }
    })
}

//客户删除
function del_cus(){
    var del_nm = $("#delCusName").text()
    data = {'del_nm':del_nm,}
    $.ajax({
        type:'POST',
        url:'/management/Customer-delete/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                customer();
            }else{
                window.message.showError(result['message'])
            }
        }
    })
}

//部门管理的页面的数据的分页显示效果函数
var page_partname = {'page':'1','num':'10'}
//选择一页显示数量
$(document).ready(function(){
     $("#setup_partname").change(function(){
        var page_partname_number = $(this).children('option:selected').val()
        page_partname['num']=page_partname_number.toString()
        page_partname['page'] = '1'
        if(page_partname_number == 'All'){
            $("#previous_p").parent().addClass("disabled")
            $("#next_p").parent().addClass("disabled")
        }
        if(page_partname_number != 'All'){
            $("#previous_p").parent().removeClass("disabled")
            $("#next_p").parent().removeClass("disabled")
        }
        if(page_partname['page'] == '1'){
            $("#previous_p").parent().addClass("disabled")
        }
        partment();
     })
})
//上一页页码的转换
function previous_partname(){
    if(page_partname['page'] != '1' && page_partname['num'] != 'All'){
        page_partname['page']= (Number(page_partname['page'])-1).toString()
        $("#next_p").parent().removeClass("disabled")
        partment();
    }
    if(page_partname['page'] == '1'){
        $("#previous_p").parent().addClass("disabled")
    }
}
//下一页的页面转换
function next_partname(){
    if(page_partname['num'] != 'All'){
        page_partname['page']= (Number(page_partname['page'])+1).toString()
        $("#previous_p").parent().removeClass("disabled")
        partment();
    }
}


//部门管理的获取数据
function partment(){
    $(".partment").removeClass("yc")
    $(".useres").addClass("yc")
    $(".customer").addClass("yc")
    $(".address").addClass("yc")
    $(".type").addClass("yc")
    $(".money").addClass("yc")
    $(".money_type").addClass("yc")
    $(".Fee_limit").addClass("yc")
    $.ajax({
        type:'GET',
        url:'/management/Department-Info/',
        data:page_partname,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
    },
    success:function(result){
        if(result['code'] === 200){
            $('#department-in-add').empty();
//            console.log(result['data'])
            data = result['data'].data
            for(var a=0; a<data.length; a++){
                var department ='<tr>'
                  +'<td>'
                    +'<span data-toggle="modal" onclick="modify_department();" data-target="#modify-department"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                    +'<span data-toggle="modal" onclick="delete_department();" data-target="#delete-department"><img alt="Delete" src="/static/images/icon_del.gif "></span>'
                  +'</td>'
                  +'<td class="yc">'+data[a].Id+'</td>'
                  +'<td>'+data[a].Department+'</td>'
                +'</tr>'
                $('#department-in-add').append(department)
            }

            data_count = result['data'].page_count
            if(page_partname['page'] == '1'){
                $("#previous_p").parent().addClass("disabled")
            }
            if(Number(page_partname['page']) >= data_count){
                $("#next_p").parent().addClass("disabled")
            }
        }else{
            alert(result['message'])
            $("#next_p").parent().addClass("disabled")
        }
    }
    })
}

//部门管理添加数据
function more_department(){
    var department = $("#add_department").val();
    department = department.replace(/\s+/g,"");
    department = department.toUpperCase();
    if(department == ""){
        window.message.showError("department can not empty")
        return false;
    }
    var data = {'department':department,}
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Department-Info/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                partment();
            }else{
            window.message.showError(result['message'])
            }
        }
    })
}

//修改部门数据
function modify_dep(){
    var modifyPartName = $("#modifyPartName").val()
    var modifyPartId = $("#modifyPartId").val()
    modifyPartName = modifyPartName.toUpperCase()
    var data = {
        'modifyPartName':modifyPartName,
        'modifyPartId':modifyPartId,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Department-modify/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                partment();
            }else{
            window.message.showError(result['message'])
            }
        }
    })
}

//删除部门信息
function del_depart(){
    var delPart = $("#delPart").text()
    var data = {'delPart':delPart,}
    $.ajax({
        type:'POST',
        url:'/management/Department-delete/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                partment();
            }else{
            window.message.showError(result['message'])
            }
        }
    })
}




//位置的页面的数据的分页显示效果函数
var page_address = {'page':'1','num':'10'}
//选择一页显示数量
$(document).ready(function(){
     $("#setup_address").change(function(){
        var page_address_number = $(this).children('option:selected').val()
        page_address['num']=page_address_number.toString()
        page_address['page'] = '1'
        if(page_address_number == 'All'){
            $("#Previous_res").parent().addClass("disabled")
            $("#next_res").parent().addClass("disabled")
        }
        if(page_address_number != 'All'){
            $("#Previous_res").parent().removeClass("disabled")
            $("#next_res").parent().removeClass("disabled")
        }
        if(page_address['page'] == '1'){
            $("#Previous_res").parent().addClass("disabled")
        }
        address();
     })
})
//上一页页码的转换
function previous_address(){
    if(page_address['page'] != '1' && page_address['num'] != 'All'){
        page_address['page']= (Number(page_address['page'])-1).toString()
        $("#next_res").parent().removeClass("disabled")
        address();
    }
    if(page_address['page'] == '1'){
        $("#Previous_res").parent().addClass("disabled")
    }
}
//下一页的页面转换
function next_address(){
    if(page_address['num'] != 'All'){
        page_address['page']= (Number(page_address['page'])+1).toString()
        $("#Previous_res").parent().removeClass("disabled")
        address();
    }
}





//位置管理 获取的数据
function address(){
    $(".address").removeClass("yc")
    $(".useres").addClass("yc")
    $(".customer").addClass("yc")
    $(".partment").addClass("yc")
    $(".type").addClass("yc")
    $(".money").addClass("yc")
    $(".money_type").addClass("yc")
    $(".Fee_limit").addClass("yc")
    $.ajax({
        type:'GET',
        url:'/management/Location-list/',
        data:page_address,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                data= result['data'].data
                console.log(result['data'])
                $('#location_list').empty()
                for(var a=0; a<data.length; a++){
                    var location ='<tr>'
                      +'<td>'
                        +'<span data-toggle="modal" onclick="modify_location();" data-target="#modify-location"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                        +'<span data-toggle="modal" onclick="delete_location();" data-target="#delete-location"><img alt="Delete" src="/static/images/icon_del.gif "></span>'
                      +'</td>'
                      +'<td class="yc">'+data[a].Id+'</td>'
                      +'<td>'+data[a].Location+'</td>'
                    +'</tr>'
                    $('#location_list').append(location)
                }

                data_count = result['data'].page_count
                console.log(page_address)
                if(page_address['page'] == '1'){
                    $("#Previous_res").parent().addClass("disabled")
                }
                if(Number(page_address['page']) >= data_count){
                    $("#next_res").parent().addClass("disabled")
                }
            }else{
                $("#Previous_res").parent().addClass("disabled")
                $("#next_res").parent().addClass("disabled")
            }
        }
    })
}
//增加位置
function add_location(){
    var location_name = $("#location_name").val()
    location_name = location_name.toUpperCase()
    var data = {'location_name':location_name,}
    $.ajax({
        type:'POST',
        url:'/management/Location-add/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                address();
            }else{
            alert(result['message'])
            }
        }
    })
}
//编辑位置
function modify_location_na(){
    var mod_location_id = $("#modifyLocationId").val()
    var mod_location_name = $("#modify_location_name").val()
    mod_location_name = mod_location_name.toUpperCase()
    var data = {'mod_location_id':mod_location_id,'mod_location_name':mod_location_name}
    $.ajax({
        type:'POST',
        url:'/management/Location-edit/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                address();
            }else{
            alert(result['message'])
            console.log(result['data'])
            }
        }
    })
}
//删除位置
function delete_location_na(){
    var del_location_name = $("#del_location_name").text()
    var data = {'del_location_name':del_location_name,}
    $.ajax({
        type:'POST',
        url:'/management/Location-delete/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                address();
            }else{
            alert(result['message'])
            }
        }
    })
}


//机种维护的页面的数据的分页显示效果函数
var page_project = {'page':'1','num':'10'}
//选择一页显示数量
$(document).ready(function(){
     $("#set_projects").change(function(){
        var page_project_number = $(this).children('option:selected').val()
        page_project['num']=page_project_number.toString()
        page_project['page'] = '1'
        if(page_project_number == 'All'){
            $("#Previous_pj").parent().addClass("disabled")
            $("#Next_pj").parent().addClass("disabled")
        }
        if(page_project_number != 'All'){
            $("#Previous_pj").parent().removeClass("disabled")
            $("#Next_pj").parent().removeClass("disabled")
        }
        if(page_project['page'] == '1'){
            $("#Previous_pj").parent().addClass("disabled")
        }
        model_type();
     })
})
//上一页页码的转换
function Previous_project(){
    if(page_project['page'] != '1' && page_project['num'] != 'All'){
        page_project['page']= (Number(page_project['page'])-1).toString()
        $("#Next_pj").parent().removeClass("disabled")
        model_type();
    }
    if(page_project['page'] == '1'){
        $("#Previous_pj").parent().addClass("disabled")
    }
}
//下一页的页面转换
function Next_project(){
    if(page_project['num'] != 'All'){
        page_project['page']= (Number(page_project['page'])+1).toString()
        $("#Previous_pj").parent().removeClass("disabled")
        model_type();
    }
}


//机种管理 数据的获取
function model_type(){
    $(".type").removeClass("yc")
    $(".useres").addClass("yc")
    $(".customer").addClass("yc")
    $(".partment").addClass("yc")
    $(".address").addClass("yc")
    $(".money").addClass("yc")
    $(".money_type").addClass("yc")
    $(".Fee_limit").addClass("yc")
    $.ajax({
        type:'GET',
        url:'/management/Model-info/',
        data:page_project,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                console.log(result['data'])
                $('#project_name').empty()
                data=result['data'].data
                for(var a=0; a<data.length; a++){
                    var project_list ='<tr>'
                      +'<td>'
                        +'<span data-toggle="modal" onclick="modify_type();" data-target="#modify-type"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                        +'<span data-toggle="modal" onclick="delete_type();" data-target="#delete-type"><img alt="Delete" src="/static/images/icon_del.gif "></span>'
                      +'</td>'
                      +'<td class="yc">'+data[a].Id+'</td>'
                      +'<td>'+data[a].Name+'</td>'
                      +'<td>'+data[a].Code+'</td>'
                    +'</tr>'
                    $('#project_name').append(project_list)
                }

                data_count = result['data'].page_count
                console.log(page_project)
                if(page_project['page'] == '1'){
                    $("#Previous_pj").parent().addClass("disabled")
                }
                if(Number(page_project['page']) >= data_count){
                    $("#Next_pj").parent().addClass("disabled")
                }
            }else{
                $("#Previous_pj").parent().addClass("disabled")
                $("#Next_pj").parent().addClass("disabled")
            }
        }

    })
}
//机种管理， 数据添加
function add_project(){
    var model_name = $("#p_n_add").val()
    var model_code = $("#p_c_add").val()
    if(model_name == ""||model_code==""){
        alert("model can't empty")
        return false;
    }
    data={
        'model_name':model_name,
        'model_code':model_code,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Model-add/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                model_type();
            }else{
                alert(result['message'])
            }
        }

    })
}
//机种管理， 数据的修改
function model_modify(){
    var model_id=$("#modifymodelId").val()
    var model_name=$("#modify_model_name").val()
    var model_code=$("#modify_model_code").val()
    if(model_name == ""||model_code==""){
        alert("model can't empty")
        return false;
    }
    data={
        'Id':model_id,
        'model_name':model_name,
        'model_code':model_code,
    }
    $.ajax({
        type:'POST',
        url:'/management/Model-modify/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                model_type();
            }else{
                alert(result['message'])
            }
        }

    })
}
//机种管理， 数据的删除
function model_del(){
    var model_name=$("#model_name").text()
    data={
        'model_name':model_name,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Model-delete/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                model_type();
            }else{
                alert(result['message'])
            }
        }

    })
}




//机种维护的页面的数据的分页显示效果函数
var page_subjects = {'page':'1','num':'10'}
//选择一页显示数量
$(document).ready(function(){
     $("#set_subjects").change(function(){
        var page_subject_number = $(this).children('option:selected').val()
        page_subjects['num']=page_subject_number.toString()
        page_subjects['page'] = '1'
        if(page_subject_number == 'All'){
            $("#Previous_sj").parent().addClass("disabled")
            $("#Next_sj").parent().addClass("disabled")
        }
        if(page_subject_number != 'All'){
            $("#Previous_sj").parent().removeClass("disabled")
            $("#Next_sj").parent().removeClass("disabled")
        }
        if(page_subjects['page'] == '1'){
            $("#Previous_sj").parent().addClass("disabled")
        }
        money();
     })
})
//上一页页码的转换
function Previous_subject(){
    if(page_subjects['page'] != '1' && page_subjects['num'] != 'All'){
        page_subjects['page']= (Number(page_subjects['page'])-1).toString()
        $("#Next_sj").parent().removeClass("disabled")
        money();
    }
    if(page_subjects['page'] == '1'){
        $("#Previous_sj").parent().addClass("disabled")
    }
}
//下一页的页面转换
function Next_subject(){
    if(page_subjects['num'] != 'All'){
        page_subjects['page']= (Number(page_subjects['page'])+1).toString()
        $("#Previous_sj").parent().removeClass("disabled")
        money();
    }
}
//会计科目管理， 数据的获取
function money(){
    $(".money").removeClass("yc")
    $(".useres").addClass("yc")
    $(".customer").addClass("yc")
    $(".partment").addClass("yc")
    $(".type").addClass("yc")
    $(".address").addClass("yc")
    $(".money_type").addClass("yc")
    $(".Fee_limit").addClass("yc")
     $.ajax({
        type:'GET',
        url:'/management/Subjects-info/',
        data:page_subjects,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                console.log(result['data'])
                $('#subjects_list').empty()
                data=result['data'].data
                for(var a=0; a<data.length; a++){
                    data[a].Rule=change_title(data[a].Rule)
                    var subjects_list ='<tr>'
                      +'<td>'
                        +'<span data-toggle="modal" onclick="modify_money();" data-target="#modify-money"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                        +'<span data-toggle="modal" onclick="delete_money();" data-target="#delete-money"><img alt="Delete" src="/static/images/icon_del.gif "></span>'
                      +'</td>'
                      +'<td class="yc">'+data[a].Id+'</td>'
                      +'<td>'+data[a].Type+'</td>'
                      +'<td>'+data[a].Rule+'</td>'
                      +'<td>'+data[a].Remark+'</td>'
                    +'</tr>'
                    $('#subjects_list').append(subjects_list)
                }

                data_count = result['data'].page_count
                console.log(page_project)
                if(page_subjects['page'] == '1'){
                    $("#Previous_sj").parent().addClass("disabled")
                }
                if(Number(page_subjects['page']) >= data_count){
                    $("#Next_sj").parent().addClass("disabled")
                }
            }else{
//                alert(result['message'])
                $("#Previous_sj").parent().addClass("disabled")
                $("#Next_sj").parent().addClass("disabled")
            }
        }

    })
}
//会计科目管理， 数据添加
function subjects_a(){
    var add_subject= $("#add_subject").val()
    var add_rule= $("#formula").val()
    var add_mark= $("#add_mark").val().trim()
    if(add_rule == ""){
        alert("calculation formula can't empty")
        return false;
    }
    data={
        'add_subject':add_subject,
        'add_mark':add_mark,
        'add_rule':add_rule,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Subjects-add/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                money();
            }else{
                alert(result['message'])
            }
        }
    })
}
//会计科目管理， 数据的修改
function sub_modify(){
    var mo_su_id= $("#modifysubId").val()
    var mo_su_type= $("#modify_sub_type").val()
    var mo_su_formula= $("#modify_formula").val()
    var mo_su_rule= $("#modify_sub_rule").val().trim()
    if(mo_su_formula ==""){
        alert("formula can't empty")
        return false;
    }
    data={
        'mo_su_id':mo_su_id,
        'mo_su_type':mo_su_type,
        'mo_su_rule':mo_su_rule,
        'mo_su_formula':mo_su_formula,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Subjects-modify/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                money();
            }else{
                alert(result['message'])
            }
        }
    })
}
//会计科目管理， 数据的删除
function sub_delete(){
    var subjects_type=$("#del_sub_type").text()
    data={
        'subjects_type':subjects_type,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Subjects-delete/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                money();
            }else{
                alert(result['message'])
            }
        }

    })
}

//显示效果的字符转变
function change_title(num){
    if(num=="1"){
        var calculation ="當月產生的費用=總價"
        return calculation
    }
    if(num=="2"){
        var calculation ="當月產生的費用=總價/12"
        return calculation
    }
    if(num=="3"){
        var calculation ="當月產生的費用=總價/24"
        return calculation
    }
    if(num=="4"){
        var calculation ="當月產生的費用=總價/36"
        return calculation
    }
    if(num=="5"){
        var calculation ="當月產生的費用=總價/72"
        return calculation
    }

}

//汇率管理
function money_type(){
    $(".money_type").removeClass("yc")
    $(".useres").addClass("yc")
    $(".customer").addClass("yc")
    $(".partment").addClass("yc")
    $(".address").addClass("yc")
    $(".type").addClass("yc")
    $(".money").addClass("yc")
    $(".Fee_limit").addClass("yc")

    $.ajax({
        type:'GET',
        url:'/management/Rate-info/',
        data:{},
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                console.log(result['data'])
                $('#man_rate').empty()
                data=result['data'].data
                for(var a=0; a<data.length; a++){
                    var subjects_list ='<tr>'
                      +'<td>'
                        +'<span data-toggle="modal" onclick="modify_money_type();" data-target="#modify_money_type"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                        +'<span data-toggle="modal" onclick="delete_money_type();" data-target="#delete_money_type"><img alt="Delete" src="/static/images/icon_del.gif "></span>'
                      +'</td>'
                      +'<td class="yc">'+data[a].Id+'</td>'
                      +'<td>'+data[a].CurrencyFrom+'</td>'
                      +'<td>'+data[a].CurrencyTo+'</td>'
                      +'<td>'+data[a].ExchangeRate+'</td>'
                    +'</tr>'
                    $('#man_rate').append(subjects_list)
                }

//                data_count = result['data'].page_count
//                console.log(page_project)
//                if(page_subjects['page'] == '1'){
//                    $("#Previous_sj").parent().addClass("disabled")
//                }
//                if(Number(page_subjects['page']) >= data_count){
//                    $("#Next_sj").parent().addClass("disabled")
//                }
            }else{
                alert(result['message'])
//                $("#Previous_sj").parent().addClass("disabled")
//                $("#Next_sj").parent().addClass("disabled")
            }
        }

    })
}
//汇率添加
function rate_add(){
    var change_currency = $("#ch_cu").val()
    var to_currency= $("#ch_to").val()
    var change_rate= $("#change_rate").val()
    if(change_currency == "" ||to_currency =="" || change_rate==""){
        alert("Can't empty")
        return false;
    }
    data={
        'change_currency':change_currency,
        'to_currency':to_currency,
        'change_rate':change_rate,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Rate-add/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                money_type();
            }else{
                alert(result['message'])
            }
        }
    })
}

//汇率的修改
function rate_modify(){
    var change_id = $("#modifyrateId").val()
    var change_currency = $("#modify_cu").val()
    var to_currency= $("#modify_to").val()
    var change_rate= $("#modify_ra").val()
    if(change_currency == "" ||to_currency =="" || change_rate==""){
        alert("Can't empty")
        return false;
    }
    data={
        'change_id':change_id,
        'change_currency':change_currency,
        'to_currency':to_currency,
        'change_rate':change_rate,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Rate-modify/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                money_type();
            }else{
                alert(result['message'])
            }
        }
    })
}
//汇率的删除
function rate_del(){
    var del_id=$("#del_rate").text()
    data={
        'del_id':del_id,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Rate-delete/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                money_type();
            }else{
                alert(result['message'])
            }
        }

    })
}



//费用额度管理
function Fee_limit(){
    $(".Fee_limit").removeClass("yc")
    $(".useres").addClass("yc")
    $(".customer").addClass("yc")
    $(".partment").addClass("yc")
    $(".address").addClass("yc")
    $(".type").addClass("yc")
    $(".money").addClass("yc")
    $(".money_type").addClass("yc")

    $.ajax({
        type:'GET',
        url:'/management/Fee-detail-info/',
        data:{},
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                console.log(result['data'])
                data = result['data']
                $('#fee_data').empty()
                for(var a=0; a<data.length; a++){
                    if(data[a].LimitPeriod =="month"){
                        data[a].LimitPeriod = "月"
                    }else if(data[a].LimitPeriod =="week"){
                        data[a].LimitPeriod = "周"
                    }else if(data[a].LimitPeriod =="year"){
                        data[a].LimitPeriod = "年"
                    }else{
                        data[a].LimitPeriod = ""
                    }
                    var fee_info ='<tr>'
                      +'<td>'
                        +'<span data-toggle="modal" onclick="modify_fee_limit();" data-target="#modify_fee_limit"><img alt="Add" src="/static/images/icon_modify.gif"></span>'
                        +'<span data-toggle="modal" onclick="delete_fee_limit();" data-target="#delete_fee_limit"><img alt="Delete" src="/static/images/icon_del.gif "></span>'
                      +'</td>'
                      +'<td class="yc">'+data[a].Id+'</td>'

                      +'<td class="yc">'+data[a].DepartmentId+'</td>'
                      +'<td>'+data[a].Department+'</td>'

                      +'<td class="yc">'+data[a].AccountTitleId+'</td>'
                      +'<td>'+data[a].Type+'</td>'

                      +'<td>'+data[a].LimitCost+'</td>'
                      +'<td>'+data[a].LimitPeriod+'</td>'
                    +'</tr>'
                    $('#fee_data').append(fee_info)
                }

//                data_count = result['data'].page_count
//                console.log(page_project)
//                if(page_subjects['page'] == '1'){
//                    $("#Previous_sj").parent().addClass("disabled")
//                }
//                if(Number(page_subjects['page']) >= data_count){
//                    $("#Next_sj").parent().addClass("disabled")
//                }
            }else{
                alert(result['message'])
            }
        }

    })

}

//费用添加之前获取相对应的数据
function before_Add_Fee(){
     $.ajax({
        type:'GET',
        url:'/management/Fee-Depart-Account-info/',
        data:{},
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                console.log(result['data'])
                depart = result['data'].depart
                account = result['data'].account
                $('#fee_depart').empty()
                $('#fee_account').empty()
                $('#fee_depart').append('<option ></option>')
                $('#fee_account').append('<option ></option>')
                for(var a=0; a<depart.length; a++){
                //<option value="1">ESRZ10</option>
                    var depart_list ='<option value="'+depart[a].Id+'">'+depart[a].Department+'</option>'
                    $('#fee_depart').append(depart_list)
                }
                for(var i=0; i<account.length; i++){
                //<option value="1">ESRZ10</option>
                    var account_list ='<option value= "'+account[i].Id+'">'+account[i].Type+'</option>'
                    $('#fee_account').append(account_list)
                }

//                data_count = result['data'].page_count
//                console.log(page_project)
//                if(page_subjects['page'] == '1'){
//                    $("#Previous_sj").parent().addClass("disabled")
//                }
//                if(Number(page_subjects['page']) >= data_count){
//                    $("#Next_sj").parent().addClass("disabled")
//                }
            }else{
                alert(result['message'])
            }
        }

    })
}


//增加费用预算
function fee_limit_add(){
    DepartmentId = $("#fee_depart").val()
    AccountId = $("#fee_account").val()
    Fee = $("#fee_cost").val()
    Fee_period = $("#fee_period").val()
    var reg = /^\d+(?=\.{0,1}\d+$|$)/
//    var check_period = new RegExp("^[a-z]*|[A-Z]*$")
    if(!reg.test(Fee)){
        alert('digital error')
        return false;

    }
    if(Fee_period == ""){
        alert("period is error")
        return false;
    }
    data={
        'DepartmentId':DepartmentId,
        'AccountId':AccountId,
        'Fee':Fee,
        'Fee_period':Fee_period,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Fee-Limit-Add/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                Fee_limit();
            }else{
                alert(result['message'])
            }
        }

    })
}

//修改费用额度
function fee_modify(){
    id = $("#modifyfeeId").val()
    DepartmentId = $("#modify_depart").val()
    AccountId = $("#modify_AccClass").val()
    Fee = $("#modify_Cost").val()
    Fee_period = $("#modify_Periode").val()
    var reg = /^\d+(?=\.{0,1}\d+$|$)/
//    var check_period = new RegExp("^[a-z]*|[A-Z]*$")
    if(!reg.test(Fee)){
        alert('digital error')
        return false;

    }

    data={
        'Id':id,
        'DepartmentId':DepartmentId,
        'AccountId':AccountId,
        'Fee':Fee,
        'Fee_period':Fee_period,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Fee-Limit-Modify/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                Fee_limit();
            }else{
                alert(result['message'])
            }
        }

    })

}

//s删除费用额度
function fee_del(){
    var del_id=$("#del_fee").text()
    data={
        'del_id':del_id,
    }
    console.log(data)
    $.ajax({
        type:'POST',
        url:'/management/Fee-Limit-del/',
        data:data,
        beforeSend :function(xmlHttp){
            xmlHttp.setRequestHeader("If-Modified-Since","0");
            xmlHttp.setRequestHeader("Cache-Control","no-cache");
        },
        success:function(result){
            if(result['code'] === 200){
                window.message.showSuccess(result['message'])
                Fee_limit();
            }else{
                alert(result['message'])
            }
        }

    })
}


