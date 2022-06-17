# 无限层级留言

一个简单的“树形留言”网站。
“无限层级”，前后端分离。

## 功能需求：

- 用户可以在网站上注册
  - 需要填写 username, password, email。
  - username需要检查
  - password需要检查
  - email需要检查

- 用户可以在网站上登录
  - 使用username+password，或者email+password 登录
  - 提供”remember me”功能，登录后一个月内不需要重新登录
  - 如果未勾选”remember me”，则关闭浏览器后再次访问会提示注册或登录
  - 用户登录后，需要在页面上方显示用户名和Email

- 用户登录后，可以发表留言。
  - 留言长度在3~200字之间，可以为中文
  - 输入时会动态提示还可以再输入多少字
  - 会记录留言发表时间

- 可以针对某个留言进行再次评论
  - 评论输入的要求与留言相同
  - 可以针对某个评论再次评论，**不限层级**

- 用户可以查看留言
  - 只需要一个页面显示全部留言及树形嵌套的评论即可（一次性加载，不要懒加载）
  - 留言以时间倒序从上向下排列，最上面是最新的
  - 某个留言旁边可以看到发布者用户名和发表时间
  - 查看留言时不需要登录
