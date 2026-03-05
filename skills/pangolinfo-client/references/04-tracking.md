# 追踪对象 API

## 追踪对象管理

### 对象列表
```bash
curl -s "https://extapi.pangolinfo.com/tracker/content/list?kind=amzProductDetail" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 创建追踪对象
```bash
curl -s -X POST "https://extapi.pangolinfo.com/tracker/content" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"kind":"amzProductDetail","content":"B0XXXXXX"}'
```

### 对象详情
```bash
curl -s "https://extapi.pangolinfo.com/tracker/content/details?id={id}" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 检查追踪状态
```bash
curl -s -X POST "https://extapi.pangolinfo.com/tracker/content/check-follow" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"B0XXXXXX"}'
```
