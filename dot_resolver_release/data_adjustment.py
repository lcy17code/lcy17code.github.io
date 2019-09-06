import os
from domain_parser import *

dn_parser = domain_parser()

#cn_dict[ip] = {cn1: {0201, 0301, ...}, cn2: {0201, ...}}

cn_dict = {}

__all__ = os.listdir(".")
for filename in sorted(__all__):
    if filename.startswith("resolver_dot"):
        print filename
        # no need to adjust fig 3.
        # os.system("grep perfect-privacy " + filename + " | wc -l")

        # provider_all[sld] = {ip1, ip2, ...}
        provider_all = {}
        provider_single = {}
        provider_invalid = {}
        # count the # of providers / providers with only 1 ip / providers with invalid certs.
        inputf = open(filename)
        for line in inputf:
            line = line.strip()
            ip, cc, cn, ver = line.split("\t")
            cn = cn[3:]
            try:
                sld = dn_parser.get_sld(cn)
            except:
                sld = cn
            if "fortinet" in sld:
                sld = "fortinet"
            if sld not in provider_all:
                provider_all[sld] = {}
            provider_all[sld][ip] = 0
            if "ok" not in ver:
                provider_invalid[sld] = 0
        print len(provider_all)
        print len(provider_invalid)
        single = 0
        for sld in provider_all:
            if len(provider_all[sld]) == 1:
                single += 1
        print single
        # print provider_all.keys()