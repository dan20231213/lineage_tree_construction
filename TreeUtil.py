from itertools import permutations
from copy import deepcopy
import copy

class TreeNode:
    def __init__(self):
        # self.value = value 
        self.neureTone = None
        self.depthTone = None
        # 0:Red, 1: Green, 2: Yellow, 3: Blue, 4: Green/Blue, 5: Yellow/Blue
        self.colorType = None
        self.colorStr = None
        self.isSup = None
        self.left = None
        self.right = None
        self.nodeId = None
        self.type = None #0: neuron, 1: progenitor
        

class TreeClass:
    static_variable = 10 
    firstK = ""
    sources = []
    roots = []

def getTreeRoots():
    return TreeClass.roots

def measuringScale(array):
    TreeClass.sources = array
    maxV = max(array)
    sMap = {}
    laminationNomal(array,maxV,sMap,False)
    # print(sMap)
    print("Start parsing Node")
    supply_tree_node(sMap) 

def supply_tree_node(dict):
    supply_dict = {}
    float_keys = [key for key in dict.keys() if key.replace('.', '', 1).isdigit()]
    sorted_float_keys = sorted(float_keys, key=lambda x: float(x))
    print(sorted_float_keys)
    add_nodes = []
    for n in range(len(sorted_float_keys)):
        current_key = sorted_float_keys[n]
        child_dic = dict[current_key]
        child_array = deepcopy(child_dic.get("cells", []))
        for node in add_nodes:
            node.depthTone = current_key
        cells = deal_need_permutation(child_array, add_nodes)
        if not cells:
            return
        if isinstance(cells, list):
            print("my_dict is a array")
            add_nodes.clear()
            cellNodes = cells
            if len(cellNodes):
                oldNode = cellNodes[0]
                rightNode = oldNode.right
                leftNode = oldNode.left
                if len(cellNodes) == 1 and rightNode is None and leftNode is None:
                    break
                if leftNode != None and leftNode.type == 1:
                    break
                replenish_node(deepcopy(cellNodes),add_nodes,current_key)
                supply_dict[current_key] = deepcopy(child_array)
        else:
            print("Start recursive operation!")
            on_kinds_of_more_tree(deepcopy(sorted_float_keys),n,deepcopy(cells),dict)
            print("End recursive operation!")
            print(TreeClass.roots)
            return

def on_kinds_of_more_tree(new_full_array, start, node_dict, origin_dict):
    ckeys = node_dict.keys()
    add_nodes = []

    for key in ckeys:
        cell_nodes = deepcopy(node_dict[key])
        start = new_full_array.index(cell_nodes[0].depthTone)
        print(f"xx: {start}")

        for n in range(start, len(new_full_array)):
            current_key = new_full_array[n]
            print(f"{n}-{len(new_full_array)}")
            print(f"keys: {current_key}")
            if cell_nodes != None:
                add_nodes.clear()
                old_node = cell_nodes[0]
                rightNode = old_node.right
                leftNode = old_node.left
                if leftNode != None and leftNode.type == 1:
                    if len(cell_nodes) == 1 and rightNode is None:
                        break
                
               
                replenish_node(deepcopy(cell_nodes), add_nodes, current_key)
                cell_nodes = None
                continue

            child_dict = origin_dict[current_key]
            child_array = deepcopy(child_dict["cells"])
            
            # Test permutations
            for node in add_nodes:
                node.depthTone = current_key

            # End condition
            if not (cell_nodes or child_array or add_nodes):
                print("Exceptional end...")
            
            cells = deal_need_permutation(child_array, add_nodes)
            if not cells:
                break

            if isinstance(cells, dict):
                add_nodes.clear()
                cell_dicts = cells
                on_kinds_of_more_tree(new_full_array[:], n, deepcopy(cell_dicts), origin_dict)
            else:
                add_nodes.clear()
                new_cell_nodes = cells
                if new_cell_nodes:
                    old_node = new_cell_nodes[0]
                    if len(new_cell_nodes) == 1 and old_node.right is None and old_node.left.type==1:
                        list_data = preorder_traversal(old_node.left)
                        if len(list_data) == len(TreeClass.sources):
                            TreeClass.roots.append(old_node.left)
                        else:
                            print("Abnormal number of deduced nodes")
                        break

                    replenish_node(deepcopy(new_cell_nodes), add_nodes, current_key)

