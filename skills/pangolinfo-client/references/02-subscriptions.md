# 订阅计划 API

## 主要端点

### 获取计划列表
```bash
curl -s "https://extapi.pangolinfo.com/setmeal/?app=data_api" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 订阅计划
```bash
curl -s -X POST "https://extapi.pangolinfo.com/setmeal/subscribe" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId":"xxx"}'
```

### 升级计划
```bash
curl -s -X POST "https://extapi.pangolinfo.com/setmeal/upgrade/{productId}" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

## 增量包

### 增量包列表
```bash
curl -s "https://extapi.pangolinfo.com/incremental/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 购买增量包
```bash
curl -s -X POST "https://extapi.pangolinfo.com/incremental/subscribe" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId":"xxx"}'
```
