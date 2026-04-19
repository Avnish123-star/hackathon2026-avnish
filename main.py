import asyncio
import json
import os
from agent.orchestrator import process_ticket_async

async def main():
    # 1. Robust Path Resolution [cite: 12, 139]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mock_dir = os.path.join(current_dir, 'mock')
    
    # --- DEBUG SECTION: Identifying the File Path Issue ---
    if os.path.exists(mock_dir):
        # This will list every file in the 'mock' folder so you can see the real name
        folder_contents = os.listdir(mock_dir)
        print(f"📂 Folder 'mock' found at: {mock_dir}")
        print(f"🔍 Contents of 'mock': {folder_contents}")
    else:
        print(f"❌ Folder 'mock' NOT found at: {mock_dir}")
        print(f"💡 Troubleshooting: Create a folder named 'mock' in {current_dir}")
        return
    # ------------------------------------------------------

    tickets_path = os.path.join(mock_dir, 'tickets.json')

    if not os.path.exists(tickets_path):
        print(f"❌ Error: {tickets_path} not found!")
        print(f"💡 Troubleshooting: Check if the file is actually named 'tickets.json' (no extra .json or .txt)")
        return

    try:
        with open(tickets_path, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON: {str(e)}")
        return

    print(f"\n🚀 KSOLVES Agentic AI Hackathon 2026")
    print(f"📦 Loaded {len(tickets)} tickets. Starting concurrent processing... [cite: 73]")
    print("-" * 50)
    
    # 2. Concurrent Processing [cite: 73]
    # This meets the 'Tickets must be processed concurrently' requirement [cite: 73]
    tasks = [process_ticket_async(t) for t in tickets]
    results = await asyncio.gather(*tasks)

    # 3. Visual Feedback for Demo Video 
    for res in results:
        # Safety check for keys to prevent crashing during the demo
        final_decision = res.get('final_decision', {})
        final_action = final_decision.get('action', 'unknown')
        ticket_id = res.get('ticket_id', 'Unknown ID')
        
        status_icon = "✅" if final_action == "resolved" else "⚠️"
        print(f"{status_icon} Ticket {ticket_id}: {final_action.upper()}")

    # 4. Save Mandatory Audit Log 
    # Required for the 'Audit Every Decision' standard [cite: 60, 135]
    audit_file = 'audit_log.json'
    with open(audit_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    
    print("-" * 50)
    print(f"🏁 Done! Audit log saved to '{audit_file}'. [cite: 135]")
    print(f"Total tickets processed: {len(results)}")

if __name__ == "__main__":
    asyncio.run(main())