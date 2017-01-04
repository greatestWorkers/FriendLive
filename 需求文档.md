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
  <td>userId</td>
  <td>用户ID(手机号)</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>password</td>
  <td>密码</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>gender</td>
  <td>性别</td>
  <td>bool</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>nickname</td>
  <td>名字</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>headImage</td>
  <td>头像</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>token</td>
  <td>序列号</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>liveStatus</td>
  <td>直播状态</td>
  <td>bool</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>isAdmin</td>
  <td>是否为管理员</td>
  <td>bool</td>
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
  <td>userId1</td>
  <td>用户1</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>userId2</td>
  <td>用户2</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
</table>

用户-房间关联表<br>
<table>
<tr>
  <th>字段名</th>
  <th>中文</th>
  <th>类型</th>
  <th>长度</th>
  <th>是否允许空</th>
</tr>
<tr>
  <td>userId</td>
  <td>用户ID</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>roomId</td>
  <td>房间ID</td>
  <td>varchar</td>
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

IP安全数据表<br>
<table>
<tr>
  <th>字段名</th>
  <th>中文</th>
  <th>类型</th>
  <th>长度</th>
  <th>是否允许空</th>
</tr>
<tr>
  <td>userId</td>
  <td>用户ID</td>
  <td>varchar</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>IP</td>
  <td>请求次数</td>
  <td>最近请求时间</td>
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
  
  
  
