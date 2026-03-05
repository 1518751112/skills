# 认证与配置

## API 基础信息

- **Base URL**: `https://extapi.pangolinfo.com`
- **认证方式**: Bearer Token
- **Content-Type**: `application/json`

## 获取 Token

用户需要在 Pangolinfo 平台注册并获取 API Token。

## 使用方式

在所有 API 请求中，需要在 Header 中包含：

```bash
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

完整示例：

```bash
curl -s "https://extapi.pangolinfo.com/user/info/data_api" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 应用类型

API 支持两种应用类型：
- `data_pilot` - 数据驾驶舱
- `data_api` - 数据 API

大多数端点需要通过 `app` 参数指定应用类型。
