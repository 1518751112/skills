---
name: pangolinfo-client
description: Pangolinfo数据采集系统API调用技能包 - 使用curl命令行工具快速调用API。支持两大API系统：1) 数据采集系统API - 管理订阅计划、任务、用户信息、运行记录、追踪对象、账单订单等；2) ScrapeAPI实时抓取 - Amazon商品详情/评论/跟卖、Google搜索结果(含AI Overview)、地图数据、WIPO专利查询等。当用户需要调用Pangolinfo相关API进行数据采集或实时抓取时使用此技能。
---

# Pangolinfo API 客户端技能

这个技能帮助用户快速调用 Pangolinfo 数据采集系统的 API，获取和管理数据。

## 工作流程

1. **获取 Token**：首先询问用户的 API token
2. **理解需求**：确认用户想要调用哪个 API 端点
3. **执行调用**：使用 curl 命令调用 API
4. **返回数据**：直接展示获取到的数据

## API 基础信息

**数据采集系统 API (Data Collection API)**
- **Base URL**: `https://extapi.pangolinfo.com`
- **认证方式**: Bearer Token (在 Authorization header 中)
- **Token 获取**: 用户在对话中提供

**ScrapeAPI (实时抓取API)**
- **Base URL**: `https://scrapeapi.pangolinfo.com`
- **认证方式**: Bearer Token (在 Authorization header 中)
- **Token 获取**: 与数据采集系统API通用

## 使用方法

### GET 请求

```bash
curl -s "https://extapi.pangolinfo.com<endpoint>" \
  -H "Authorization: Bearer <token>"
```

### POST 请求

```bash
curl -s -X POST "https://extapi.pangolinfo.com<endpoint>" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '<json_body>'
```

参数说明：
- `-s`: 静默模式，不显示进度条
- `-X POST`: 指定 HTTP 方法（GET 是默认值，可省略）
- `-H`: 添加 HTTP header
- `-d`: POST 请求体（JSON 格式）

## 常用 API 端点参考

以下端点来自 OpenAPI 规范，标注 ✅ 的已验证可用：

### 用户相关
- `GET /user/info/{app}` - 获取用户信息
- `POST /user/login` - 用户登录
  - `-d '{"email":"user@example.com","password":"password"}'`
- `POST /user/reg` - 用户注册
  - `-d '{"email":"user@example.com","password":"password","phone":"18888888888","source":"{}","code":"123456"}'`

### 订阅计划
- `GET /setmeal/?app={app}` - 获取订阅计划列表 ✅
- `POST /setmeal/subscribe` - 订阅计划 ✅
  - `-d '{"productId":"5f42f9b6-5578-4689-88b3-62137ec29545","coupons":["sSDbahJd"]}'`
- `POST /setmeal/upgrade/{productId}` - 升级计划
  - `-d '{"contents":["B0XXXXXX"],"kind":"amzProductDetail"}'`
- `POST /setmeal/replace/{productId}` - 更换计划
- `POST /setmeal/cancel/{orderNo}` - 取消订阅

### 增量包
- `GET /incremental/?app={app}` - 获取增量包列表 ✅
- `POST /incremental/subscribe` - 订阅增量包 ✅
  - `-d '{"productId":"844f3ffd-eafd-4161-a1dc-ebd24a0f406d","num":1}'`

### 任务管理
- `GET /crawler/task/queryPage?pageNum={num}&pageSize={size}` - 分页查询任务列表 ✅
- `POST /crawler/task/save` - 创建/保存任务 ✅
  - `-d '{"kind":"amzProductDetail","title":"测试任务","contents":["B0XXXXXX"],"targetSite":"amz_us","runWay":"manual","cycle":"daily","requireFields":["asin","price"],"relatedFields":[],"cronExpress":[],"zipcode":"90001"}'`
- `GET /crawler/task/{taskId}` - 获取任务详情 ✅
- `POST /crawler/task/run/{taskId}` - 运行任务 ✅
- `POST /crawler/task/runOnce/{taskId}` - 运行任务一次 ✅
- `POST /crawler/task/pause/{taskId}` - 暂停任务 ✅
- `POST /crawler/task/export` - 导出任务数据 (需要kind、fileType、recordIds字段)
  - `-d '{"kind":"amzKeyword","fileType":"excel","recordIds":["<recordId>"]}'`

