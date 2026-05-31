import math

class Coefficients():
    #check out PARTS_VECTORS and CONNECTION_PARTS in image_data to know/change exact order/sequence
    #          for parts: 
    # shoulders, hips, torso left, torso right, left forearm, left arm, right forearm, right arm, left thigh, left calve, right thigh, right calve
    #         for connections: 
    #shoulder and right forearm, shoulder and left forearm, hips and right leg, hips and left leg, sholder and right torso part, sholder and left torso part, right hand and right forearm, left hand and left forearm, right thigh and right calve, left thigh and left calve 
    # DEFAULT = {
    #     "kn_parts" : [0.8, 0.3, 0.5, 0.5, 0, 0, 0, 0, 0.5, 0, 0.5, 0],
    #     "kn_connections" : [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0],
    #     "secondary_kn_parts" : [0, 0, 0, 0, 0.5, 0, 0.5, 0, 0, 0, 0, 0],
    #     "secondary_kn_connections": [0.5, 0.5, 0, 0, 0, 0, 0.5, 0.5, 0, 0]
    # }
    DEFAULT = {
        "kn_parts" : [0.6, 0.3, 0.3, 0.3, 0.1, 0, 0.1, 0, 0.5, 0, 0.5, 0],
        "kn_connections" : [0, 0, 0, 0, 0, 0, 0, 0, 0.6, 0.6],
        "secondary_kn_parts" : [0, 0, 0, 0, 0, 0.1, 0, 0.1, 0, 0.6, 0, 0.6],
        "secondary_kn_connections": [0.1, 0.1, 0.5, 0.5, 0.3, 0.3, 0.1, 0.1, 0, 0]
    }

    HANDS = {
        "kn_parts" : [0.3, 0, 0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0],
        "kn_connections" : [0.5, 0.5, 0, 0, 0, 0, 0.5, 0.5, 0, 0],
        "secondary_kn_parts" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "secondary_kn_connections": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }

    # LEGS = {
    #     "kn_parts" : [0, 0.3, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5],
    #     "kn_connections" : [0, 0, 0.5, 0.5, 0, 0, 0, 0, 0.5, 0.5],
    #     "secondary_kn_parts" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     "secondary_kn_connections": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # }

    LEGS = {
        "kn_parts" : [0, 0.3, 0, 0, 0, 0, 0, 0, 0.6, 0.5, 0.6, 0.5],
        "kn_connections" : [0, 0, 0.5, 0.5, 0, 0, 0, 0, 0.6, 0.6],
        "secondary_kn_parts" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "secondary_kn_connections": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }

    HEAVY = {
        "kn_parts" : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "kn_connections" : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "secondary_kn_parts" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "secondary_kn_connections": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }


# def __compare_angles(angle1, angle2):
#     #if angle/s is/are missing => one or both parts are missing => cannot compare
#     if angle1 == 0 or angle2 == 0:
#         return 0

#     diff = abs(angle1 - angle2)
#     if diff > math.pi:
#         diff = 2 * math.pi - diff

#     # as idea diff**2 
#     return diff


def __compare_angles(angle1, angle2):
    #if angle/s is/are missing => one or both parts are missing => cannot compare
    if angle1 == 0 or angle2 == 0:
        return 0

    diff = abs(angle1 - angle2)
    if diff > math.pi:
        diff = 2 * math.pi - diff

    # as idea diff**2 
    return diff



