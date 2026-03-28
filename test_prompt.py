from core.agent import Agent
import json

agent = Agent()
req1 = "open whatapp and text her 'hi'"
req2 = "open telegram and send 'xyz' a message saying hello"

print("--- REQ 1 ---")
print(json.dumps(agent.get_action(req1), indent=2))

print("--- REQ 2 ---")
print(json.dumps(agent.get_action(req2), indent=2))
