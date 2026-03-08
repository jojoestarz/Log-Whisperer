# Demo Guide: Proving Real Execution Works

## Quick Demo (5 minutes)

The fastest way to prove real execution is functional:

```bash
cd log-whisperer
python demo_live_execution.py
```

**What you'll see:**
1. ✅ Creates a real git repository
2. ✅ Commits a "broken" config file
3. ✅ Shows DRY_RUN mode (preview only)
4. ✅ Shows SAFE mode (controlled execution)
5. ✅ Shows FULL mode (actual execution)
6. ✅ Displays before/after config comparison
7. ✅ Proves the git revert actually worked

**Interactive:** Press Enter to advance through each step.

## Demo Options

### Option 1: Live Interactive Demo (Recommended)
**Best for:** Live presentations, stakeholder demos

```bash
python demo_live_execution.py
```

**Shows:**
- Real git repository creation
- Broken config scenario
- All three execution modes
- Before/after comparison
- Actual file changes
- Git history updates

**Duration:** 5 minutes  
**Interaction:** Press Enter to advance

### Option 2: Automated Test Suite
**Best for:** Technical validation, CI/CD

```bash
python test_real_execution.py
```

**Shows:**
- 5 automated tests
- Real git operations
- All execution modes
- Error handling
- Success/failure reporting

**Duration:** 10 seconds  
**Interaction:** None (fully automated)

### Option 3: Full Pipeline Demo
**Best for:** End-to-end demonstration

```bash
python demo_real_execution.py
```

**Shows:**
- Council debate (3 AI agents)
- Remediation plan generation
- All execution modes explained
- Configuration options
- Mode comparison table

**Duration:** 3 minutes  
**Interaction:** Minimal

## What Each Demo Proves

### Live Interactive Demo Proves:

1. **Real Repository Operations**
   ```
   📁 Demo directory: /tmp/log_whisperer_demo_xyz
   ✓ Created initial working config
   ✗ Created broken config (commit: abc123de)
   ```

2. **Actual File Changes**
   ```yaml
   # BEFORE
   prefix_list: ""  # ← BROKEN
   
   # AFTER  
   prefix_list:
     - 198.41.200.0/24
     - 172.64.0.0/13
   ```

3. **Real Git Commands**
   ```bash
   Executed: True
   Success: True
   Command: git revert abc123de --no-commit
   ```

4. **Visible Results**
   ```
   Git Status:
   M  bgp-config.yaml
   
   Git History (after revert):
   def456 Revert "Deploy 4821 - BROKEN CONFIG"
   abc123 Deploy 4821 - BROKEN CONFIG
   789012 Initial config - working
   ```

### Test Suite Proves:

1. **DRY_RUN Mode**
   ```
   ✓ DRY_RUN mode works correctly
   Mode: dry_run
   Executed: False
   Output: [DRY RUN] Would execute: git revert abc123 --no-commit
   ```

2. **SAFE Mode**
   ```
   ✓ SAFE mode blocks unsafe commands
   Mode: safe
   Success: False
   Error: Command service_restart not in safe list
   ```

3. **FULL Mode**
   ```
   ✓ Real git execution works!
   Mode: full
   Executed: True
   Success: True
   ```

4. **Error Handling**
   ```
   ✓ Handles missing commands gracefully
   ✓ Multiple command execution works
   ```

## Demo Script for Presentations

### Setup (30 seconds)
```bash
cd log-whisperer
python demo_live_execution.py
```

### Act 1: The Problem (1 minute)
**Say:** "We have a broken BGP config that caused an outage."

**Show:** 
- Broken config file with empty prefix_list
- Git history showing the bad commit

**Point out:**
- This is a real git repository
- The config file actually exists
- The commit is real

### Act 2: The Solution (2 minutes)
**Say:** "Log Whisperer can fix this automatically."

**Show:**
- DRY_RUN mode (preview)
- SAFE mode (controlled)
- FULL mode (actual execution)

**Point out:**
- Three safety levels
- Real subprocess execution
- Actual command output

