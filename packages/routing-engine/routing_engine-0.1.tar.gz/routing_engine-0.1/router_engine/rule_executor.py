from .rule_evaluator import evaluate_condition
import actions.greetings as greetings

class ExecutionFailed(Exception):
    pass

def get_function_by_name(name,actions):
    return actions.get(name, None)

def execute_action(action_name,actions):
    function = get_function_by_name(action_name,actions)
    if not function:
        raise ExecutionFailed(f"Action {action_name} not found")
    
    try:
        function()
    except Exception as e:
        raise ExecutionFailed(f"Failed to execute action {action_name}: {str(e)}")



