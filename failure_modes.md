# Failure Mode Analysis

### 1. Tool Latency & Timeout Recovery [cite: 71]
* **Scenario**: A mock tool (e.g., `get_order`) takes longer than the 2.0s threshold.
* **Response**: The `safe_call` wrapper utilizes `asyncio.wait_for` to catch the timeout.
* **Mitigation**: The system triggers a retry budget (up to 2 attempts). If the tool remains unresponsive, the ticket is gracefully escalated rather than crashing the loop, preserving system stability[cite: 71, 107].

### 2. Ambiguous Input / Data Mismatch [cite: 59]
* **Scenario**: A ticket body contains a typo in the Order ID (e.g., "ORD-XXXX") or is missing customer details.
* **Response**: The Regex extraction fails to find a valid ID, and the tool returns `None`.
* **Mitigation**: The agent detects the "Missing Context" during the decision phase. Instead of making a "black-box" guess, it performs an **Intelligent Escalation**, handing off to a human with a summary of exactly what data was missing[cite: 58, 75].

### 3. Malformed Tool Output [cite: 107]
* **Scenario**: A tool returns data in an unexpected format or a string containing "error".
* **Response**: The `orchestrator.py` logic includes schema validation (`isinstance(order, dict)`).
* **Mitigation**: If the data is corrupted, the `can_resolve` flag is set to `False`. This ensures the agent never takes an "Irreversible Action" (like a refund) on bad data[cite: 94, 95].