# Log Whisperer - Quick Demo Guide

## Run the Interactive Demo

```bash
cd log-whisperer
./run_demo.sh
```

Or directly:
```bash
python3 demo_interactive.py
```

## What Happens

1. **Mode Selection**: Choose your execution mode
   - `dry` - Preview only (no execution)
   - `safe` - Execute low-risk commands only
   - `full` - Execute all commands (real fix)

2. **Scenario Setup**: Creates a real git repository with a broken config

3. **Incident Simulation**: 
   - BGP config deployment 4821 breaks production
   - Empty `prefix_list` causes route withdrawal
   - Services go down

4. **Remediation**: 
   - Command: `git revert <commit> --no-commit`
   - Execution based on your selected mode

5. **Verification**: See the actual results
   - Config file changes
   - Git history updates
   - Before/after comparison

## Execution Modes Explained

### Dry Run Mode (`dry`)
- **What it does**: Shows what would happen
- **Executes commands**: No
- **Use case**: Testing, validation, demos
- **Output**: Preview of command and expected results

### Safe Mode (`safe`)
- **What it does**: Executes only low-risk commands
- **Executes commands**: Yes (if command is in safe list)
- **Use case**: Controlled remediation
- **Output**: Real execution with safety checks

### Full Mode (`full`)
- **What it does**: Executes all commands
- **Executes commands**: Yes (all commands)
- **Use case**: Production incidents, real fixes
- **Output**: Complete remediation with verification

## What You'll See

### In Dry Mode
```
✓ Preview complete - no changes made
✓ Command validated successfully
✓ Would revert commit if executed
```

### In Safe/Full Mode
```
✓ Command executed successfully
✓ Config file restored to working state
✓ Git history updated
✓ System would be healthy again
```

## Demo Flow

```
┌─────────────────────────────────────────┐
│  1. Choose Mode (dry/safe/full)        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  2. Setup: Create git repo + broken cfg │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  3. Show: Broken config state           │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  4. Execute: Run remediation command    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  5. Verify: Show results & comparison   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  6. Cleanup: Remove demo directory      │
└─────────────────────────────────────────┘
```

## Tips for Presenting

1. **Start with Dry Mode**: Show the preview without risk
2. **Explain the Scenario**: BGP config broke production
3. **Show the Broken Config**: Highlight the empty `prefix_list`
4. **Run Safe/Full Mode**: Demonstrate real execution
5. **Verify the Fix**: Show before/after comparison
6. **Highlight Key Points**:
   - Real git commands executed
   - Actual file changes
   - Git history updated
   - System would be restored

## Troubleshooting

### Git not found
```bash
# Install git
sudo apt-get install git  # Ubuntu/Debian
brew install git          # macOS
```

### Permission denied
```bash
chmod +x run_demo.sh
chmod +x demo_interactive.py
```

### Module not found
```bash
pip install -r requirements.txt
```

## Next Steps

After the demo, explore:
- `demo_council_debate.py` - See multi-agent debate
- `demo_pretty_pipeline.py` - Full pipeline with visualization
- `api/main.py` - Run the API server
- `MCP_INTEGRATION_GUIDE.md` - Learn about MCP tools

## Key Takeaways

✅ **Real Execution**: Not just mocks - actual git commands run
✅ **Safety Modes**: Three levels of control (dry/safe/full)
✅ **Visible Results**: See file changes and git history
✅ **Production Ready**: Proven functionality with real tools
✅ **Flexible**: Choose execution mode based on risk tolerance
