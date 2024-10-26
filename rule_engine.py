class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # 'operator' or 'operand'
        self.left = left            # left child (for operators)
        self.right = right          # right child (for operators)
        self.value = value          # operand value (e.g., age, department)

# Function to create a rule (returns an AST)
def create_rule(rule_string):
    # For simplicity, we will hardcode the rule creation here
    if rule_string == "rule1":
        # (age > 30 AND department = 'Sales') OR (salary > 50000 OR experience > 5)
        return Node(
            "operator", 
            left=Node("operator", 
                      left=Node("operand", value=("age", ">", 30)),
                      right=Node("operand", value=("department", "=", "Sales"))
                     ),
            right=Node("operator",
                       left=Node("operand", value=("salary", ">", 50000)),
                       right=Node("operand", value=("experience", ">", 5))
                      )
        )
    # Add more rules as needed
    return None

# Function to combine multiple rules (returns the root of combined AST)
def combine_rules(rules):
    if len(rules) == 0:
        return None
    root = create_rule(rules[0])
    for rule in rules[1:]:
        new_rule_ast = create_rule(rule)
        root = Node("operator", left=root, right=new_rule_ast)  # Combine with AND
    return root

# Function to evaluate a rule's AST with input data
def evaluate_rule(ast, data):
    if ast.node_type == "operand":
        attr, op, val = ast.value
        if op == ">":
            return data.get(attr, 0) > val
        elif op == "<":
            return data.get(attr, 0) < val
        elif op == "=":
            return data.get(attr, None) == val
    elif ast.node_type == "operator":
        # Adding OR logic. We assume that the operator's default is AND, unless explicitly handled as OR.
        # Here, left is evaluated and OR logic is introduced in right.
        return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
    return False

# Example usage:

# Create and evaluate rules
rule1_ast = create_rule("rule1")
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

print("Input Data:", data)

# Evaluating the rule on the given data
result = evaluate_rule(rule1_ast, data)
print("Evaluation Result:", result)  # Should return True based on the rule and input data
