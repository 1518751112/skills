# 任务管理 API

## 任务操作

### 任务列表（分页）
```bash
curl -s "https://extapi.pangolinfo.com/crawler/task/queryPage?pageNum=1&pageSize=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 创建任务
```bash
curl -s -X POST "https://extapi.pangolinfo.com/crawler/task/save" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contents":["B0XXXXXX"],"kind":"amzProductDetail"}'
```

### 运行任务
```bash
curl -s -X POST "https://extapi.pangolinfo.com/crawler/task/run/{taskId}" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### 暂停任务
```bash
curl -s -X POST "https://extapi.pangolinfo.com/crawler/task/pause/{taskId}" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

## 运行记录

### 获取运行记录
```bash
curl -s "https://extapi.pangolinfo.com/crawler/record/queryPage?pageNum=1&pageSize=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```
