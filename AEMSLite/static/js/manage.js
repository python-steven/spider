function modify_User(){
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#modifyId").val(a[1].innerHTML)
            $("#modifyNum").val(a[2].innerHTML)
            $("#modifyName").val(a[3].innerHTML)
            $("#modifyPart").val(a[4].innerHTML)
            $("#modifyEmail").val(a[5].innerHTML)
            $("#modifyRole").val(a[6].innerHTML)
        });
    });
}
function delete_User(){
    $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#deluser").empty();
            $("#deluser").append(a[3].innerHTML)
        });
    });

}
function modify_customer(){
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#modifyCusId").val(a[1].innerHTML)
            $("#modifyCusName").val(a[2].innerHTML)
        });
    });
}
function delete_customer(){
    $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#delCusName").empty();
            $("#delCusName").append(a[2].innerHTML)
        });
    });

}
function modify_department(){
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#modifyPartId").val(a[1].innerHTML)
            $("#modifyPartName").val(a[2].innerHTML)
        });
    });
}
function delete_department(){
    $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#delPart").empty();
            $("#delPart").append(a[2].innerHTML)
        });
    });

}
function modify_location(){
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#modifyLocationId").val(a[1].innerHTML)
            $("#modify_location_name").val(a[2].innerHTML)
        });
    });
}
function delete_location(){
    $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#del_location_name").empty();
            $("#del_location_name").append(a[2].innerHTML)
        });
    });

}
function modify_type(){
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#modifymodelId").val(a[1].innerHTML)
            $("#modify_model_name").val(a[2].innerHTML)
            $("#modify_model_code").val(a[3].innerHTML)
        });
    });
}
function delete_type(){
    $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#model_name").empty();
            $("#model_name").append(a[2].innerHTML)
        });
    });

}
function modify_money(){
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            console.log(a[3].innerHTML)
            $("#modifysubId").val(a[1].innerHTML)
            $("#modify_sub_type").val(a[2].innerHTML)
//            $("#modify_formula").find("option:contains('"+a.eq(3).text()+"')").attr("selected",true);
//            $("#modify_formula").val(a[3].innerHTML)
            $("#modify_formula option[name='"+a[3].innerHTML+"']").attr("selected", true)
            $("#modify_sub_rule").val(a[4].innerHTML)
        });
    });
}
function delete_money(){
    $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#del_sub_type").empty();
            $("#del_sub_type").append(a[2].innerHTML)
        });
    });

}

function modify_money_type (){
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            console.log(a[3].innerHTML)
            $("#modifyrateId").val(a[1].innerHTML)
            $("#modify_cu").val(a[2].innerHTML)
            $("#modify_to").val(a[3].innerHTML)
//            $("#modify_formula").find("option:contains('"+a.eq(3).text()+"')").attr("selected",true);
//            $("#modify_formula").val(a[3].innerHTML)
//            $("#modify_formula option[name='"+a[3].innerHTML+"']").attr("selected", true)
//            $("#modify_formula option[name='"+a[3].innerHTML+"']").attr("selected", true)
            $("#modify_ra").val(a[4].innerHTML)
        });
    });
}
function delete_money_type(){
    $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#del_rate").empty();
            $("#del_rate").append(a[1].innerHTML)
        });
    });

}


function modify_fee_limit(){
    var limit_id
    var depart_id
    var account_id
    var fee_cal
     $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            limit_id = a[1].innerHTML
            depart_id = a[2].innerHTML
            account_id = a[4].innerHTML
            fee_cal = a[6].innerHTML
            by_type = a[7].innerHTML
            console.log(a[2].innerHTML)
            console.log(a[4].innerHTML)
//            $("#modifyrateId").val(a[1].innerHTML)
//            $("#modify_cu").val(a[2].innerHTML)
//            $("#modify_to").val(a[3].innerHTML)
//            $("#modify_formula").find("option:contains('"+a.eq(3).text()+"')").attr("selected",true);
//            $("#modify_formula").val(a[3].innerHTML)
//            $("#modify_formula option[name='"+a[3].innerHTML+"']").attr("selected", true)
//            $("#modify_formula option[name='"+a[3].innerHTML+"']").attr("selected", true)
//            $("#modify_ra").val(a[4].innerHTML)
        });
    });

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
                $('#modify_depart').empty()
                $('#modify_AccClass').empty()
                $('#modify_Periode').empty()
                for(var a=0; a<depart.length; a++){
                //<option value="1">ESRZ10</option>
                    if(depart_id == depart[a].Id){
                        var depart_list ='<option value="'+depart[a].Id+'" selected>'+depart[a].Department+'</option>'
                        $('#modify_depart').append(depart_list)

                    }else{
                        var depart_list ='<option value="'+depart[a].Id+'">'+depart[a].Department+'</option>'
                        $('#modify_depart').append(depart_list)
                    }
                }
                for(var i=0; i<account.length; i++){
                //<option value="1">ESRZ10</option>
                    if(account_id == account[i].Id){
                        var account_list ='<option value= "'+account[i].Id+'" selected>'+account[i].Type+'</option>'
                        $('#modify_AccClass').append(account_list)

                    }else{
                        var account_list ='<option value= "'+account[i].Id+'">'+account[i].Type+'</option>'
                        $('#modify_AccClass').append(account_list)
                    }
                }
                $('#modify_Cost').val(fee_cal)

                limit_type_0 = '<option value="year">年</option>'
                limit_type_1 = '<option value="month">月</option>'
                limit_type_2 = '<option value="year">周</option>'
                if(by_type == '年'){
                    limit_type_0 = '<option value="year" selected>年</option>'
                    limit_type_1 = '<option value="month">月</option>'
                    limit_type_2 = '<option value="year">周</option>'
                    $('#modify_Periode').append(limit_type_0)
                    $('#modify_Periode').append(limit_type_1)
                    $('#modify_Periode').append(limit_type_2)
                }else if(by_type == '月'){
                    limit_type_0 = '<option value="year">年</option>'
                    limit_type_1 = '<option value="month" selected>月</option>'
                    limit_type_2 = '<option value="year">周</option>'
                    $('#modify_Periode').append(limit_type_0)
                    $('#modify_Periode').append(limit_type_1)
                    $('#modify_Periode').append(limit_type_2)

                }else if(by_type == '周'){
                    limit_type_0 = '<option value="year">年</option>'
                    limit_type_1 = '<option value="month">月</option>'
                    limit_type_2 = '<option value="year" selected>周</option>'
                    $('#modify_Periode').append(limit_type_0)
                    $('#modify_Periode').append(limit_type_1)
                    $('#modify_Periode').append(limit_type_2)
                }
                $('#modify_Periode').append()
                $('#modifyfeeId').val(limit_id)
            }else{
                alert(result['message'])
            }
        }

    })

}
function delete_fee_limit(){
    $("tr").each(function(index) {
        $("tr").eq(index).click(function() {
            var a = $(this).find("td")
            $("#del_fee").empty();
            $("#del_fee").append(a[1].innerHTML)
        });
    });

}
