# 用户管理 API

## 用户信息

### 当前用户信息
```bash
curl -s "https://extapi.pangolinfo.com/user/info/data_api" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 用户登录
```bash
curl -s -X POST "https://extapi.pangolinfo.com/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'
```

### 用户注册
```bash
curl -s -X POST "https://extapi.pangolinfo.com/user/reg" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'
```
