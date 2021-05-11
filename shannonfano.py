from numpy.lib.scimath import log2
import argparse
original_p_dict = {}
shannon_fano_dict = {}
code_dict = {}


parser = argparse.ArgumentParser(description='Shannon-fano coding script',
                                     epilog='Enjoy!')

parser.add_argument('input_file',
                    action='store',
                    type=str,
                    metavar='',
                    help='input file name')
parser.add_argument('output_file',
                    action='store',
                    type=str,
                    metavar='',
                    help='input file name')

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

def make_xi_values(probabilities):
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

    xi_list = xi_values.split()
    count_two = 0
    for i in shannon_fano_dict:
        shannon_fano_dict[i] = float(xi_list[count_two])
        count_two += 1

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


args = parser.parse_args()
file_content = read_from_file(args.input_file)
original_p_dict = take_symbol_to_probality(file_content)
original_p_dict = sort_of_dict_by_value(original_p_dict)
key_list = original_p_dict.keys()
for i in key_list:
    code_dict[i] = ""
    shannon_fano_dict[i] = ""
make_xi_values(original_p_dict)
shannon_fano_coding(key_list,0,1)
length = calculate_length(shannon_fano_dict)
effi = calculate_efficiency(length)

count = 1
output_string = ""
for i in key_list:
    pretty_spaces_one = (7-len(str(original_p_dict[i])))*" "
    pretty_spaces_two = (7-len(str(code_dict[i])))*" "
    output_string += f"x{count}* = {shannon_fano_dict[i]}{pretty_spaces_one}-->" \
                     f"    {code_dict[i]}{pretty_spaces_two}<-- p{count}* =" \
                     f" {original_p_dict[i]} L{count} = {len(code_dict[i])}\n\n"
    count += 1
output_string += f"Expected length: {length}         Efficiency: {effi}\n"


write_to_file(args.output_file, output_string)

print("Shannon-Fano Coding finished successfully")