def deal_need_permutation(red_array, colors):
    red_array.extend(colors)
    if not red_array:
        return None
 
    is_same = all(node.colorType == red_array[0].colorType for node in red_array)

    # Perform your checks and color assignments here
    filtered_array = [item for item in colors if item.colorType == 3]
    if len(filtered_array) > 2:
        print("The number of blues exceeds the limit...cannot continue")
        return None
    elif len(filtered_array) == 2:
        if (len(colors) + len(red_array)) > 4:
            print("Contains two blue colors, then the coaxial has at most two other colors")
            return None
   
    for tnode in filtered_array:
        if tnode.left is None or tnode.right is None:
            break
        if tnode.left.colorType == 3 and tnode.right.colorType == 3 and len(red_array) > 1:
            return None
        
    if len(colors) > 2:
        nums = 2 - len(filtered_array)
        filteredArray2 = [item for item in colors if item.colorType == 4]
        if len(filteredArray2) > nums:
            for i in range(len(filteredArray2) - nums):
                node = filteredArray2[i]
                node.colorType = 1
                node.colorStr = get_char_for_type(1)
    
    if len(red_array) == 2:
        strM = ""
        index = -1
        for i, node in enumerate(red_array):
            if i:
                strM += "." + get_char_for_type(node.colorType)
            else:
                strM += get_char_for_type(node.colorType)
            if node.colorType == 4:
                index = i

        match = get_change_matching_list()
        if strM in match:
            node = red_array[index]
            node.colorType = 3
            node.colorStr = get_char_for_type(3)

    if is_same:
        return deepcopy(red_array)
    else:
        cells = combinations(red_array)
        return cells

def combinations(red_array):
    if len(red_array) < 3:
        return deepcopy(red_array)
    
    permutations_result = list(permutations(red_array))

    def deduplicate(permutations_result):
        seen = set()
        deduplicated = []
        for perm in permutations_result:
            colors = [node.colorType for node in perm]
            colors_tuple = tuple(colors)
            if colors_tuple not in seen:
                seen.add(colors_tuple)
                deduplicated.append(perm)
        return deduplicated

    deduplicated_result = deduplicate(permutations_result)
    temp_set = set()
    temp_list = []
    temp_dict = {}
    for perm in deduplicated_result:
        # print([node.colorType for node in perm])
        # property_values = [node.colorStr for node in perm]
        # print(property_values)  
        split_arrays = [perm[i:i+2] for i in range(0, len(perm), 2)]
        # split_arrays_str = [tuple(property_values[i:i+2]) for i in range(0, len(property_values), 2)]

        temp_strs = []
        for nNodes in split_arrays:
            if len(nNodes) == 1:
                temp_strs.append(str(nNodes[0].colorStr))
            else:
                leftNode = nNodes[0]
                rightNode = nNodes[1]
                temp_strs.append(str(leftNode.colorStr+"."+rightNode.colorStr))
        keyStr = ".".join(temp_strs)
        print(keyStr)
        set1 = set(temp_strs)
        set2 = set(get_mismatching_list())
        if set1.intersection(set2):
            print("Include assignments that do not comply with rules, exclude")
            break

        temp_dict[keyStr] = perm
        temp_list.append(temp_strs)
        # print(split_arrays)
        # temp_set.add(tuple(split_arrays_str))
    # unique_arrays = set(map(tuple, map(sorted, temp_list)))
    print("222222:")
    print(temp_dict)
    first_dict = standard_Screening(temp_list,temp_dict,True)
    print("111111:")
    print(temp_list)
    print(first_dict)

    return first_dict


