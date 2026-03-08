# How to Use the Interactive Demo

## Step-by-Step Guide

### 1. Start the Demo
```bash
cd log-whisperer
./run_demo.sh
```

### 2. Select Your Mode

You'll see a table like this:
```
┌─────────────────────────────────────────────────────────────────────┐
│                         Execution Modes                             │
├────────────┬──────────────────────────────────────────┬────────────┤
│ Mode       │ Description                              │ Executes?  │
├────────────┼──────────────────────────────────────────┼────────────┤
│ dry        │ Preview mode - shows what would happen   │ No         │
│ safe       │ Safe mode - executes low-risk commands   │ Yes (safe) │
│ full       │ Full mode - executes all commands        │ Yes (all)  │
└────────────┴──────────────────────────────────────────┴────────────┘

Type one of: dry, safe, or full (then press Enter)
Select execution mode [dry/safe/full] (dry): _
```

### 3. Type Your Choice

**Just type the mode name:**
- Type `dry` and press Enter
- Type `safe` and press Enter  
- Type `full` and press Enter
- Or just press Enter to use the default (dry)

**Important:** 
- ❌ Don't use arrow keys
- ❌ Don't try to click
- ✅ Just type the word and press Enter

### 4. Follow the Prompts

The demo will guide you through:
- Press Enter to see the broken config
- Press Enter to execute the remediation
- Press Enter to cleanup

## Quick Examples

### Example 1: Safe Preview (Dry Mode)
```bash
./run_demo.sh
# When prompted, type: dry
# Press Enter
# Follow the prompts
```

### Example 2: See Real Execution (Full Mode)
```bash
./run_demo.sh
# When prompted, type: full
# Press Enter
# Watch the real git commands execute!
```

### Example 3: Use Default
```bash
./run_demo.sh
# When prompted, just press Enter (uses dry mode)
```

## What Each Mode Does

### Dry Mode (dry)
```
✓ Shows what would happen
✓ No actual execution
✓ Safe for testing
✓ Good for first run
```

### Safe Mode (safe)
```
✓ Executes low-risk commands
✓ Real git operations
✓ Controlled execution
✓ Good for demos
```

### Full Mode (full)
```
✓ Executes all commands
✓ Real remediation
✓ Shows complete fix
✓ Proves functionality
```

## Common Issues

### "I can't select with arrow keys"
That's normal! Just type the mode name:
```
Select execution mode [dry/safe/full] (dry): full
```
Type `full` and press Enter.

### "Nothing happens when I click"
Mouse doesn't work here. Type the mode name instead.

### "What if I make a typo?"
The prompt will ask again if you type something invalid:
```
Select execution mode [dry/safe/full] (dry): ful
Please select one of dry, safe, full
Select execution mode [dry/safe/full] (dry): full
```

### "Can I just press Enter?"
Yes! It will use the default mode (dry).

## Tips

1. **First time?** Use `dry` mode to see what happens
2. **Want to see real execution?** Use `full` mode
3. **Presenting to others?** Use `full` mode for impact
4. **Testing changes?** Use `dry` mode for safety
5. **Not sure?** Just press Enter for default

## The Complete Flow

```
1. Run: ./run_demo.sh
   ↓
2. Type mode: dry / safe / full
   ↓
3. Press Enter
   ↓
4. Press Enter to see broken config
   ↓
5. Press Enter to execute remediation
   ↓
6. See results (based on your mode)
   ↓
7. Press Enter to cleanup
   ↓
8. Done! 🎉
```

## Need Help?

- Read [RUN_DEMO.md](RUN_DEMO.md) for more details
- Read [DEMO_QUICK_START.md](DEMO_QUICK_START.md) for presentation tips
- Read [SETUP.md](SETUP.md) for installation help

Happy demoing! 🚀
