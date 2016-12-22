#友播系统文档
简述：实现一个基于好友管理的直播应用

##功能：
###1.注册
  通过手机号(phoneNumber)和密码(password)以及验证码进行注册
  
###2.登录
  通过手机号(phoneNumber)和密码(password)进行登录，登录时进行手机验证码验证
    
###3.好友管理
  3.1 搜索好友 <br>
  根据手机号来搜索指定的用户，找到则显示该用户的信息，未找到则提示该用户不存在
  
  3.2 添加好友 <br>
  找到指定好友后，点击加为好友，向指定好友发送申请，对方通过后则提示添加成功，对方拒绝则提示拒绝信息。
  
  3.3 删除好友 <br>
  从好友列表中选中某好友，点击删除，从好友列表中删除该项。
  
  3.4 显示好友列表<br>
  进入应用后首先展示我的所有好友，每一行展示该好友的头像，昵称，直播状态。
  
  3.5 消息
  进入消息页面，查看待处理的好友申请请求，同意则加为好友，拒绝则拒绝添加。
  

###4.直播间
  4.1 评论<br>
  4.2 主播创建直播间，关闭直播间<br>
  4.3 用户进入直播间，用户退出直播间<br>
  
#数据表<br>
用户表
<table>
<tr>
  <th>字段名</th>
  <th>中文</th>
  <th>类型</th>
  <th>长度</th>
  <th>是否允许空</th>
</tr>
<tr>
  <td>用户id</td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
  
</table>
<br>
好友关系表
<table>
<tr>
  <th>字段名</th>
  <th>中文</th>
  <th>类型</th>
  <th>长度</th>
  <th>是否允许空</th>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
</table>
直播间表<br>
<table>
<tr>
  <th>字段名</th>
  <th>中文</th>
  <th>类型</th>
  <th>长度</th>
  <th>是否允许空</th>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
</tr>
</table>
  

  
  
  
  