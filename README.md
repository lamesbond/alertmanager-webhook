# alertmanager-webhook
alertmanager-webhook接收alertmanager的告警，发送到微信，钉钉，邮件，目前只做了微信

首先得搭建prometheus和alertmanager，能触发告警规则，注册一个企业微信，新建企业，微信不要求企业认证，任何人都可以建企业，获取企业ID
![image](https://user-images.githubusercontent.com/53105658/157872228-621bb424-46a4-474d-93bd-5deab29e3e64.png)
创建企业后新建企业应用
![MCE_XPRPY{(N7K%($_E~NQF](https://user-images.githubusercontent.com/53105658/157871695-aaba0b2d-5879-4aa5-8e6b-2813a125d492.png)
企业建好后创建应用，获取AgentId和Secret，然后在接收消息那里填企业微信回调的url
![PY} 9PBMT{9``R{~2 11R1W](https://user-images.githubusercontent.com/53105658/157872995-dd0cc6e2-545c-4fdf-9b39-5ac683939968.png)
url就是企业微信要访问的地址，需要是公网IP，放云上就行，如果用域名得是备案过的域名，Token和EncodingAESKey随机生成就行
![`Q$4{(FQ9S~7JSTT8%%QAGR](https://user-images.githubusercontent.com/53105658/157873198-3bc97d8f-47b6-4d51-bb7c-27063bb5ac10.png)
把企业ID，应用的AgentId和Secret，回调的Token和EncodingAESKey填到项目里面
![EKYVP00)6ILTRZHPX4OX~R4](https://user-images.githubusercontent.com/53105658/157871296-e842c560-7787-4488-a647-b4b71691df2a.png)

receivers:
- name: 'wechat'
  webhook_configs:
  - url: "http://yourhostip:9096/wechat_send"
