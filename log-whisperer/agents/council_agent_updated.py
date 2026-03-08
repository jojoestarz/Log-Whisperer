# This is just the updated display_debate function to copy into council_agent.py

def display_debate(debates: list[CouncilDebate], with_delays: bool = False):
    """
    Display the council debate with colored panels and confidence bars.
    
    Args:
        debates: List of debate results from agents
        with_delays: If True, show each hypothesis with a delay (for presentations)
    """
    colors = ["cyan", "yellow", "magenta"]
    
    console.print("\n[bold white]🏛️  Council Debate in Progress[/bold white]")
    console.print("[dim]Three agents analyzing the incident...[/dim]\n")
    
    for i, debate in enumerate(debates):
        color = colors[i % len(colors)]
        
        # Add delay before showing each hypothesis (except the first)
        if with_delays and i > 0:
            DemoDelay.hypothesis_reveal()
        
        # Create panel with agent's position
        panel_content = f"[bold]{debate.hypothesis}[/bold]\n\n"
        panel_content += f"[dim]Reasoning:[/dim] {debate.reasoning}\n\n"
        panel_content += f"[dim]Confidence:[/dim] {debate.confidence:.0%}"
        
        panel = Panel(
            panel_content,
            title=f"[{color}]{debate.agent_name}[/{color}]",
            border_style=color
        )
        console.print(panel)
        
        # Show confidence bar
        bar_length = int(debate.confidence * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
        console.print(f"[{color}]{bar}[/{color}] {debate.confidence:.0%}\n")
        
        # Add brief pause after showing hypothesis for audience to read
        if with_delays:
            DemoDelay.hypothesis_read()