def laminationNomal(array, maxV, sMap, isSup):
    superArray = []
    otherArray = []
    for idx in range(len(array)):
        obj = array[idx]
        maxNum = maxV
        halfNum = maxV / 2.0
        scopeArray = queryScope([maxNum, halfNum], obj)
        if len(scopeArray) == 1:
            key = str(scopeArray[0])
            if key == str(maxNum):
                superArray.append(obj)
            else:
                otherArray.append(obj)
        else:
            print("Data may vary：", obj)
        if idx == len(array) - 1:
            if len(superArray) > 0:
                currentK = sum(superArray) / len(superArray)
                halfNum = currentK / 2.0
                cks = f"{currentK:.2f}"
                nodes = []
                for dat in superArray:
                    node = TreeNode()
                    node.neureTone = dat
                    node.depthTone = cks
                    node.colorType = 0
                    node.colorStr = get_char_for_type(0)
                    node.isSup = False
                    nodes.append(node)
                dict = {
                    "cells": nodes,
                    "sacles": superArray,
                    "SCALE": cks
                }
                if len(TreeClass.firstK) == 0:
                    TreeClass.firstK = cks
            else:
                dict = {
                    "cells": [],
                    "sacles": [],
                    "SCALE": str(maxNum)
                }
            sMap[dict["SCALE"]] = dict

            if otherArray:
                laminationNomal(otherArray, halfNum, sMap, False)
            else:
                for i in range(1, 6):
                    ikl = 2 ** i * float(TreeClass.firstK)
                    iklStr = f"{ikl:.2f}"
                    dict_b = {
                        "cells": [],
                        "sacles": [],
                        "SCALE": iklStr
                    }
                    sMap[dict_b["SCALE"]] = dict_b
                TreeClass.firstK = ""

def queryScope(numbers_array, target_number):
    closest_numbers = []
    closest_difference = float('inf')

    for number in numbers_array:
        difference = abs(target_number - number)
        if difference < closest_difference:
            closest_difference = difference
            closest_numbers = [number]
        elif difference == closest_difference:
            closest_numbers.append(number)

    return closest_numbers

def orderValueArrayWithDictionary(dictionary):
    orderValueArray = []

    # Get all keys from the dictionary
    keyArray = list(dictionary.keys())

    # Sort the keys
    sortedArray = sorted(keyArray, key=lambda x: (int(x) if x.isdigit() else x))

    # Extract values based on the sorted keys
    for key in sortedArray:
        orderValueArray.append(dictionary[key])

    return orderValueArray

def get_mismatching_list():
     return [
        "G.R",
        "R.G", 
        "Y.R",
        "R.Y",
        "Y.G",
        "G.Y",
        "Y.Y"
    ]

def get_change_matching_list():
    return [
        "R.P",
        "P.R",
        "Y.P",
        "P.Y"
    ]

def get_change_matching_yb_list():
    return [
        "O.Y",
        "Y.O",
        "O.R",
        "R.O",
        "O.G",
        "G.O"
    ]

def get_char_for_type(type):
    info = ""
    if type == 0:
        info = "R"
    elif type == 1:
        info = "G"
    elif type == 2:
        info = "Y"
    elif type == 3:
        info = "B"
    elif type == 4:
        info = "P"
    elif type == 5:
        info = "O"
    return info

def current_standard_str(current_str):
    if current_str in ["R.B", "B.R", "R.P", "P.R", "O.R", "R.O"]:
        return "R.B"
    elif current_str in ["G.B", "B.G", "O.G", "G.O"]:
        return "G.B"
    elif current_str in ["G.P", "P.G"]:
        return "G.P"
    elif current_str in ["Y.B", "B.Y", "Y.P", "P.Y", "Y.O", "O.Y"]:
        return "Y.B"
    elif current_str in ["B.P", "P.B"]:
        return "B.P"
    elif current_str in ["O.P", "P.O"]:
        return "O.P"
    else:
        return current_str
    
def standard_Screening(unique_arrays, temp_dict, isTransform):
    temp_first = []
    first_dict = {}
    for info in unique_arrays:
        temp_low = []
        old_keyStr = ".".join(info)
        print(old_keyStr)
        first_nodes = temp_dict[old_keyStr]
        new_sources = list(first_nodes)
        # for stand in info:
        #    temp_low.append(current_standard_str(stand))
        for index in range(len(info)):
            frontStr = info[index]
            endStr = current_standard_str(frontStr)
            temp_low.append(endStr)
            # if frontStr != endStr:
            #     oneIndex = index*2
            #     nextIndex = oneIndex + 1
            #     node1 = first_nodes
            if isTransform:
                
                new_sources = improve_current_node(frontStr,new_sources,index)

        temp_first.append(temp_low)
        new_keyStr = ".".join(temp_low)
        if new_keyStr not in first_dict:
            for xnode in new_sources:
                print(xnode.colorStr)
            first_dict[new_keyStr] = new_sources
            

    unique_arrays = set(map(tuple, map(sorted, temp_first)))
    print(first_dict)
    return first_dict


