from string import ascii_uppercase
from numpy.lib.scimath import log2
original_p_dict = {}
shannon_fano_dict = {}
code_dict = {}


def read_from_file(file_name: str):
    with open(file_name, encoding='utf-8') as f:
        file_content = f.readline()
    return file_content

def write_to_file(file_name: str, content: str) -> dict:
    with open(file_name, "w") as f:
        content = str(content)
        f.write(content)

def take_symbol_to_probality(probab: list) -> dict:
    probabilities = {}
    probab = probab.split()
    key_count = 1
    for i in range(len(probab)):
        #key = ascii_uppercase[i]
        key = key_count
        value = float(probab[i])
        probabilities[key] = value
        key_count += 1
    return probabilities

def sort_of_dict_by_value(probabilities : dict):
    probabilities = dict(sorted(probabilities.items(), key=lambda item: item[1] , reverse = True))
    return probabilities

def shannon_fano_coding(key_list,interval_min, interval_max):
    difference = None
    above_middle = []
    below_middle = []

    interval_middle = (interval_max-interval_min)/2+interval_min

    for i in key_list:
        if shannon_fano_dict[i] < interval_middle:
            below_middle.append(i)
            code_dict[i] += "0"
        else:
            above_middle.append(i)
            code_dict[i] += "1"


    if len(below_middle) > 1:
        shannon_fano_coding(below_middle,interval_min,interval_middle)
    if len(above_middle) > 1:
        shannon_fano_coding(above_middle,interval_middle, interval_max)

def second_step(probabilities):
    xi_values = ""
    values = []
    count = 2
    temp = 0
    k = 0
    for i in probabilities:
        values.append(probabilities[i])

    xi_values += "0"
    xi_values += " " + str(values[0])
    for i in range(len(values)-2):
        for j in range(count):
            k = values[j]
            temp += k
        xi_values += " "+str(round(temp,2))
        temp = 0
        count += 1

    return xi_values

def calculate_length(p_dict):
    length = 0.0
    for i in p_dict:
        length += original_p_dict[i]*len(code_dict[i])
    return round(length,2)

def calculate_efficiency(length):

    efficiency = 0.0
    for i in original_p_dict:
        efficiency += original_p_dict[i]*log2(original_p_dict[i])
    efficiency = -1*efficiency
    return round(efficiency/length,7)

#probab = take_symbol_to_probality("0.20 0.25  0.12 0.08 0.30 0.05")
#probab = take_symbol_to_probality("0.36 0.18  0.18 0.1 0.09 0.07")
#probab = take_symbol_to_probality("0.09 0.05 0.06 0.18 0.12 0.10 0.28 0.02 0.10")
#probab = take_symbol_to_probality("0.36 0.20 0.10 0.08 0.08 0.08 0.04 0.04 0.02")
#shannon_fano_dict = take_symbol_to_probality("0.28 0.18 0.12 0.10 0.10 0.09 0.06 0.05 0.02")
#probab = take_symbol_to_probality("0.375 0.125 0.2 0.125 0.08 0.125")

file_content = read_from_file("input1.txt")
shannon_fano_dict = take_symbol_to_probality(file_content)
shannon_fano_dict = sort_of_dict_by_value(shannon_fano_dict)
original_p_dict = shannon_fano_dict
key_list = shannon_fano_dict.keys()
for i in key_list:
    code_dict[i] = ""
xi = second_step(shannon_fano_dict)
shannon_fano_dict  = take_symbol_to_probality(xi)
shannon_fano_coding(key_list,0,1)
length = calculate_length(shannon_fano_dict)
effi = calculate_efficiency(length)

count = 1
output_string = ""
for i in key_list:
    pretty_spaces_one = (7-len(str(original_p_dict[i])))*" "
    pretty_spaces_two = (7-len(str(code_dict[i])))*" "
    output_string += f"x{count}* = {original_p_dict[i]}{pretty_spaces_one}-->     {code_dict[i]}{pretty_spaces_two}<-- p{count}* = {shannon_fano_dict[i]} L{len(code_dict[i])} = {count}\n"
    count += 1
write_to_file("output1.txt", output_string)


print(original_p_dict)
print(code_dict)
print(length)
print(effi)
print("Shannon-Fano Coding: ")
