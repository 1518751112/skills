# 快速开始

## 基本用法

使用 curl 命令调用 Pangolinfo API：

```bash
curl -s "https://extapi.pangolinfo.com<endpoint>" \
  -H "Authorization: Bearer <token>"
```

## 常见示例

### 1. 查询订阅计划
```bash
curl -s "https://extapi.pangolinfo.com/setmeal/?app=data_api" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. 查询积分使用记录
```bash
curl -s "https://extapi.pangolinfo.com/point_usage/list?app=data_api&startTime=2026-03-01%2000:00&endTime=2026-03-31%2023:59" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. 获取任务列表
```bash
curl -s "https://extapi.pangolinfo.com/crawler/task/queryPage?pageNum=1&pageSize=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. 创建任务（POST 请求）
```bash
curl -s -X POST "https://extapi.pangolinfo.com/crawler/task/save" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contents":["B0XXXXXX"],"kind":"amzProductDetail"}'
```

## 注意事项

- URL 参数需要进行 URL 编码（空格 = %20）
- POST 请求的 body 必须是有效的 JSON 字符串
- Token 需要从 Pangolinfo 平台获取
- 使用 -s 参数隐藏进度条
- 使用 -v 参数查看详细调试信息
