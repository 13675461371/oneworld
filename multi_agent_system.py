"""
Simplified Multi-Agent System for Enterprise Knowledge & Workflow Automation
- Coordinator Agent
- Knowledge Agent
- Task Agent
- Tool Execution Layer

This is a minimal but complete runnable example.
"""

from typing import List, Dict, Any
import queue
import threading

# ---------------------- Base Agent ----------------------
class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def handle(self, message: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

# ---------------------- Knowledge Agent ----------------------
class KnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__("KnowledgeAgent")
        self.knowledge_base = {
            "leave_policy": "Employees are entitled to 15 days of paid leave.",
            "expense_policy": "Expenses must be approved by managers."
        }

    def handle(self, message):
        query = message.get("query", "")
        for k, v in self.knowledge_base.items():
            if k in query:
                return {"agent": self.name, "result": v}
        return {"agent": self.name, "result": "No relevant knowledge found."}

# ---------------------- Task Agent ----------------------
class TaskAgent(BaseAgent):
    def __init__(self):
        super().__init__("TaskAgent")

    def handle(self, message):
        task = message.get("task")
        if task == "submit_expense":
            return {"agent": self.name, "result": "Expense submitted successfully."}
        return {"agent": self.name, "result": "Unknown task."}

# ---------------------- Tool Layer ----------------------
class ToolExecutor:
    def execute(self, action: str, params: Dict[str, Any]):
        if action == "log":
            print(f"[LOG]: {params}")
        return {"status": "done"}

# ---------------------- Coordinator ----------------------
class Coordinator:
    def __init__(self):
        self.agents = {
            "knowledge": KnowledgeAgent(),
            "task": TaskAgent()
        }
        self.tool_executor = ToolExecutor()

    def route(self, user_input: str):
        if "policy" in user_input:
            return self.agents["knowledge"].handle({"query": user_input})
        elif "expense" in user_input:
            return self.agents["task"].handle({"task": "submit_expense"})
        else:
            return {"result": "Cannot determine intent."}

# ---------------------- Multi-Agent Runtime ----------------------
class MultiAgentSystem:
    def __init__(self):
        self.coordinator = Coordinator()
        self.message_queue = queue.Queue()

    def submit(self, user_input: str):
        self.message_queue.put(user_input)

    def run(self):
        while not self.message_queue.empty():
            msg = self.message_queue.get()
            response = self.coordinator.route(msg)
            print(f"Response: {response}")

# ---------------------- Demo ----------------------
if __name__ == "__main__":
    system = MultiAgentSystem()
    system.submit("What is the leave_policy?")
    system.submit("Submit my expense")
    system.run()
