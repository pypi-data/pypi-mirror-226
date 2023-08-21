
# YunXiao API
An API tool for YunXiao Education Institution Management System.


# Copyright Statement
YunXiao software is owned by XiaoGuanJia. This project is for learning purposes only. If there is any infringement, please contact me to delete.


# Contact
admin@sqkkyzx.com


# API Endpoint

## V2

- ### arranges_query_date

` 列出日期范围全部排课[最大9999条] ` 

| Parameter | Description |
|-----------|-------------|
| teacherids | 老师ID |
| date | 查询日期 **2020-02-20** |


- ### arranges_query_daterange

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### campus_query

` 查询全部校区 ` 

| Parameter | Description |
|-----------|-------------|


- ### campus_query_performance_date

` 分校区列出指定日期的费用数据。 ` 

| Parameter | Description |
|-----------|-------------|
| date | 日期 |


- ### campus_query_performance_daterange

` 查询指定日期范围业绩。 ` 

| Parameter | Description |
|-----------|-------------|
| startdate | 起始日期 |
| enddate | 截止日期 |


- ### charges_query_detail

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### charges_query_record

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### class_query_arrange

` 查询班级排课 ` 

| Parameter | Description |
|-----------|-------------|
| classid | 班级ID |


- ### class_query_info

` 查询指定班级信息 ` 

| Parameter | Description |
|-----------|-------------|
| classid | 班级id |


- ### class_query_student

` 查询班级学生 ` 

| Parameter | Description |
|-----------|-------------|
| inout | **[1]** 当前在班学员 **[2]** 历史学员 |
| classid | 班级ID |


- ### classes_query

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### comefroms_query

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### company_query_performance_month

` 查询指定月份的每日费用数据 ` 

| Parameter | Description |
|-----------|-------------|
| yy_mm | 查询月份，默认为本月。**2023-02** |


- ### curriculums_query

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### loop

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### order_query_info

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### orders_query

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### orders_query_items

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### orders_query_refund

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### payments_query

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### payments_query_receipt

` 取得收据信息。 ` 

| Parameter | Description |
|-----------|-------------|
| order_id | 订单 ID |
| payment_group_id | 支付 ID |


- ### payments_query_record

` 列出指定操作日期范围的所有订单记录 ` 

| Parameter | Description |
|-----------|-------------|
| enddate | YY-MM-DD |
| startdate | YY-MM-DD |


- ### payments_query_refund

` 查询指定操作日期范围的所有退费 ` 

| Parameter | Description |
|-----------|-------------|
| enddate | YY-MM-DD |
| startdate | YY-MM-DD |


- ### renew_cookie

` 刷新 cookie.tmp 配置中存储的 cookie ` 

| Parameter | Description |
|-----------|-------------|


- ### renew_token

` 刷新 token.tmp 配置中存储的 token ` 

| Parameter | Description |
|-----------|-------------|


- ### request

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### student_operation__history

` 设置学生为曾就读。 ` 

| Parameter | Description |
|-----------|-------------|
| studentlist | 学生ID |


- ### student_operation_suspend

` 设置学生为停课。 ` 

| Parameter | Description |
|-----------|-------------|
| student_id | 学生ID |
| suspend_course_date | 停课时间。0000-00-00 |
| remove_class | 是否从班级中移除 |


- ### student_query_cards

` 查看学员的课程卡包 ` 

| Parameter | Description |
|-----------|-------------|
| studentid | 学生ID |


- ### student_query_class_records

` [工作台][学员][就读课程][出入班记录] ` 

| Parameter | Description |
|-----------|-------------|
| studentid | 学生ID |
| curriculum_id | 课程ID |


- ### student_query_course

` 查看学员的课程卡包 ` 

| Parameter | Description |
|-----------|-------------|
| studentid | 学生ID |


- ### student_query_info

` 查询学生基本信息 ` 

| Parameter | Description |
|-----------|-------------|
| companyid | 机构ID |
| studentid | 学员ID |


- ### students_query

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### students_query_cards

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### students_query_course_amount

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### students_query_course_fee

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### teacher_query_arrange

` 取得指定老师的课表。 ` 

| Parameter | Description |
|-----------|-------------|
| teacher_id | 查询的老师ID |
| start_date | 起始日期，默认为本周一 |
| end_date | 结束日期，默认为本周日 |


- ### teachers_query

` 查询老师。 ` 

| Parameter | Description |
|-----------|-------------|
| size | 查询数量，最大 200 |
| status | 老师状态。 **1** 在职 **0** 离职 |
| name | 查询教师的姓名 |


