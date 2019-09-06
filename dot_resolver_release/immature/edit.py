import os
'''
__all__ = os.listdir(".")
for filename in __all__:
    if filename.startswith("dot"):
        inputf = open(filename)
        outputf = open("resolver_" + filename, "w")
        for line in inputf:
            line = line.strip()
            if "cleanbrowsing.org" in line or "cloudflare-dns" in line or "dns.google" in line\
                    or "quad9.net" in line or "nextdns.io" in line:
                if "\"ok\"" not in line:
                    continue
            elif "support@fortinet.com" in line:
                if "\"ok\"" in line:
                    continue
            outputf.write(line + "\n")
'''

__all__ = os.listdir(".")
for filename in __all__:
    if filename.startswith("resolver_dot"):
        os.system("cat " + filename + " | sort | uniq > ../" + filename)

