# 遇见 - 学生心理支持咖啡预约系统

一个帮助学生预约心理咨询老师的在线平台。

## 功能特点

- 用户注册与登录（学生/教师角色）
- 教师信息展示与搜索
- 在线预约心理咨询
- 预约状态管理
- 费用申请与报销
- 反馈与评价系统

## 技术栈

- **前端**: React + Vite + Ant Design
- **后端**: Flask + SQLAlchemy
- **数据库**: SQLite（可切换至 PostgreSQL/MySQL）
- **认证**: JWT

## 本地运行

### 环境要求

- Python 3.10+
- Node.js 18+

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/your-username/遇见.git
cd 遇见
```

2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 运行应用
```bash
python app.py
```

4. 访问 http://localhost:5000

## 部署到 Heroku

1. 创建 Heroku 应用
```bash
heroku create your-app-name
```

2. 添加 PostgreSQL 数据库（可选）
```bash
heroku addons:create heroku-postgresql:mini
```

3. 设置环境变量
```bash
heroku config:set SECRET_KEY=your-secret-key
```

4. 推送部署
```bash
git push heroku main
```

## 部署到其他平台

### Railway

1. 连接 GitHub 仓库
2. 选择项目根目录
3. Railway 会自动检测 Procfile 并部署

### Render

1. 创建新的 Web Service
2. 连接 GitHub 仓库
3. 设置:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && gunicorn app:app`

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| SECRET_KEY | Flask 密钥 | your-secret-key |
| DATABASE_URL | 数据库连接字符串 | sqlite:///coffee_app.db |

## 项目结构

```
遇见/
├── backend/
│   ├── app.py          # Flask 应用主文件
│   ├── requirements.txt # Python 依赖
│   ├── Procfile        # Heroku 部署配置
│   └── runtime.txt     # Python 版本
├── frontend/
│   ├── index.html      # 入口 HTML
│   └── assets/         # 静态资源
└── README.md
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/register | 用户注册 |
| POST | /api/login | 用户登录 |
| GET | /api/teachers | 获取教师列表 |
| GET | /api/teachers/:id | 获取教师详情 |
| POST | /api/appointments | 创建预约 |
| PUT | /api/appointments/:id | 更新预约状态 |
| GET | /api/appointments/student/:id | 获取学生预约 |
| GET | /api/appointments/teacher/:id | 获取教师预约 |
| POST | /api/expenses | 创建费用申请 |
| PUT | /api/expenses/:id | 更新费用状态 |
| POST | /api/feedbacks | 提交反馈 |

## License

MIT
