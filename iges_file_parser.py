import re

main_list = {}


def multi_print(message, file, skip_console=False):
    print(message, file=file)
    if skip_console:
        return
    print(message)


def populate_list():
    with open('project/files/iges_file.igs', 'r') as file:
        for line in file:
            line = re.sub(r"\s+", ">", line.strip(), flags=re.UNICODE).split('>')
            line.pop()
            line_data = line[0][:-1].split(',')
            line_group = line[-1:][0]
            line_group_ending = line[-1:][0][-1:]

            if line_group_ending == 'P':
                if line_group in main_list:
                    main_list[line_group]['line_data'].extend(line_data)
                else:
                    main_list.update({line_group: {'line_data': line_data}})


def find_pems():
    links = []
    type_116 = []
    type_406 = []
    pem_data = []

    for line_location in main_list:
        if '116' in main_list[line_location]['line_data'][0]:
            type_116.append(line_location)
        elif '406' in main_list[line_location]['line_data'][0]:
            type_406.append(line_location)
        elif '402' in main_list[line_location]['line_data'][0]:
            links.append(line_location)

    for link_location in links:
        coordinates = ""
        name = ""

        if any(location in main_list[link_location]['line_data'][1:] for location in [x[:-1] for x in type_116]) \
                and any(location in main_list[link_location]['line_data'][1:] for location in [x[:-1] for x in type_406]):
            for coordinates_location in type_116:
                for linked_location in main_list[link_location]['line_data'][1:]:
                    if coordinates_location[:-1] == linked_location:
                        coordinates_regex = r"(.*D.*)"
                        coordinates = [re.search(coordinates_regex, x).group(1) for x in main_list[coordinates_location]['line_data'][1:][:-4]]
                        coordinates = [float(x.replace('D', 'E')) for x in coordinates]

            for lists_location in type_406:
                for linked_location in main_list[link_location]['line_data'][1:]:
                    if lists_location[:-1] == linked_location:
                        name_text = main_list[lists_location]['line_data'].pop()
                        name_regex = r"H(.*)_|H(.*)"
                        name = re.search(name_regex, name_text).group(1)
                        if name is None:
                            name = re.search(name_regex, name_text).group(2)

            pem_data.append({'name': name, 'coordinates': coordinates})

    with open('project/files/parsed_iges_output.csv', 'w') as file:
        for data in pem_data:
            multi_print(f"{data['name']},,,,,,,", file=file)
            multi_print(f",{data['coordinates'][0]},{data['coordinates'][1]},{data['coordinates'][2]},,,,", file=file)


def run():
    populate_list()
    find_pems()


run()
