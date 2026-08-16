import re           # re module for regular expressions

def read_ips():     # ips.txt contains 1000 lines, each line is an IP address
    # read all content of file
    with open("ips.txt", "r") as file:      # reading mode
        content = file.read()

    # split into possible IPs (by whitespace or newline)
    ips = content.split()

    # remove duplicates using set, then back to list
    unique_ips = list(set(ips))

    return unique_ips


def get_pattern():
    # valid range: 47.82.11.0 - 47.82.11.255
    # rules:
    # - must start with 47.82.11.
    # - last number: 0–255
    # - no leading zero like 03

    pattern = r"^47\.82\.11\.(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"   # regex pattern for valid IPs in the specified range
    return pattern


def filter_ips(all_ips):
    correct = []        # list to store valid IPs
    pattern = get_pattern()

    for ip in all_ips:
        if re.match(pattern, ip):   # check if the IP matches the pattern
            if ip not in correct:   # avoid duplicates
                correct.append(ip)

    return correct


def main():
    # do not change below code
    all_ips = read_ips()
    correct_ips = filter_ips(all_ips)
    for p in correct_ips:           # print each valid IP address
        print(p)                    # print total count of valid IP addresses
    print(len(correct_ips))         # print the total number of valid IP addresses found


if __name__ == "__main__":
    main()

# run with: python ips.py
# test with: python pytest test_ips.py