### 运行记录
- `GET /crawler/record/queryPage?pageNum={num}&pageSize={size}` - 分页查询运行记录 ✅

### 追踪对象
- `GET /tracker/content/list?kind={kind}&pageNum={num}&pageSize={size}` - 获取追踪对象列表 ✅
- `POST /tracker/content` - 创建追踪对象 (需要kind和contents字段)
  - `-d '{"kind":"amzKeyword","contents":["desk"]}'`
- `POST /tracker/content/check-follow` - 检查追踪状态 (需要kind和contents字段)
  - `-d '{"kind":"amzProductDetail","contents":["B0D79QCMF5","B0C1Y8Z6VT"]}'`

### 任务统计
- `GET /task/stats/tracker` - 获取追踪统计 ✅
- `GET /task/stats/object` - 获取对象统计 ✅

### 积分使用
- `GET /point_usage/list?app={app}&startTime={time}&endTime={time}` - 获取积分使用列表 ✅
- `GET /point_usage/queryPage?pageNum={num}&pageSize={size}&app={app}` - 分页查询积分使用 ✅

### 订单
- `GET /order/queryPage?pageNum={num}&pageSize={size}&app={app}` - 分页查询订单 ✅

### 商品类目
- `POST /category/check-category` - 检查类目 (需要contents字段，包含类目URL)
  - `-d '{"contents":["https://www.amazon.com/s?node=3735641"]}'`
- `GET /category/queryPage?pageNum={num}&pageSize={size}` - 分页查询类目 ✅

## ScrapeAPI 端点参考

以下为实时抓取API端点（Base URL: `https://scrapeapi.pangolinfo.com`）：

### Amazon 抓取API
- `POST /api/v1/scrape` - Amazon商品抓取（支持多种解析器）
  - `-d '{"url":"https://www.amazon.com/dp/B0XXXXXX","format":"json","parserName":"amzProductDetail","bizContext":{"zipcode":"10041"}}'`
  - 支持的parserName: amzProductDetail, amzKeyword, amzProductOfCategory, amzProductOfSeller, amzBestSellers, amzNewReleases, amzFollowSeller
- `POST /api/v1/scrape/follow-seller` - Amazon商品跟卖卖家抓取
  - `-d '{"url":"https://www.amazon.com","bizContext":{"zipcode":"10041","asin":"B0XXXXXX"}}'`
- `POST /api/v1/scrape` - Amazon商品评论抓取
  - `-d '{"url":"https://www.amazon.com","format":"json","parserName":"amzReviewV2","bizContext":{"bizKey":"review","pageCount":1,"asin":"B0XXXXXX","filterByStar":"all_stars","sortBy":"recent"}}'`

### SERP 搜索API
- `POST /api/v3/extract/search` - 异步SERP搜索任务
  - `-d '{"url":"https://www.google.com/search?q=how+java+work","timeout":25000,"callback":"","isObstinate":true}'`
- `POST /api/v3/extract/batch/search` - 批量SERP搜索任务
  - `-d '{"timeout":25000,"callback":"","urls":["https://www.google.com/search?q=how+java+work"]}'`
- `POST /api/v2/scrape` - AI模式搜索（googleAISearch）
  - `-d '{"url":"https://www.google.com/search?num=10&udm=50&q=javascript","parserName":"googleAISearch","screenshot":true,"param":["how to setup"]}'`
- `POST /api/v2/scrape` - AI Overview搜索（googleSearch）
  - `-d '{"url":"https://www.google.com/search?q=how+java+work","parserName":"googleSearch","screenshot":true}'`

### 地图数据API
- `POST /api/v3/extract/search/maps` - 地图搜索/商家列表解析
  - `-d '{"query":"restaurants near San Francisco","ll":"37.7822392,-122.4642121,13z","hl":"en","from":0,"num":50,"timeout":25000,"url":""}'`
