---
name: pangolinfo-client
description: Pangolinfo数据采集系统API调用技能包 - 使用Node.js脚本快速调用API，确保Windows环境下的UTF-8兼容性。
---

# Pangolinfo API 客户端技能

这个技能帮助用户快速调用 Pangolinfo 数据采集系统的 API，获取和管理数据。

## 使用方法

### GET 请求
node -e "fetch(\'URL\', { headers: { \'Authorization\': \'Bearer <token>\' } }).then(r => r.text()).then(console.log)"

### POST 请求
node -e "fetch(\'URL\', { method: \'POST\', headers: { \'Authorization\': \'Bearer <token>\', \'Content-Type\': \'application/json\' }, body: JSON.stringify(<json_body>) }).then(r => r.text()).then(console.log)"

## 示例

**示例 1: 获取积分使用记录**
node -e "fetch(\'https://extapi.pangolinfo.com/point_usage/list?app=data_api&startTime=2026-03-01%2000:00&endTime=2026-03-31%2023:59\', { headers: { \'Authorization\': \'Bearer <token>\' } }).then(r => r.text()).then(console.log)"

**示例 10: Amazon商品详情抓取（ScrapeAPI）**
node -e "fetch(\'https://scrapeapi.pangolinfo.com/api/v1/scrape\', { method: \'POST\', headers: { \'Authorization\': \'Bearer <token>\', \'Content-Type\': \'application/json\' }, body: JSON.stringify({ url: \'https://www.amazon.com/dp/B0DYTF8L2W\', format: \'json\', parserName: \'amzProductDetail\', bizContext: { zipcode: \'10041\' } }) }).then(r => r.text()).then(console.log)"

## 注意事项

- 使用 Node.js fetch API 可确保 Windows 系统下的 UTF-8 字符正常显示
- 需要 Node.js 18+ 环境以支持原生 fetch
