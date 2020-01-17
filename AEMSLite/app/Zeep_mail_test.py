from zeep import Client


def Send_mail(receivers, subject, content, mail_type):
    client = Client("http://10.41.95.141:90/webservice/?wsdl")

    # content_imagename_Value = {'name': 'Border.png', 'type': '', 'data': open('Border.png', 'rb').read()} #picture one information
    # content_imagename_Value1 = {'name': 'python.png', 'type': '', 'data': open('python.png', 'rb').read()} #picture two information
    # content_imagename_list = {}
    # content_imagename_list['_Value'] = [content_imagename_Value, content_imagename_Value1]
    #
    # enclosure_Value = {'name': 'test.txt', 'type': '', 'data': open('test.txt', 'rb').read()}   #attachment file information one
    # # base64.encode('requirements.txt', enclosure_Value['data'])
    # enclosure_Value1 = {'name': 'hello.txt', 'type': '', 'data': open('hello.txt', 'rb').read()}  #attachment file information two
    # enclosure_list = {}
    # enclosure_list['_Value'] = [enclosure_Value, enclosure_Value1]
    #,contentImageNameList=content_imagename_list,enclosureList=enclosure_list

    to_receivers = "Steven_X_Xu@wistron.com"                                                       #mail receiver need
    cc_receivers = ""                                                                           # cc information
    title = "Send Mail"                                                                         # mail title

    contents = "test"                #mail string information
    result = client.service.SendMail(toReceivers=to_receivers, ccReceivers=cc_receivers
                                     ,subject=title,content=contents
                                     ,contentImageNameList={},enclosureList={}
                                     )
    print(result)


Send_mail()



def send_mail(receivers, subject, content, mail_type):
    """ 按mail_type选定的格式发送邮件 """
    client = Client("http://10.41.95.141:90/webservice/?wsdl")
    to_receivers = ",".join(receivers)  # mail receiver need
    cc_receivers = ""  # cc information
    title = subject  # mail title

    contents = content  # mail string information
    result = client.service.SendMail(toReceivers=to_receivers, ccReceivers=cc_receivers
                                     , subject=title, content=contents
                                     , contentImageNameList={}, enclosureList={}
                                     )
    print(result)
    # ret = True
    # try:
    #     msg = MIMEText(content, mail_type, 'utf-8')
    #     msg['From'] = formataddr(["Devlop", sender])
    #     msg['To'] = formataddr(["Signers", ",".join(receivers)])
    #     msg['Subject'] = subject
    #     conn = smtplib.SMTP('wzsowa.wistron.com', 587) #wistron mail server, port 587
    #     conn.starttls()
    #     conn.login(sender, password)
    #     conn.sendmail(sender, receivers, msg.as_string())
    #     conn.quit()
    # except Exception as ex:
    #     traceback.print_exc()
    #     ret = False
    # return ret
"""
explain +SQL语句
执行计划包含的信息    id select_type table type possible_keys key key_len ref rows
表的速去顺序
数据读取操作的操作类型
那些缩影可以使用
那些索引被实际使用
表之间的引用
每张表有多少行被
id  select_type    table type possible_keys key key_len ref rows
    SIMPLE
    SUBQUERY
    PRIMARY
    UNION
    UNION RESULT
explain 的性能指标参数‘
System > const(常量) > eq_ref() > ref() > range > index
1. id   说明每个对象表的执行顺序， id越大执行越早， id越小执行越晚
2.select_type  主查询 子查询  衍生查询   联合查询
3.type  显示查询使用了何种类型  
    system  表只有一行记录 
    const   常数 
    eq_ref  唯一性索引扫描  对于每一个索引键，
    ref     
    range   范围
    index  
    all
    在多表关联时， 可能用到的索引 实际使用到的索引， 和备用到的索引的长度
    int 4 
    varchar utf-8 3字节 *20字段长度+null（1）+2（varchar的存储长度）=63
    
    
    优化： 常用字段先建立索引、
    复合索引在建立和使用时，尽量考虑在用户应用查询时，常用的排序方向和字段组合顺序
"""

'''
1.plsql 首创oracle
2.plsq 有两种
有返回值的  函数
没有返回值的 存储过程（执行一些列的复杂的数据库操作，比如自动生成表数据， 比如对做账表的关联增删改查）
>1.先执行
 show variables like 'log_bin_trust_function_creators';
 set global log_bin_trust_function_creators=1;
>2.执行
    ：随机生成字符串函数
    DELIMITER $$
    CREATE FUNCTION rand_string(n INT) RETURNS VARCHAR(255)
    BEGIN
    DECLARE chars_str VARCHAR(100) DEFAULT
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRESTUVWXYZ';
    DECLARE return_str VARCHAR(255) DEFAULT '';
    DECLARE i INT DEFAULT 0;
    WHILE i < n DO
    SET return_str = CONCAT(return_str,SUBSTRING(chars_str,FLOOR(1+RAND()*52),1));
    SET i = i +1;
    END WHILE;
    RETURN return_str; 
    END $$
    
    ：随机生成部门编号的函数 100-->110
    DELIMITER $$
    CREATE FUNCTION rand_num()
    RETURNS INT(5)
    BEGIN
    DECLARE i INT DEFAULT 0;
    SET i=FLOOR(100+RAND()*10);
    RETURN i;
    END $$
    :创建存储过程 deparment 添加数据  (部门编号初始值，部门编号最大值)
    DELIMITER $$
    CREATE PROCEDURE insert_dept(IN START INT(10),IN max_num INT(10))
    BEGIN
    DECLARE i INT DEFAULT 0;
    SET autocommit =0;
    REPEAT
    SET i = i+1;
    INSERT INTO dept(deptno,dname,loc) VALUES((START+i))
    ,rand_string(10),rand_string(8);
    UNTIL i= max_num
    END REPEAT;
    COMMIT;
    END $$
    ：生产员工数据(员工编号初始值，员工的数量)
    DELIMITER $$
    CREATE PROCEDURE insert_emp(IN START INT(10),IN max_num INT(10))
    BEGIN
    DECLARE i INT DEFAULT 0;
    #set autommit = 0 把autommit 设置成0
    SET autocommit = 0;
    REPEAT
    SET i = i+1;
    INSERT INTO emp(empno,ename,job,mgr,hiredate,sal,comm,deptno) VALUES((START+i)
    ,rand_string(6),'SALESMAN',0001,CURDATE(),2000,400,rand_num());
    UNTIL i = max_num
    END REPEAT;
    COMMIT;
    END $$


emp表
id，empno,ename,job,mgr,hiredate,sal,comm,deptno
dept
id,deptno dname loc
'''


