- `POST /api/v3/extract/batch/maps` - 批量地图数据解析
  - `-d '{"querys":["restaurants near San Francisco"],"ll":"46.423669,-129.9427085,13.1z","hl":"en","from":0,"num":200,"timeout":25000,"urls":[]}'`

### WIPO 专利API
- `POST /api/v3/wipo` - WIPO专利数据查询
  - `-d '{"rd":"","status":"ACT","irn":"000298","hol":"","id":"","id_search":"","lcs":"","prod":"","source":"","ds":"AL","ed":"","from":0,"num":10}'`

## 示例

**示例 1: 获取积分使用记录**
```bash
curl -s "https://extapi.pangolinfo.com/point_usage/list?app=data_api&startTime=2026-03-01%2000:00&endTime=2026-03-31%2023:59" \
  -H "Authorization: Bearer <token>"
```

**示例 2: 获取订阅计划**
```bash
curl -s "https://extapi.pangolinfo.com/setmeal/?app=data_api" \
  -H "Authorization: Bearer <token>"
```

**示例 3: 分页查询任务列表**
```bash
curl -s "https://extapi.pangolinfo.com/crawler/task/queryPage?pageNum=1&pageSize=10" \
  -H "Authorization: Bearer <token>"
```

**示例 4: 创建任务（POST）**
```bash
curl -s -X POST "https://extapi.pangolinfo.com/crawler/task/save" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"contents":["B0XXXXXX"],"kind":"amzProductDetail"}'
```

**示例 5: 查看详细请求信息（调试用）**
```bash
curl -v "https://extapi.pangolinfo.com/setmeal/?app=data_api" \
  -H "Authorization: Bearer <token>"
```

**示例 6: 添加追踪对象（POST）**
```bash
curl -s -X POST "https://extapi.pangolinfo.com/tracker/content" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind":"amzKeyword","contents":["desk"]}'
```

**示例 7: 检查追踪状态（POST）**
```bash
curl -s -X POST "https://extapi.pangolinfo.com/tracker/content/check-follow" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind":"amzProductDetail","contents":["B0D79QCMF5","B0C1Y8Z6VT"]}'
```

**示例 8: 导出任务数据（POST）**
```bash
curl -s -X POST "https://extapi.pangolinfo.com/crawler/task/export" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind":"amzKeyword","fileType":"excel","recordIds":["<recordId>"]}'
```

**示例 9: 校验类目ID（POST）**
```bash
curl -s -X POST "https://extapi.pangolinfo.com/category/check-category" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"contents":["https://www.amazon.com/s?node=3735641"]}'
```

**示例 10: Amazon商品详情抓取（ScrapeAPI）**
```bash
curl -s -X POST "https://scrapeapi.pangolinfo.com/api/v1/scrape" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.amazon.com/dp/B0DYTF8L2W","format":"json","parserName":"amzProductDetail","bizContext":{"zipcode":"10041"}}'
```

**示例 11: Google搜索结果抓取（ScrapeAPI）**
```bash
curl -s -X POST "https://scrapeapi.pangolinfo.com/api/v3/extract/search" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.google.com/search?q=how+java+work","timeout":25000,"isObstinate":true}'
```

**示例 12: 地图数据抓取（ScrapeAPI）**
```bash
curl -s -X POST "https://scrapeapi.pangolinfo.com/api/v3/extract/search/maps" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query":"restaurants near San Francisco","ll":"37.7822392,-122.4642121,13z","hl":"en","from":0,"num":50,"timeout":25000}'
```

## 注意事项

- 始终使用用户提供的 token
- API 返回的数据直接展示给用户
- 如果 API 返回错误，清晰地告知用户错误信息
- URL 参数需要进行 URL 编码（如空格用 %20）
- 许多 queryPage 端点需要分页参数（pageNum 和 pageSize）
- POST 端点需要根据 OpenAPI 规范提供正确的请求体字段
- 建议优先使用已验证的端点（标注 ✅）
- 使用 -v 参数可以查看详细的请求和响应信息，便于调试
- 使用 -s 参数可以隐藏进度条，获得更清晰的输出
