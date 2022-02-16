from pulp import *

count = 0
# array[x] will be the cost to buy x bottles of "coca cola".
array = []

while count <= 200:
    array += [count*10]
    count += 1
while count <= 400:
    array += [(10 * 200) + ((count-200) * 8)]
    count += 1
while count <= 600:
    array += [(10 * 200) + (8 * 200) + ((count-400) * 7)]
    count += 1

COLA_MIX = [1,2]  # 1 is mix-1 and 2 is mix-2.
COLA = [1,2]  # 1 is "coca cola" and 2 is "pepsi".
zset = [1,2,3,4]
yset = [1,2,3]

prob = LpProblem("Piecewise", LpMaximize)

# amount_vars = x
amount_vars = LpVariable("amount", 0, None, LpInteger)
# [(1,1), (1,2), (2,1), (2,2)]
cola_vars = LpVariable.dicts("cola-X-mixed", [(i,j) for i in COLA for j in COLA_MIX], 0, None, LpInteger)
z_vars = LpVariable.dicts("zset", zset, 0)
y_vars = LpVariable.dicts("yset", yset, 0, 1, LpBinary)

prob += lpSum(7 * cola_vars[(i,1)] for i in COLA) + lpSum(9 * cola_vars[(i,2)] for i in COLA) - (z_vars[1]*array[0]) - (z_vars[2]*array[200]) - (z_vars[3]*array[400]) - (z_vars[4]*array[600])
# x = 0z_1 + 200z_2 + 400z_3 + 600z_4
prob += amount_vars == (0*z_vars[1]) + (200*z_vars[2]) + (400*z_vars[3]) + (600*z_vars[4])
# x_11 + x_12 <= x + 200
# prob += lpSum(pizza_vars[(1,j)] for j in PIZZA) <= amount_vars + 300
prob += lpSum(cola_vars[(1,j)] for j in COLA_MIX) - amount_vars <= 300  # במקום השורה למעלה שבהערה נרשום בצורה הזאת (כלומר לאחר העברת אגפים כי זאת הצורה המתאימה להנחות של סימפלקס)
# x_21 + x_22 <= 400
prob += lpSum(cola_vars[(2,j)] for j in COLA_MIX) <= 450
# x_11 / (x_11 + x_21) >= 0.5  ||  0.5x_11 - 0.5x_21 >= 0
prob += ((0.5 * cola_vars[(1,1)]) - (0.5 * cola_vars[2,1])) >= 0
# x_12 / (x_12 + x_22) >= 0.75  ||  0.25x_12 - 0.75x_22 >= 0
prob += ((0.25 * cola_vars[(1,2)]) - (0.75 * cola_vars[2,2])) >= 0
# y_1 + y_2 + y_3 = 1
prob += lpSum(y_vars[k] for k in yset) == 1
# z_1 + z_2 + z_3 + z_4 = 1
prob += lpSum(z_vars[k] for k in zset) == 1
# if y_1 = 1 -> z_1 + z_2 = 1 && z_3 == z_4 == 0
# if y_2 = 1 -> z_2 + z_3 = 1 && z_1 == z_4 == 0
# if y_3 = 1 -> z_3 + z_4 = 1 && z_1 == z_2 == 0
prob += z_vars[1] <= y_vars[1]
prob += z_vars[2] <= y_vars[1] + y_vars[2]
prob += z_vars[3] <= y_vars[2] + y_vars[3]
prob += z_vars[4] <= y_vars[3]

prob.solve()
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total profit:", value(prob.objective))
