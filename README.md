# Lucidia Platform

**The end of technical barriers. AI-powered learning that actually works.**

```
Upload a problem → Get visual explanation → Actually understand it
```

## The Problem We Solve

- **60% of parents** can't help with their children's homework
- **40% of 4th graders** below basic reading level
- **$124.5 billion** spent on tutoring globally - but EdTech doesn't work
- Current tools: drill-and-practice that creates anxiety, not understanding

## The Lucidia Difference

| Traditional EdTech | Lucidia |
|-------------------|---------|
| Shows answers | Builds understanding |
| Text-heavy explanations | 3D visualizations |
| One-size-fits-all | Adapts to learning style |
| Forgets every session | Remembers your journey |
| Separate tools for each subject | One platform, all subjects |

## How It Works

1. **Upload** - Photo, voice, or text - however you communicate best
2. **Understand** - AI generates personalized visual explanations
3. **Practice** - Contextual problems in game-like scenarios
4. **Master** - Build conceptual understanding, not just procedures

## Quick Start

```bash
# Clone and install
git clone https://github.com/BlackRoad-OS/lucidia-platform
cd lucidia-platform

# Start the API
cd api && pip install -e . && uvicorn main:app --reload

# Start the web app (separate terminal)
cd web && npm install && npm run dev
```

## Architecture

```
lucidia-platform/
├── api/                    # FastAPI backend
│   ├── routers/           # API endpoints
│   │   ├── problems.py    # Problem upload & analysis
│   │   ├── explanations.py # AI-generated explanations
│   │   ├── visualizations.py # 3D/2D visualization generation
│   │   └── users.py       # Auth & user management
│   ├── services/          # Business logic
│   │   ├── ai_tutor.py    # Core tutoring engine
│   │   ├── memory.py      # Persistent user context
│   │   └── visualizer.py  # Visual content generation
│   └── main.py            # FastAPI app
├── web/                    # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   └── lib/               # Utilities
├── packages/              # Shared packages
│   └── lucidia-core/      # Core reasoning engines
└── deploy/                # Infrastructure
    ├── railway.toml
    └── Dockerfile
```

## Pricing

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0 | 10 problems/month, basic explanations |
| **Student** | $9.99/mo | Unlimited problems, visual explanations, memory |
| **Family** | $19.99/mo | Up to 5 users, progress tracking, parent dashboard |
| **School** | $3-8/student/yr | Admin controls, LMS integration, analytics |

## Powered By

Built on the BlackRoad OS stack:
- [lucidia-core](https://github.com/BlackRoad-OS/lucidia-core) - AI reasoning engines
- [lucidia-math](https://github.com/BlackRoad-OS/lucidia-math) - Mathematical computation
- [blackroad-agents](https://github.com/BlackRoad-OS/blackroad-agents) - Agent orchestration

## License

MIT - See [LICENSE](LICENSE) for details.

---

**Ready to transform learning?** Visit [lucidia.ai](https://lucidia.ai)

Built by [BlackRoad OS](https://blackroad.io)
