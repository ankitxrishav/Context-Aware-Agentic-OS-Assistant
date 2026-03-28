from core.agent import Agent
import json

agent = Agent()
req1 = "make a folder on desktop name 'hammeettttt' and open in vs code"
req2 = "search google for time in indoneaisa"

print("--- REQ 1 ---")
print(json.dumps(agent.get_action(req1), indent=2))

print("--- REQ 2 ---")
print(json.dumps(agent.get_action(req2), indent=2))
