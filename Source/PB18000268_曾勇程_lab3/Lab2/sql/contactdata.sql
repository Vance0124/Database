use lab2;
set sql_safe_updates=0;
delete from contacts;
insert into contacts value(1, '傻蛋', 17877181899, '123@qq.com', '父亲');
insert into contacts value(2, '二狗蛋', 17877181899, '12334@qq.com', '母亲');
insert into contacts value(3, '三狗蛋', 17877181899, '1232@qq.com', '儿子');
-- insert into Contacts value('111111111111111111', 'O\' Neil', 17877181899, '123\'@11.cn', 'Rose\'s mum');
SELECT * FROM lab2.contacts;