def __compare_images(image1, image2, coefficients = Coefficients.DEFAULT):
    # factor = 0
    factor_parts = 0
    #k for parts: shoulders, hips, torso left, torso right, left forearm, left arm, right forearm, right arm, left thigh, left calve, right thigh, right calve
    #            sh, h, tl, tr, lf, la, rf, ra, lt, lc, rt, rc
    # default: shoulders: how straight, back or front; hips; torso sides: body upwards or sideways; legs thigh: standing, lying, sitting
    # kn_parts = [0.8, 0.3, 0.5, 0.5, 0, 0, 0, 0, 0.5, 0, 0.5, 0]
    kn_parts = coefficients["kn_parts"]
    kn_parts_sum = 0
    # kn_parts = [2, 1]
    # secondary_kn_parts = [0, 0, 0, 0, 0.5, 0, 0.5, 0, 0, 0, 0, 0]
    secondary_kn_parts = coefficients["secondary_kn_parts"]
    secondary_kn_parts_sum = 0
    secondary_factor_parts = 0
    for part in range(len(kn_parts)):
        factor_parts += kn_parts[part]*__compare_angles(image1.parts_angles[part], image2.parts_angles[part])
        kn_parts_sum += kn_parts[part]
        secondary_factor_parts += secondary_kn_parts[part]*__compare_angles(image1.parts_angles[part], image2.parts_angles[part])
        secondary_kn_parts_sum += secondary_kn_parts[part]
    if kn_parts_sum != 0:
        factor_parts = factor_parts / kn_parts_sum
    if secondary_kn_parts_sum != 0:
        factor_parts = secondary_factor_parts / secondary_kn_parts_sum

    factor_connections = 0
    #k for connections: 
    # default: hips-leg connection; shoulder-torso: bending forward body or straight
    # kn_connections = [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0]
    kn_connections = coefficients["kn_connections"]
    kn_connections_sum = 0
    # secondary_kn_connections = [0.5, 0.5, 0, 0, 0, 0, 0.5, 0.5, 0, 0]
    secondary_kn_connections = coefficients["secondary_kn_connections"]
    secondary_kn_connections_sum = 0
    secondary_factor_connections = 0
    for connection in range(len(kn_connections)):
        factor_connections += kn_connections[connection]*__compare_angles(image1.connection_angles[connection], image2.connection_angles[connection])
        kn_connections_sum += kn_connections[connection]
        secondary_factor_connections += secondary_kn_connections[connection]*__compare_angles(image1.connection_angles[connection], image2.connection_angles[connection])
        secondary_kn_connections_sum += secondary_kn_connections[connection]
    
    if kn_connections_sum != 0:
        factor_connections = factor_connections / kn_connections_sum
    if secondary_kn_connections_sum != 0:
        secondary_factor_connections = secondary_factor_connections / secondary_kn_connections_sum

    # factor = 2*factor_parts + factor_connections
    factor = 0.6*(factor_parts + factor_connections) + 0.4*(secondary_factor_parts + secondary_factor_connections)

    return factor


def sort_images(sketch, images, coefficients = Coefficients.DEFAULT):
    sorted_images = images
    key = lambda image: __compare_images(sketch, image, coefficients)
    filtered_for_sort = sorted_images
    # key_filter = lambda image: filter_first(sketch, image)
    # threshold = (0.8*(math.pi/3) + 0.3*(math.pi/3) + 0.5*(math.pi/3) + 0.5*(math.pi/3) + 0.5*(math.pi/3)+0.5*(math.pi/3))/3.1
    # filtered_for_sort = sorted((obj for obj in sorted_images if key_filter(obj) < threshold), key = key_filter)
    # sorted_images.sort(reverse=True, key=key)
    filtered_for_sort.sort(key=key)
    print("Top sorted keys:")
    for img in filtered_for_sort[0:10]:
        print(key(img))

    return filtered_for_sort




# def filter_first(sketch, image):
#     factor_parts = 0
#     kn_parts = Coefficients.DEFAULT["kn_parts"]
#     kn_parts_sum = 0
#     for part in range(len(kn_parts)):
#         factor_parts += kn_parts[part]*__compare_angles(sketch.parts_angles[part], image.parts_angles[part])
#         kn_parts_sum += kn_parts[part]
#     factor_parts = factor_parts / kn_parts_sum
#     return factor_parts

def get_coefficients(options):
        main_option = options["main_option"]
        match main_option:
                case "DEFAULT":
                    return Coefficients.DEFAULT
                case "HANDS":
                    return Coefficients.HANDS
                case "LEGS":
                    return Coefficients.LEGS
                case "HEAVY":
                    return Coefficients.HEAVY
                case "CUSTOM":
                    options_dict = options["custom_options"]
                    coefficients = calculate_coefficitents(options_dict)
                    return coefficients
                case _:
                    print(f"STRANGE OPTION VARIANT: {main_option.get()}")
                    return None


