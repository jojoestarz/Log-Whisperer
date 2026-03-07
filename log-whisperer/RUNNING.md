# 🔊 Log Whisperer - Currently Running

## ✅ All Services Active

### 🎨 React Frontend (Recommended)
**URL:** http://localhost:5173
- Full React UI with real-time streaming
- Interactive timeline visualization
- Modern design

### 🚀 Backend API
**URL:** http://localhost:8000
- Status: http://localhost:8000/status
- Trigger pipeline: POST http://localhost:8000/trigger
- Events stream: http://localhost:8000/events

### 📄 Simple Demo (Alternative)
**URL:** http://localhost:3000/demo.html
- Lightweight HTML version
- Same functionality as React UI
- No build required

## 🎯 How to Use

1. Open http://localhost:5173 in your browser
2. Click **"RUN LOG WHISPERER"** button
3. Watch the AI pipeline execute in real-time:
   - Logs ingested
   - Decision agent analyzes
   - Writer agent generates fix
   - Safety gate validates
4. Click **"APPROVE & EXECUTE"** when prompted
5. See MTTR drop from 57:00 → 04:12

## 📊 What You'll See

- **Baseline MTTR:** 57:00 (manual response)
- **AI-Powered MTTR:** 04:12 (automated)
- **Reduction:** 98.7%
- **Cost Savings:** ~$740K annually

## 🛑 To Stop Services

```bash
# Find and kill processes
lsof -ti:8000 | xargs kill
lsof -ti:5173 | xargs kill
lsof -ti:3000 | xargs kill
```

## 🔧 Configuration

- Demo mode is enabled (`.env` has `DEMO_MODE=true`)
- No API key needed for demo
- Uses cached responses for instant visualization

---

**Ready to visualize!** Open http://localhost:5173 now 🚀
