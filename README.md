# Ultralearning AI System

AI 驅動的超級學習系統，基於 Scott Young 的 Ultralearning 方法論。

## 技術棧

| 層級 | 技術 |
|------|------|
| 前端 | Vue 3 + Vite + TailwindCSS + Pinia |
| 後端 | Spring Boot 3 + Spring Security (JWT) + JPA |
| AI   | Python FastAPI + Anthropic Claude API |
| 資料庫 | MySQL 8.0 |
| 部署 | Docker Compose |

## 核心功能

1. **🗺️ 元學習 (Metalearning)** — AI 自動分析主題，生成知識地圖與學習路線
2. **🎯 刻意練習 (Drill)** — 針對薄弱點生成選擇題/簡答題，即時評分反饋
3. **🗂 間隔重複 (Retrieval)** — SM-2 算法驅動的智能閃卡系統
4. **💡 費曼技巧 (Intuition)** — AI 深度解釋概念 + 個性化類比 + 教學反饋

## 快速啟動

### 1. 設定 API 金鑰

```bash
cp ai-service/.env.example ai-service/.env
# 編輯 .env，填入你的 Anthropic API Key
```

### 2. Docker Compose 啟動（推薦）

```bash
docker-compose up -d
```

訪問：`http://localhost`

### 3. 本地開發

**AI 服務 (Python)**
```bash
cd ai-service
pip install -r requirements.txt
cp .env.example .env  # 填入 API Key
python main.py
# 訪問：http://localhost:8000
```

**後端 (Spring Boot)**
```bash
cd backend
# 確保 MySQL 運行（或修改 application.yml 的連接設定）
mvn spring-boot:run
# 訪問：http://localhost:8080
```

**前端 (Vue.js)**
```bash
cd frontend
npm install
npm run dev
# 訪問：http://localhost:5173
```

## 系統架構

```
Browser
  ↓ HTTP
Vue.js (Port 80/5173)
  ↓ /api proxy
Spring Boot (Port 8080)   ←→ MySQL (Port 3306)
  ↓ HTTP
Python FastAPI (Port 8000)
  ↓ Anthropic SDK
Claude API
```

## API 端點

### Python AI Service (Port 8000)
- `POST /api/metalearning/knowledge-map` - 生成知識地圖
- `POST /api/drill/questions` - 生成練習題
- `POST /api/feedback/evaluate` - 評估回答
- `POST /api/retrieval/flashcards` - 生成閃卡
- `POST /api/intuition/feynman-explain` - 費曼解釋
- `POST /api/intuition/feynman-teach` - 費曼教學反饋（流式）

### Spring Boot (Port 8080)
- `POST /api/auth/register` - 註冊
- `POST /api/auth/login` - 登入
- `GET/POST /api/goals` - 學習目標管理
- `GET/POST /api/flashcards` - 閃卡管理
- `POST /api/ai/**` - AI 功能代理（需 JWT）