### Act 3: The Proof (2 minutes)
**Say:** "Let's verify it actually worked."

**Show:**
- Git status (modified file)
- Fixed config file
- Updated git history
- Before/after comparison

**Point out:**
- File content changed
- Git history updated
- System would be healthy

### Conclusion (30 seconds)
**Say:** "This proves real execution is functional."

**Highlight:**
- Real git operations
- Actual file changes
- Production-ready
- Safety controls

## Key Talking Points

### For Technical Audiences

1. **"This uses subprocess.run() for real execution"**
   - Not mocked
   - Actual system calls
   - Real return codes

2. **"Three safety modes protect against accidents"**
   - DRY_RUN: Preview only
   - SAFE: Filtered execution
   - FULL: Complete execution

3. **"Error handling is comprehensive"**
   - Timeouts
   - Command not found
   - Permission errors
   - Execution failures

4. **"It's production-ready"**
   - Tested thoroughly
   - Proper logging
   - Stop on failure
   - Rollback support

### For Non-Technical Audiences

1. **"The system can actually fix problems"**
   - Not just recommendations
   - Real actions
   - Measurable results

2. **"Safety controls prevent mistakes"**
   - Preview mode
   - Approval required
   - Risk assessment

3. **"It's faster than manual fixes"**
   - Seconds vs minutes
   - Automated execution
   - Consistent results

4. **"You can see it working"**
   - Visual feedback
   - Before/after comparison
   - Clear success indicators

## Common Questions & Answers

**Q: Is this really executing commands?**  
A: Yes! Run `python test_real_execution.py` to see real git operations.

**Q: What if something goes wrong?**  
A: Three safety modes, timeouts, stop-on-failure, and comprehensive error handling.

**Q: Can I see the actual code?**  
A: Yes! Check `execution/executor.py` - it uses `subprocess.run()`.

**Q: How do I know it's not mocked?**  
A: The demo creates a real git repo, you can inspect the files and git history.

**Q: What commands are supported?**  
A: git revert, kubectl apply/scale/restart, argocd sync - all real CLI tools.

**Q: Is it safe for production?**  
A: Yes, with SAFE or FULL mode after human approval. DRY_RUN for testing.

## Troubleshooting Demo Issues

### Demo won't start
```bash
# Check Python environment
python --version  # Should be 3.10+

# Check dependencies
pip install -r requirements.txt

# Check git is installed
git --version
```

### "Command not found: git"
```bash
# Install git
sudo apt-get install git  # Ubuntu/Debian
brew install git           # macOS
```

### Demo directory not cleaned up
```bash
# Manual cleanup
rm -rf /tmp/log_whisperer_demo_*
```

### Want to see more detail
```bash
# Run with verbose logging
LOG_LEVEL=DEBUG python demo_live_execution.py
```

## Recording the Demo

### For Screenshots
1. Run `python demo_live_execution.py`
2. Screenshot at each "Press Enter" pause
3. Capture before/after comparison
4. Show git history

### For Video
1. Start screen recording
2. Run `python demo_live_execution.py`
3. Narrate each step
4. Highlight key outputs
5. Show final verification

### For Documentation
1. Run demo
2. Copy terminal output
3. Add to documentation
4. Include before/after configs

## Next Steps After Demo

1. **Try different modes**
   ```bash
   EXECUTION_MODE=dry_run python demo_real_execution.py
   EXECUTION_MODE=safe python demo_real_execution.py
   ```

2. **Run full test suite**
   ```bash
   python test_real_execution.py
   ```

3. **Integrate with your infrastructure**
   - Setup kubectl access
   - Configure Argo CD
   - Prepare git repositories

4. **Customize for your needs**
   - Add new commands
   - Adjust safety rules
   - Configure timeouts

## Summary

The demos prove real execution is functional by:
- ✅ Creating actual git repositories
- ✅ Executing real commands
- ✅ Showing visible file changes
- ✅ Displaying git history updates
- ✅ Demonstrating all safety modes
- ✅ Handling errors gracefully

**Run `python demo_live_execution.py` to see it yourself!** 🎉
