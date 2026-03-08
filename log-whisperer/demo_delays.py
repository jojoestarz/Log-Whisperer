"""
Demo mode delay configuration for presentation-friendly pacing.

Delays are calibrated for:
- Audience comprehension (time to read)
- Realistic processing simulation
- Maintaining engagement (not too slow)
"""

import time
from rich.console import Console

console = Console()


class DemoDelay:
    """Centralized delay management for demo mode."""
    
    # Event delays (in seconds)
    INGESTION = 1.2          # Loading and parsing logs
    INITIATE_ANALYSIS = 0.8  # Starting analysis
    AGENT_THINKING = 2.0     # Each agent analyzing
    AGENT_COMPLETE = 0.6     # Agent finished message
    HYPOTHESIS_REVEAL = 1.2  # Between hypothesis displays
    HYPOTHESIS_READ = 0.8    # Time to read each hypothesis
    CONSENSUS_START = 0.8    # Starting consensus
    CONSENSUS_PROCESS = 2.5  # Building consensus
    PLAN_GENERATION = 1.8    # Generating remediation plan
    PLAN_EXPLANATION = 1.5   # Explaining the plan
    COMMAND_DISPLAY = 1.0    # Showing each command
    COMMAND_DETAIL = 0.8     # Command details
    
    @staticmethod
    def wait(duration: float, message: str = None):
        """
        Wait with optional status message.
        
        Args:
            duration: Seconds to wait
            message: Optional message to display
        """
        if message:
            console.print(f"[dim]{message}[/dim]")
        time.sleep(duration)
    
    @staticmethod
    def ingestion():
        """Delay for log ingestion."""
        DemoDelay.wait(DemoDelay.INGESTION, "📥 Ingesting incident logs...")
    
    @staticmethod
    def initiate_analysis():
        """Delay for starting analysis."""
        DemoDelay.wait(DemoDelay.INITIATE_ANALYSIS, "🔍 Initiating analysis...")
    
    @staticmethod
    def agent_thinking(agent_name: str):
        """Delay for agent processing."""
        DemoDelay.wait(DemoDelay.AGENT_THINKING, f"💭 {agent_name} analyzing...")
    
    @staticmethod
    def agent_complete():
        """Brief pause after agent completes."""
        time.sleep(DemoDelay.AGENT_COMPLETE)
    
    @staticmethod
    def hypothesis_reveal():
        """Delay between hypothesis reveals."""
        time.sleep(DemoDelay.HYPOTHESIS_REVEAL)
    
    @staticmethod
    def hypothesis_read():
        """Time to read a hypothesis."""
        time.sleep(DemoDelay.HYPOTHESIS_READ)
    
    @staticmethod
    def consensus_start():
        """Delay for starting consensus."""
        DemoDelay.wait(DemoDelay.CONSENSUS_START, "🤝 Initiating consensus protocol...")
    
    @staticmethod
    def consensus_process():
        """Delay for consensus building."""
        DemoDelay.wait(DemoDelay.CONSENSUS_PROCESS, "⚖️  Synthesizing expert opinions...")
    
    @staticmethod
    def plan_generation():
        """Delay for plan generation."""
        DemoDelay.wait(DemoDelay.PLAN_GENERATION, "⚙️  Generating remediation plan...")
    
    @staticmethod
    def plan_explanation():
        """Delay for plan explanation."""
        time.sleep(DemoDelay.PLAN_EXPLANATION)
    
    @staticmethod
    def command_display():
        """Delay between commands."""
        time.sleep(DemoDelay.COMMAND_DISPLAY)
    
    @staticmethod
    def command_detail():
        """Delay for command details."""
        time.sleep(DemoDelay.COMMAND_DETAIL)
