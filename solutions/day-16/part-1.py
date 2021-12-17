import math

input = open("input.txt", "r")

hexa_binary_tbl = {
    "0": ["0", "0", "0", "0"],
    "1": ["0", "0", "0", "1"],
    "2": ["0", "0", "1", "0"],
    "3": ["0", "0", "1", "1"],
    "4": ["0", "1", "0", "0"],
    "5": ["0", "1", "0", "1"],
    "6": ["0", "1", "1", "0"],
    "7": ["0", "1", "1", "1"],
    "8": ["1", "0", "0", "0"],
    "9": ["1", "0", "0", "1"],
    "A": ["1", "0", "1", "0"],
    "B": ["1", "0", "1", "1"],
    "C": ["1", "1", "0", "0"],
    "D": ["1", "1", "0", "1"],
    "E": ["1", "1", "1", "0"],
    "F": ["1", "1", "1", "1"]
}

def binary_to_decimal(raw):
    sum = 0
    length = len(raw)
    for i in range(length):
        sum += int(raw[i]) * pow(2, length - 1 - i)
    return sum

class Operator:
    def values(packets):
        return list(map(lambda x: x.get_value(), packets))

    def max(packets):
        return max(Operator.values(packets))

    def min(packets):
        return min(Operator.values(packets))

    def sum(packets):
        return sum(Operator.values(packets))

    def product(packets):
        return math.prod(Operator.values(packets))

    def greater_than(packets):
        if packets[0].get_value() > packets[1].get_value():
            return 1
        else:
            return 0

    def less_than(packets):
        if packets[0].get_value() < packets[1].get_value():
            return 1
        else:
            return 0
    
    def equal_to(packets):
        if packets[0].get_value() == packets[1].get_value():
            return 1
        else:
            return 0

class Parser:
    def __init__(self, raw, starting_index=0):
        self.raw = raw
        self.current_index = starting_index

    def get_next(self, i):
        raw_slice = self.raw[self.current_index : self.current_index + i]
        self.current_index += i
        return raw_slice

class Packet:
    def new(raw):
        parser = Parser(raw)
        return Packet.parse(parser)
    
    def parse(parser):
        version = binary_to_decimal(parser.get_next(3))
        type_id = binary_to_decimal(parser.get_next(3))

        if type_id == 4:
            return LiteralPacket.parse(parser, version, type_id)
        else:
            return OperatorPacket.parse(parser, version, type_id)


class LiteralPacket(Packet):
    def __init__(self, version, type_id, value):
        self.version = version
        self.type_id = type_id
        self.value = value
    
    def parse(parser: Parser, version, type_id):
        # Value
        binary_value = []
        while True:
            group_flag = int(parser.get_next(1)[0])
            binary_value.extend(parser.get_next(4))

            if group_flag == 0:
                break
        value = binary_to_decimal(binary_value)

        # Create the packet
        return LiteralPacket(
            version = version, 
            type_id = type_id, 
            value = value
        )
    
    def get_value(self):
        return self.value


class OperatorPacket(Packet):
    type_id_function_tbl = {
        0: Operator.sum,
        1: Operator.product,
        2: Operator.min,
        3: Operator.max,
        5: Operator.greater_than,
        6: Operator.less_than,
        7: Operator.equal_to
    }

    def __init__(self, version, type_id, length_type_id, packets):
        self.version = version
        self.type_id = type_id
        self.length_type_id = length_type_id
        self.packets = packets

    def parse(parser: Parser, version, type_id):
        # Length Type Id
        length_type_id = int(parser.get_next(1)[0])

        # Packets and Packets Length 
        packets = []
        if length_type_id == 0:
            packets_length = binary_to_decimal(parser.get_next(15))
            end_index = parser.current_index + packets_length
            while True:
                packets.append(Packet.parse(parser))
                if parser.current_index >= end_index:
                    break
        else:
            packets_number = binary_to_decimal(parser.get_next(11))
            while True:
                packets.append(Packet.parse(parser))
                if len(packets) == packets_number:
                    break

        return OperatorPacket(
            version = version,
            type_id = type_id,
            length_type_id = length_type_id,
            packets = packets
        )

    
    # This returns all the packets. It goes deep
    def get_all_packets(self):
        all_packets = []
        for packet in self.packets:
            if isinstance(packet, OperatorPacket):
                all_packets.extend(packet.get_all_packets() + [packet])
            else:
                all_packets.append(packet)

        return all_packets

    # This returns all the packets in the operator
    def get_packets(self):
        return self.packets

    def get_value(self):
        operator = OperatorPacket.type_id_function_tbl[self.type_id]
        return operator(self.get_packets())

# Convert Hexa to Binary
binary = []
for char in input.readline():
    if char in hexa_binary_tbl:
        binary.extend(hexa_binary_tbl[char])

# Parse the packet
packet = Packet.new(binary)

# Get the version sum
version_sum = packet.version + sum(list(map(lambda x: x.version, packet.get_all_packets())))

# Print the version sum
print(version_sum)