def replenish_node(child_array, add_nodes, depth_tone):
    present_node = None
    for i, current_node in enumerate(child_array):
        if current_node.nodeId == None:
            current_node.nodeId = str(int(float(current_node.depthTone) * 1000000 + i))

        if not current_node.type:
            current_node.code = "1"
        else:
            # currentNode.depthTone = depthTone
            pass
        if (i + 1) % 2:  # Create parent node for odd indices
            present_node = add_present_node_with_child(current_node, i)
            add_nodes.append(present_node)
            present_node.code = f"{current_node.code}2"
            present_node.colorType = 3
            present_node.colorStr = get_char_for_type(3)
            present_node.left = current_node
            current_node.parentNodeId = present_node.nodeId
        else:
            present_node.code = f"{present_node.code}{current_node.code}"
            present_node.right = current_node
            # Handle colorType assignments
            if current_node.colorType == 0 and present_node.left.colorType == 0:
                present_node.colorType = 4
                present_node.colorStr = get_char_for_type(4)
            elif current_node.colorType == 1 and present_node.left.colorType == 1:
                #G.P and P.G = Y
                present_node.colorType = 2
                present_node.colorStr = get_char_for_type(2)
            elif current_node.colorType == 4 and present_node.left.colorType == 4:
                #G.G and G.G = O（Yellow/Blue）
                present_node.colorType = 5
                present_node.colorStr = get_char_for_type(5)
            elif current_node.colorType == 1 and present_node.left.colorType == 4 | current_node.colorType == 4 and present_node.left.colorType == 1:
                #G.G and G.G = O（Yellow/Blue）
                present_node.colorType = 5
                present_node.colorStr = get_char_for_type(5)
            else:
                present_node.colorType = 3
                present_node.colorStr = get_char_for_type(3)
            # Handle other colorType assignments
            current_node.parentNodeId = present_node.nodeId
            present_node = None
                    
def improve_current_node(current_name, sources, index):
    resources = sources
    #1.B.P
    if current_name == "P.B":
         oneIndex = index*2
         nextIndex = oneIndex + 1
         pNode = resources[oneIndex]
         bNode = resources[nextIndex]
         if bNode.left.colorType==3 or bNode.right.colorType==3:
            # p_node = pNode.copy()
            p_node = copy.deepcopy(pNode)
            p_node.colorType = 1
            p_node.colorStr = get_char_for_type(1)
            resources[oneIndex] = p_node

    if current_name == "B.P":
         oneIndex = index*2
         nextIndex = oneIndex + 1
         bNode = resources[oneIndex]
         pNode = resources[nextIndex]
         if bNode.left.colorType==3 or bNode.right.colorType==3:
            p_node = copy.deepcopy(pNode)
            p_node.colorType = 1
            p_node.colorStr = get_char_for_type(1)
            resources[oneIndex] = p_node

    match = get_change_matching_list()
    if current_name in match:
        pIndex = 0
        result = current_name.endswith('P')
        if result:
            pIndex = 1
        realIndex = index * 2 + pIndex
        node = resources[realIndex]
        n_node = copy.deepcopy(node)
        n_node.colorType = 3
        n_node.colorStr = get_char_for_type(3)
        resources[realIndex] = n_node
    
    oMatch = get_change_matching_yb_list()
    if current_name in oMatch:
        oIndex = 0
        if current_name.endswith('O'):
            oIndex = 1
        realIndex = index * 2 + oIndex
        node = resources[realIndex]
        n_node = copy.deepcopy(node)
        n_node.colorType = 3
        n_node.colorStr = get_char_for_type(3)
        resources[realIndex] = n_node

    return resources


def preorder_traversal(node):
    res = []
    stack = []

    while node is not None or stack:
        if node is not None:
            if  node.colorType == 0:
                res.append(node.depthTone)
            stack.append(node)
            node = node.left
        else:
            last_node = stack.pop()
            node = last_node.right

    return res

def add_present_node_with_child(child_node, i):
    ppid = str(int(float(child_node.depthTone) * 2000000) + i)
    present_node = TreeNode()
    present_node.type = 1
    present_node.nodeId = ppid
    return present_node