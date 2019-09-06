import os

#cn_dict[ip] = {cn1: {0201, 0301, ...}, cn2: {0201, ...}}
cn_dict = {}

__all__ = os.listdir(".")
for filename in __all__:
    if filename.startswith("resolver_dot"):
        inputf = open(filename)
        for line in inputf:
            try:
                ip, cc, cn, ver = line.split("\t")
            except:
                print filename, line
            if ip not in cn_dict:
                cn_dict[ip] = {}
            if cn not in cn_dict[ip]:
                cn_dict[ip][cn] = {}
            cn_dict[ip][cn][filename[filename.find("19"):filename.find(".txt")]] = 0

for filename in __all__:
    if filename.startswith("resolver_dot"):
        inputf = open(filename)
        outputf = open("../" + filename, "w")
        for line in inputf:
            line = line.strip()
            try:
                ip, cc, cn, ver = line.split("\t")
            except:
                print filename, line
            # check the major cn from the dict.
            for cn_temp in cn_dict[ip]:
                if len(cn_dict[ip][cn_temp]) >= 3:
                    if cn != cn_temp:
                        if cn[3:] not in cn_temp[3:] and cn_temp[3:] not in cn[3:]:
                            print filename, line, cn_temp, cn_dict[ip][cn_temp]
                            cn = cn_temp
                            line = ip + "\t" + cc + "\t" + cn + "\t" + ver
            outputf.write(line + "\n")