def calculate_coefficitents(options_dict):
    coefficients = {
        "kn_parts" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "kn_connections" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "secondary_kn_parts" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "secondary_kn_connections": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }

    important_parts = []
    add = lambda list1, list2: [x + y for x, y in zip(list1, list2)]

    #add coefficients if part is chosen primary or secondary
    for part in options_dict.keys():
        match part:
                case 'hand_right':
                    hand_r_parts = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
                    hand_r_connections = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
                    if options_dict[part] == 'primary':
                        important_parts.append(part)
                        # coefficients["kn_parts"][6] += 1
                        # coefficients["kn_parts"][7] += 1
                        # coefficients["kn_connections"][6] += 1
                        coefficients["kn_parts"] = add(hand_r_parts, coefficients["kn_parts"])
                        coefficients["kn_connections"] = add(hand_r_connections, coefficients["kn_connections"])
                    if options_dict[part] == 'secondary':
                        important_parts.append(part)
                        # coefficients["secondary_kn_parts"][6] += 1
                        # coefficients["secondary_kn_parts"][7] += 1
                        # coefficients["secondary_kn_connections"][6] += 1
                        coefficients["secondary_kn_parts"] = add(hand_r_parts, coefficients["secondary_kn_parts"])
                        coefficients["secondary_kn_connections"] = add(hand_r_connections, coefficients["secondary_kn_connections"])
                case 'hand_left':
                    hand_l_parts = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
                    hand_l_connections = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                    if options_dict[part] == 'primary':
                        important_parts.append(part)
                        coefficients["kn_parts"] = add(hand_l_parts, coefficients["kn_parts"])
                        coefficients["kn_connections"] = add(hand_l_connections, coefficients["kn_connections"])
                    if options_dict[part] == 'secondary':
                        important_parts.append(part)
                        coefficients["secondary_kn_parts"] = add(hand_l_parts, coefficients["secondary_kn_parts"])
                        coefficients["secondary_kn_connections"] = add(hand_l_connections, coefficients["secondary_kn_connections"])
                case 'leg_right':
                    leg_r_parts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
                    leg_r_connections = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
                    if options_dict[part] == 'primary':
                        important_parts.append(part)
                        coefficients["kn_parts"] = add(leg_r_parts, coefficients["kn_parts"])
                        coefficients["kn_connections"] = add(leg_r_connections, coefficients["kn_connections"])
                    if options_dict[part] == 'secondary':
                        important_parts.append(part)
                        coefficients["secondary_kn_parts"] = add(leg_r_parts, coefficients["secondary_kn_parts"])
                        coefficients["secondary_kn_connections"] = add(leg_r_connections, coefficients["secondary_kn_connections"])
                case 'leg_left':
                    leg_l_parts = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
                    leg_l_connections = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                    if options_dict[part] == 'primary':
                        important_parts.append(part)
                        coefficients["kn_parts"] = add(leg_l_parts, coefficients["kn_parts"])
                        coefficients["kn_connections"] = add(leg_l_connections, coefficients["kn_connections"])
                    if options_dict[part] == 'secondary':
                        important_parts.append(part)
                        coefficients["secondary_kn_parts"] = add(leg_l_parts, coefficients["secondary_kn_parts"])
                        coefficients["secondary_kn_connections"] = add(leg_l_connections, coefficients["secondary_kn_connections"])
                case 'shoulders':
                    shoulders_parts = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    if options_dict[part] == 'primary':
                        important_parts.append(part)
                        coefficients["kn_parts"] = add(shoulders_parts, coefficients["kn_parts"])
                    if options_dict[part] == 'secondary':
                        important_parts.append(part)
                        coefficients["secondary_kn_parts"] = add(shoulders_parts, coefficients["secondary_kn_parts"])
                case 'hips':
                    hips_parts = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    if options_dict[part] == 'primary':
                        important_parts.append(part)
                        coefficients["kn_parts"] = add(hips_parts, coefficients["kn_parts"])
                    if options_dict[part] == 'secondary':
                        important_parts.append(part)
                        coefficients["secondary_kn_parts"] = add(hips_parts, coefficients["secondary_kn_parts"])
                case 'torso':
                    torso_parts = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
                    torso_connections = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
                    if options_dict[part] == 'primary':
                        important_parts.append(part)
                        coefficients["kn_parts"] = add(torso_parts, coefficients["kn_parts"])
                        coefficients["kn_connections"] = add(torso_connections, coefficients["kn_connections"])
                    if options_dict[part] == 'secondary':
                        important_parts.append(part)
                        coefficients["secondary_kn_parts"] = add(torso_parts, coefficients["secondary_kn_parts"])
                        coefficients["secondary_kn_connections"] = add(torso_connections, coefficients["secondary_kn_connections"])
                case _:
                    print(f"STRANGE PART NAMING: {part}")
                    print('Compare with CUSTOM_OPTIONS in filter')
                    return None
            
    #consider additional conections
    if 'hand_right' in important_parts and 'shoulders' in important_parts:
        connections = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if options_dict['hand_right'] == 'primary' and options_dict['shoulders'] == 'primary':
            coefficients["kn_connections"] = add(connections, coefficients["kn_connections"])
        else:
            coefficients["secondary_kn_connections"] = add(connections, coefficients["secondary_kn_connections"])

    if 'hand_left' in important_parts and 'shoulders' in important_parts:
        connections = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        if options_dict['hand_left'] == 'primary' and options_dict['shoulders'] == 'primary':
            coefficients["kn_connections"] = add(connections, coefficients["kn_connections"])
        else:
            coefficients["secondary_kn_connections"] = add(connections, coefficients["secondary_kn_connections"])

    if 'leg_right' in important_parts and 'hips' in important_parts:
        connections = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        if options_dict['leg_right'] == 'primary' and options_dict['hips'] == 'primary':
            coefficients["kn_connections"] = add(connections, coefficients["kn_connections"])
        else:
            coefficients["secondary_kn_connections"] = add(connections, coefficients["secondary_kn_connections"])

    if 'leg_left' in important_parts and 'hips' in important_parts:
        connections = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        if options_dict['leg_left'] == 'primary' and options_dict['hips'] == 'primary':
            coefficients["kn_connections"] = add(connections, coefficients["kn_connections"])
        else:
            coefficients["secondary_kn_connections"] = add(connections, coefficients["secondary_kn_connections"])

    return coefficients


