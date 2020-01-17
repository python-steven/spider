var configData={
    //登录页面
    "title":['登录','Login'],
    "nickName":['用户名','User Name'],
    "email":['邮箱','Email'],
    "password":['密码','Password'],
    "Remember":['记住密码','Remember me'],

    //侧栏
    "Budget":['预算编码','Budget Code'],
    "Statistics":['统计分析','Statistical Analysis'],
    "Equipment":['设备保养','Equipment Maintaince'],
    "Maintenance":['设备保养监控','Maintenance Monitor'],
    "NG":['设备NG率监控','NG Rate Monitor'],
    "System":['系统管理','System Management'],
    "modify_pwd":['修改密码','Change Password'],

    //预算编码页面
    "Application":['预算表单申请','My Apply Form'],
    "Sign-off":['预算表单签核','Need My Signature'],
    "MySign-off":['我签核过的预算编码单','My Signed Form'],
    "Report":['报表','My Form Report'],


    //通用
    "Operate":['操作','Operator'],
    "Setting":['设置','Setting'],
    "Filter":['筛选','Filter'],
    "Detail":['开单状况','Detail'],
    "Department":['部门','Department'],
    "Date":['申请日期','Applyed Date'],
    "InCharge":['负责人','PIC'],
    "Equipments":['设备名称','Equipments'],
    "SignedOne":['签核人','Signer'],
    "Status":['表单状态','Status'],
    "Code":['预算编码','Budget Code'],
    "CombinedForm":['合并开单','Combine Form'],
    "SingleForm":['单独开单','Single Form'],
    "AddForm":['填写预算编码单','Add'],
    "Customer":['客户','Customer'],
    "Form_Details":['表单详情','Form Details'],
    "UpdatedTime":['签核日期','Sign Data'],

    //系统管理
    "UserManage":['用户管理','Users'],
    "CustomerManage":['客户管理','Customers'],
    "DepartmentManage":['部门管理','Departments'],
    "StaffNumber":['员工工号','User ID'],
    "StaffName":['员工名称','Name'],
    "StaffDepartment":['员工部门','Department'],
    "StaffEmail":['邮箱','Email'],
    "Level":['角色','Role'],
    "AddUser":['添加用户','Add User'],
    "AddCustomer":['添加客户','Add Customer'],
    "AddDepartment":['添加部门','Add Dept'],

    //修改密码
    "ChangePassword":['修改密码','Change Password'],
    "OldPW":['原始密码','Old Password'],
    "NewPW":['新密码','New Password'],
    "ConfirmNewPW":['重复新密码','Confirm New Password'],

    //统计分析
    "Chart":['图表','Chart'],
    "Data":['数据','Data'],

    //设备保养
    "EquipmentList":['设备列表','EquipmentList'],
    "ByPNSetting":['by PN设定','By PN Setting'],
    "Spec":['品名','Spec'],
    "CheckCycle":['保养周期(按天数)','Check Cycle'],
    "CheckCountCycle":['保养周期(按次数)','Check Counts Cycle'],
    "UsedTimes":['已使用次数','Used Times'],
    "NextCheckTime":['下次保养时间','Next Check Date'],
    "Maintenaner":['保养人','Maintenaner'],
    "AddEquipment":['添加设备','Add Equipment'],
    "ImportEquipment":['Excel汇入设备','Excel Import Equipment'],
    "MyEquipment":['我添加的设备','MyEquipment'],
    "EquipmentMaintaince":['设备保养','Equipment Maintaince'],
    "MaintainceDate":['保养时间','Maintaince Date'],
    "MaintainceStatus":['保养状态','Maintaince Status'],
    "MaintainceContent":['保养内容','Maintaince Content'],
    "Remark":['备注','Remark'],
    "Maintain":['保养','Maintain'],

    //设备NG率监控
    "NGStandar":['NG标准','NG Standar'],
    "ActualNGRate":['实际NG率','Actual NG Rate'],
    "NGCounts":['NG次数','NG Counts'],
};
$(document).ready(function(){
    $("#language").change(function(){
        var index= $("#language").val()
        if(index == 1){
            $.cookie("language","English",{expires:7});
        }else{
            $.cookie("language","Chinese",{expires:7});
        }
        $(".lng").each(function() {
           var _this=$(this);
           console.log(_this.data("name"))
           _this.html(configData[_this.data("name")][index]);
        })
    });
})
/* function language(obj){
   var index=obj.value;
   alert(index);
   $(".lng").each(function() {
       var _this=$(this);
       _this.html(configData[_this.data("name")][index]);
   })
} */