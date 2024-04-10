#Main processes and ideas
# 1.Separate gradients
# 2.Filter
# 3.Condition
# 4.Spanning tree list and printing
# 5.Enter the displayed tree structure
# 6.Display the corresponding tree structure to the page

import TreeUtil
import tkinter as tk

# Define functions to perform initial hierarchical filtering of data
# 23.61#22.41#22.06#19.29#22.02#14.80#9.98
resource = [23.61, 22.41, 22.06, 19.29, 22.02, 14.808, 9.98]

# Example usage:
# lamination(array, maxV, sMap, isSup)
print("Check out the basic data model------------")
TreeUtil.measuringScale(resource)
# print("Start parsingNode")
# TreeUtil.supply_tree_node()

# Create Tkinter window
window = tk.Tk()
window.title("Binary Tree Visualization")
window.geometry("1000x700")

# Function to calculate node coordinates
def calculate_coordinates(node, x, y, width):
    if node is not None:
        # Calculate the coordinates of the current node
        x_coord = x
        y_coord = y

        # draw node
        canvas.create_oval(x_coord - 20, y_coord - 20, x_coord + 20, y_coord + 20, fill="blue")
        canvas.create_text(x_coord, y_coord, text=node.colorStr)
        
        # Calculate the coordinates of child nodes
        if node.left is not None:
            left_x = x - width // 4
            left_y = y + 100
            canvas.create_line(x_coord, y_coord, left_x, left_y, fill="red")
            calculate_coordinates(node.left, left_x, left_y, width // 2)

        if node.right is not None:
            right_x = x + width // 4
            right_y = y + 100
            canvas.create_line(x_coord, y_coord, right_x, right_y, fill="red")
            calculate_coordinates(node.right, right_x, right_y, width // 2)

# Create Canvas for drawing nodes and connecting lines
canvas = tk.Canvas(window, width=1400, height=700)
canvas.pack()

# Adjust the x-coordinate of the root node so that it is in the center of the window
root_x = 500
root_y = 50

# Use the calculate coordinate function to draw a binary tree
print(TreeUtil.getTreeRoots())
roots = TreeUtil.getTreeRoots()
if len(roots) > 0:
    root = roots[0]
    calculate_coordinates(root, root_x, root_y, 500)
# calculate_coordinates(root, root_x, root_y, 500)

# Start Tkinter mainloop
window.mainloop()