def __compare_images_test(image1, image2, coefficients = Coefficients.DEFAULT):
    # factor = 0
    factor_parts = 0
    #k for parts: shoulders, hips, torso left, torso right, left forearm, left arm, right forearm, right arm, left thigh, left calve, right thigh, right calve
    #            sh, h, tl, tr, lf, la, rf, ra, lt, lc, rt, rc
    # default: shoulders: how straight, back or front; hips; torso sides: body upwards or sideways; legs thigh: standing, lying, sitting
    # kn_parts = [0.8, 0.3, 0.5, 0.5, 0, 0, 0, 0, 0.5, 0, 0.5, 0]
    kn_parts = coefficients["kn_parts"]
    kn_parts_sum = 0
    # kn_parts = [2, 1]
    # secondary_kn_parts = [0, 0, 0, 0, 0.5, 0, 0.5, 0, 0, 0, 0, 0]
    secondary_kn_parts = coefficients["secondary_kn_parts"]
    secondary_kn_parts_sum = 0
    secondary_factor_parts = 0
    print(f"Comparing {image1.path} and {image2.path}")
    for part in range(len(kn_parts)):
        print(f"comparing part {part}: {__compare_angles(image1.parts_angles[part], image2.parts_angles[part])}")
        print(f"{image1.parts_angles[part]} and {image2.parts_angles[part]}")
        factor_parts += kn_parts[part]*__compare_angles(image1.parts_angles[part], image2.parts_angles[part])
        kn_parts_sum += kn_parts[part]
        secondary_factor_parts += secondary_kn_parts[part]*__compare_angles(image1.parts_angles[part], image2.parts_angles[part])
        secondary_kn_parts_sum += secondary_kn_parts[part]
    print(f"Factor parts before devision: {factor_parts}")
    if kn_parts_sum != 0:
        factor_parts = factor_parts / kn_parts_sum
    if secondary_kn_parts_sum != 0:
        factor_parts = secondary_factor_parts / secondary_kn_parts_sum
    print(f"Factor parts after devision: {factor_parts}")

    factor_connections = 0
    #k for connections: 
    # default: hips-leg connection; shoulder-torso: bending forward body or straight
    # kn_connections = [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0]
    kn_connections = coefficients["kn_connections"]
    kn_connections_sum = 0
    # secondary_kn_connections = [0.5, 0.5, 0, 0, 0, 0, 0.5, 0.5, 0, 0]
    secondary_kn_connections = coefficients["secondary_kn_connections"]
    secondary_kn_connections_sum = 0
    secondary_factor_connections = 0
    for connection in range(len(kn_connections)):
        factor_connections += kn_connections[connection]*__compare_angles(image1.connection_angles[connection], image2.connection_angles[connection])
        kn_connections_sum += kn_connections[connection]
        secondary_factor_connections += secondary_kn_connections[connection]*__compare_angles(image1.connection_angles[connection], image2.connection_angles[connection])
        secondary_kn_connections_sum += secondary_kn_connections[connection]
    
    if kn_connections_sum != 0:
        factor_connections = factor_connections / kn_connections_sum
    if secondary_kn_connections_sum != 0:
        secondary_factor_connections = secondary_factor_connections / secondary_kn_connections_sum

    # factor = 2*factor_parts + factor_connections
    factor = 0.6*(factor_parts + factor_connections) + 0.4*(secondary_factor_parts + secondary_factor_connections)

    return factor