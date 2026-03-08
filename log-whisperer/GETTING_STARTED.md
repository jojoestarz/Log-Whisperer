# Getting Started with Log Whisperer

## 5-Minute Quick Start

### Step 1: Install Dependencies (2 min)
```bash
cd log-whisperer
pip install -r requirements.txt
```

### Step 2: Run the Demo (3 min)
```bash
./run_demo.sh
```

That's it! The demo will:
1. Ask you to choose a mode (dry/safe/full)
2. Create a test scenario
3. Show you how Log Whisperer fixes incidents
4. Clean up automatically

## What to Try

### First Time: Dry Mode
```
Select: dry
```
- Safe to run
- Shows preview only
- No actual changes
- Perfect for understanding the system

### Second Time: Full Mode
```
Select: full
```
- See real execution
- Actual git commands run
- Files change
- Git history updates
- Proves functionality

## Next Steps

### 1. Explore Other Demos
```bash
# See the multi-agent debate
python3 demo_council_debate.py

# See the full pipeline
python3 demo_pretty_pipeline.py
```

### 2. Run Tests
```bash
# Test real execution
python3 test_real_execution.py

# Test council agent
python3 test_council_agent.py
```

### 3. Start the API Server
```bash
# Configure your API key
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY

# Start server
python3 api/main.py
```

### 4. Read the Guides
- [SETUP.md](SETUP.md) - Detailed setup instructions
- [DEMO_QUICK_START.md](DEMO_QUICK_START.md) - Demo presentation guide
- [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md) - MCP tools integration

## Troubleshooting

### Dependencies not installed?
```bash
pip install -r requirements.txt
```

### Git not found?
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git
```

### Permission denied?
```bash
chmod +x run_demo.sh
```

## Understanding the System

### Execution Modes
- **dry** - Preview only, no execution
- **safe** - Execute low-risk commands only
- **full** - Execute all commands

### Components
- **Council Agent** - Multi-agent debate for root cause analysis
- **Writer Agent** - Generates remediation commands
- **Executor** - Runs commands with safety checks
- **Terminal Grid** - Real-time infrastructure visualization
- **Terminal Logger** - Pretty event logging

### Flow
```
Incident → Council Debate → Generate Plan → 
Safety Check → Human Approval → Execute → Verify
```

## Quick Reference

### Run Interactive Demo
```bash
./run_demo.sh
```

### Run Specific Demo
```bash
python3 demo_council_debate.py      # Multi-agent debate
python3 demo_pretty_pipeline.py     # Full pipeline
python3 demo_real_execution.py      # Execution comparison
```

### Run Tests
```bash
python3 test_real_execution.py      # Test executor
python3 test_council_agent.py       # Test council
python3 test_writer_agent.py        # Test writer
```

### Start API
```bash
python3 api/main.py
```

## Common Questions

### Q: Is this safe to run?
A: Yes! The demo creates a temporary directory and cleans up automatically. In dry mode, nothing is executed.

### Q: Do I need an API key?
A: Not for the interactive demo. Only needed for the full pipeline with AI agents.

### Q: What does the demo actually do?
A: Creates a git repo, commits a broken config, then shows how Log Whisperer would fix it using git revert.

### Q: Can I use this in production?
A: The execution system is functional. You'd need to:
1. Connect to your real infrastructure
2. Configure proper authentication
3. Set up monitoring and alerting
4. Implement approval workflows

### Q: What about MCP tools?
A: MCP integration is documented but not implemented. See [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md) for details.

## Success Checklist

- [ ] Dependencies installed
- [ ] Demo runs successfully
- [ ] Tried dry mode
- [ ] Tried full mode
- [ ] Saw real git execution
- [ ] Understood execution modes
- [ ] Read the documentation
- [ ] Explored other demos

## Need Help?

1. Check [SETUP.md](SETUP.md) for detailed setup
2. Check [DEMO_QUICK_START.md](DEMO_QUICK_START.md) for demo tips
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
4. Read the code - it's well documented!

## What's Next?

After getting started:

1. **Customize** - Adapt for your infrastructure
2. **Integrate** - Connect to your monitoring
3. **Extend** - Add new agents or tools
4. **Deploy** - Run in your environment
5. **Contribute** - Share improvements

Happy incident remediation! 🚀
