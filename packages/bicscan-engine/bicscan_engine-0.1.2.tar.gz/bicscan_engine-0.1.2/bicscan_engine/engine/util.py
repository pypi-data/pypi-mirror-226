class Utils:
    @staticmethod
    def find_all_occurrences(bytecode, char):
        occurrences = []
        index = 0
        while index < len(bytecode):
            index = bytecode.find(char, index)
            if index == -1:
                break
            occurrences.append(index)
            index += 1
        return occurrences

    @staticmethod
    def make_unique_list(input_list):
        return list(set(input_list))

    @staticmethod
    def is_ipfs_uri(uri):
        return uri.count("ipfs") >= 1

    @staticmethod
    def is_https_uri(uri):
        return uri.startswith("https://")
