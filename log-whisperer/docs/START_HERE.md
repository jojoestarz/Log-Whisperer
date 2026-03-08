# Start Here 🚀

## Single Command to Run Everything

```bash
./run_demo.sh
```

That's it! This launches the main menu where you can choose what to do.

## What You'll See

```
┌─────────────────────────────────────────────────────┐
│              🤫 Log Whisperer                       │
│     Multi-agent incident remediation system         │
└─────────────────────────────────────────────────────┘

Available Options:
┌────────┬──────────────────────────────────┬──────────┐
│ Option │ Description                      │ API Key  │
├────────┼──────────────────────────────────┼──────────┤
│ 1      │ Full Pipeline                    │ Required │
│ 2      │ Quick Execution Demo             │ Not needed│
│ 3      │ Start API Server                 │ Required │
│ 4      │ Run Tests                        │ Optional │
│ q      │ Quit                             │ -        │
└────────┴──────────────────────────────────┴──────────┘

Select an option [1/2/3/4/q] (2):
```

## Recommended First Run

**Choose Option 2** - Quick Execution Demo
- No API key needed
- Shows execution modes (dry/safe/full)
- Runs in 30 seconds
- Proves the system works

## After That

**Choose Option 1** - Full Pipeline
- Requires API key in `.env`
- Shows AI agents in action
- Complete incident remediation
- Takes 2-3 minutes

## File Structure

```
log-whisperer/
├── main.py              ← SINGLE ENTRY POINT (start here!)
├── run_demo.sh          ← Launcher script
├── README.md            ← Overview
└── START_HERE.md        ← You are here
```

## No More Confusion

Before: 20+ demo/test files, unclear what to run
Now: **One file** - `main.py` - does everything

## Quick Commands

```bash
# Run the app
./run_demo.sh

# Or directly
python3 main.py

# That's it!
```

## Need Help?

The main menu is self-explanatory. Just run it and choose an option!

```bash
./run_demo.sh
```

Happy incident remediation! 🎉
