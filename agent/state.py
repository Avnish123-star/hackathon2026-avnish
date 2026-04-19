class AgentState:
    def __init__(self, ticket):
        self.ticket = ticket
        self.reasoning = []
        self.tool_calls = []
        self.final_action = None

    def log(self, message):
        """Logs internal reasoning steps for auditability[cite: 61]."""
        self.reasoning.append(message)

    def log_tool(self, name, args, result):
        """Logs tool calls, arguments, and outcomes[cite: 61]."""
        self.tool_calls.append({
            "tool": name,
            "args": args,
            "result": result
        })

    def get_full_reasoning(self):
        """
        Consolidates all reasoning steps into a structured list.
        This ensures your Audit Log is clear and detailed[cite: 135].
        """
        return self.reasoning