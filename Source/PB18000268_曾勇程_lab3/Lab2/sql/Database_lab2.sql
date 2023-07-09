/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/5/18 17:38:54                           */
/*==============================================================*/
use lab2;

drop table if exists Contacts;

drop table if exists Hold_C_L;

drop table if exists CK_account;

drop table if exists SV_account;

drop table if exists Transact;

drop table if exists Account;

drop table if exists payout;

drop table if exists Loans;

drop table if exists manager;

drop table if exists Client;

drop table if exists Clerk;

drop table if exists department;

drop table if exists Bank;

/*==============================================================*/
/* Table: Account  账户                                             */
/*==============================================================*/
create table Account
(
   ID                   numeric(20,0) not null,
   balance              float(8,2) not null,
   TIME_open            date not null,
   TIME_access          date not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: Bank 银行分行（支行）                                                 */
/*==============================================================*/
create table Bank
(
   name                 varchar(50) not null,
   city                 varchar(50) not null,
   property             float(8,2) not null,
   primary key (name)
);

/*==============================================================*/
/* Table: CK_account 支票账户                                           */
/*==============================================================*/
create table CK_account
(
   ID                   numeric(20,0) not null,
   balance              float(8,2) not null,
   TIME_open            date not null,
   TIME_access          date not null,
   overdraft            float(8,2) not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: Clerk 职员                                                */
/*==============================================================*/
create table Clerk
(
   ID_card              char(18) not null,
   ID_depert            numeric(10,0) not null,
   name                 varchar(20) not null,
   telephone            numeric(11,0) not null,
   address              text,
   Data_SW              date not null,
   primary key (ID_card)
);

/*==============================================================*/
/* Table: Client 客户                                               */
/*==============================================================*/
create table Client
(
   ID_card              char(18) not null,
   Cle_ID_card          char(18) not null,
   name                 varchar(20) not null,
   telephone            numeric(11,0) not null,
   address               text,
   clerk_type           bool not null,
   primary key (ID_card)
);

/*==============================================================*/
/* Table: Contacts 联系人                                             */
/*==============================================================*/
create table Contacts
(
   ID_card              char(18) not null,
   name                 varchar(20) not null,
   telephone            numeric(11,0) not null,
   Email                varchar(40) not null,
   relation             varchar(10) not null,
   primary key (ID_card, name)
);

/*==============================================================*/
/* Table: Hold_C_L 持有信息                                             */
/*==============================================================*/
create table Hold_C_L
(
   name                 varchar(50) not null,
   ID_loan              numeric(20,0) not null,
   ID_card              char(18) not null,
   primary key (name, ID_loan, ID_card)
);

/*==============================================================*/
/* Table: Loans 贷款                                                */
/*==============================================================*/
create table Loans
(
   name                 varchar(50) not null,
   ID_loan              numeric(20,0) not null,
   money_loan           float(8,2) not null,
   TIME_open            datetime not null,
   primary key (name, ID_loan)
);

/*==============================================================*/
/* Table: SV_account 储蓄账户                                           */
/*==============================================================*/
create table SV_account
(
   ID                   numeric(20,0) not null,
   balance              float(8,2) not null,
   TIME_open            date not null,
   TIME_access          date not null,
   rate                 float not null,
   currency             varchar(20) not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: Transact 交易                                             */
/*==============================================================*/
create table Transact
(
   name                 varchar(50) not null,
   ID_card              char(18) not null,
   Type                 bool not null,
   ID                   numeric(20,0),
   primary key (name, ID_card, Type)
);

/*==============================================================*/
/* Table: department 部门                                           */
/*==============================================================*/
create table department
(
   ID_depert            numeric(10,0) not null,
   Ban_name             varchar(50),
   ID_card              char(18),
   name                 varchar(20) not null,
   Type_depert          varchar(20) not null,
   primary key (ID_depert)
);

/*==============================================================*/
/* Table: manager  经理                                             */
/*==============================================================*/
create table manager
(
   ID_card              char(18) not null,
   ID_depert            numeric(10,0),
   name                 varchar(20) not null,
   telephone            numeric(11,0) not null,
   address              text,
   Data_SW              date not null,
   primary key (ID_card)
);

/*==============================================================*/
/* Table: payout 支付情况                                               */
/*==============================================================*/
create table payout
(
   name                 varchar(50) not null,
   ID_loan              numeric(20,0) not null,
   TIME_pay             datetime not null,
   money_pay            float(8,2) not null,
   primary key (name, ID_loan, TIME_pay)
);

alter table CK_account add constraint FK_Inheritance_1 foreign key (ID)
      references Account (ID) on delete restrict on update restrict;

alter table Clerk add constraint FK_Belong foreign key (ID_depert)
      references department (ID_depert) on delete restrict on update restrict;

alter table Client add constraint FK_Duty foreign key (Cle_ID_card)
      references Clerk (ID_card) on delete restrict on update restrict;

alter table Contacts add constraint FK_Provide foreign key (ID_card)
      references Client (ID_card) on delete restrict on update restrict;

alter table Hold_C_L add constraint FK_Hold_C_L foreign key (ID_card)
      references Client (ID_card) on delete restrict on update restrict;

alter table Hold_C_L add constraint FK2_Hold_C_L foreign key (name, ID_loan)
      references Loans (name, ID_loan) on delete restrict on update restrict;

alter table Loans add constraint FK_GIVE foreign key (name)
      references Bank (name) on delete restrict on update restrict;

alter table SV_account add constraint FK2_Inheritance_1 foreign key (ID)
      references Account (ID) on delete restrict on update restrict;

alter table Transact add constraint FK_Matchup foreign key (ID)
      references Account (ID) on delete restrict on update restrict;

alter table Transact add constraint FK_T_B foreign key (name)
      references Bank (name) on delete restrict on update restrict;

alter table Transact add constraint FK_T_C foreign key (ID_card)
      references Client (ID_card) on delete restrict on update restrict;

alter table department add constraint FK_Hold_B_D foreign key (Ban_name)
      references Bank (name) on delete restrict on update restrict;

-- alter table department add constraint FK_Lead foreign key (ID_card)
--       references manager (ID_card) on delete restrict on update restrict;

alter table manager add constraint FK_Inheritance_2 foreign key (ID_card)
      references Clerk (ID_card) on delete restrict on update restrict;

alter table manager add constraint FK2_Lead foreign key (ID_depert)
      references department (ID_depert) on delete restrict on update restrict;

alter table payout add constraint FK_Suc_pay foreign key (name, ID_loan)
      references Loans (name, ID_loan) on delete restrict on update restrict;