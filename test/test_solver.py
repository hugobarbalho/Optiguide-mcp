import pyomo.environ as pyo

# Create a model
model = pyo.ConcreteModel()

# Define variables
model.x_A = pyo.Var(domain=pyo.NonNegativeIntegers)
model.x_B = pyo.Var(domain=pyo.NonNegativeIntegers)

# Parameters
Labor_A = 2
Labor_B = 1
Material_A = 3
Material_B = 2
Total_Labor = 100
Total_Material = 150
Profit_A = 40
Profit_B = 30

# Objective function
model.Profit = pyo.Objective(
    expr=Profit_A * model.x_A + Profit_B * model.x_B,
    sense=pyo.maximize
)

# Constraints
model.LaborConstraint = pyo.Constraint(
    expr=Labor_A * model.x_A + Labor_B * model.x_B <= Total_Labor
)
model.MaterialConstraint = pyo.Constraint(
    expr=Material_A * model.x_A + Material_B * model.x_B <= Total_Material
)

# Solve the model
solver = pyo.SolverFactory("appsi_highs")
result = solver.solve(model)

# Display the results
print(f"Optimal units of Product A (x_A): {pyo.value(model.x_A)}")
print(f"Optimal units of Product B (x_B): {pyo.value(model.x_B)}")
print(f"Maximum Profit: ${pyo.value(model.Profit)}")