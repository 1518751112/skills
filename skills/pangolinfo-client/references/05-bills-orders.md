# 账单与订单 API

## 积分账单

### 积分使用记录
```bash
curl -s "https://extapi.pangolinfo.com/point_usage/list?app=data_api&startTime=2026-03-01%2000:00&endTime=2026-03-31%2023:59" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 分页查询积分使用
```bash
curl -s "https://extapi.pangolinfo.com/point_usage/queryPage?pageNum=1&pageSize=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 导出积分使用记录
```bash
curl -s -X POST "https://extapi.pangolinfo.com/point_usage/export" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startTime":"2026-03-01","endTime":"2026-03-31"}'
```

## 订单管理

### 订单列表
```bash
curl -s "https://extapi.pangolinfo.com/order/queryPage?pageNum=1&pageSize=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 分页获取订单
```bash
curl -s "https://extapi.pangolinfo.com/order/listByPage/data_api/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```
