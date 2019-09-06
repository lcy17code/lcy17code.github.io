#!/usr/bin/python
#encoding:   utf-8

import re
import os
import sys
import time
import string

try:
    from entropy import shannon_entropy
except:
    pass

class domain_parser(object):
    def __init__(self, filename = './public_suffix_list.dat'):
        self.suffix = {}
        self.sld_domain = {}
        self.psl_file = filename
        self.ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
        self.DIGIT = '0123456789'

        self.suffix = domain_parser._load_dict_dn(self.psl_file)

        self.filter_file = './filter_domain.txt'
        self.filter_domain = domain_parser._load_dict_dn(self.filter_file)

    @classmethod
    def _load_dict_dn(cls, file):
        tmp_dict = {}
        try:
            fd = open(file, 'r')
        except:
            sys.stdout.write("=======open %s failed\n" %file)
            sys.exit(1)

        for line in fd:
            line = line.strip()
            if line.startswith("//") or len(line) == 0:
                continue
            line = line.split()[0]
            if line in tmp_dict:
                tmp_dict[line] = None
            else:
                tmp_dict[line] = None
        fd.close()

        return tmp_dict

    @classmethod
    def _load_filter_dn(cls, file):
        keywords_regex1 =  ""

        try:
            fp = open(file, 'r')
        except:
            sys.stdout.write("open %s failed\n" %file)
            sys.exit(1)

        for line in fp:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
        
            keywords_regex1 += line + '|'
        fp.close()

        return keywords_regex1.strip('|')
        

    def get_tld(self, dn):
        tld = None
        dn_segs = dn.split('.')
        seg_num = len(dn_segs)
        for i in xrange(0, seg_num, 1):
            tld = '.'.join(dn_segs[i:])
            if tld in self.suffix:
                return tld

        #if nothing find, just return 'invalid'
        return "invalid"

    def get_tld_detail(self, dn):
        tld = None
        dn_segs = dn.split('.')
        seg_num = len(dn_segs)
        for i in xrange(0, seg_num, 1):
            tld = '.'.join(dn_segs[i:])
            if tld in self.suffix:
                return tld, None

        #if nothing find, just return 'invalid'
        return "invalid", dn_segs[-1]

    def get_sld(self, dn):
        second_ld = None

        dn_segs = dn.split('.')
        seg_num = len(dn_segs)
        for i in xrange(seg_num-1, -1, -1):
            second_ld = '.'.join(dn_segs[i:])
            if second_ld not in self.suffix:
                return second_ld

        return None

    def is_nested_dn(self, dn):
        prev_pos = 0
        etld_count = 0
        dn_segs = dn.split('.')
        num_segs = len(dn_segs)

        for i in xrange(num_segs):
            if self.suffix.has_key(dn_segs[i]):
                etld_count += 1
                if etld_count >= 2:
                    return True
                if prev_pos and (i - prev_pos > 1):
                    return True
            else:
                 prev_pos = i
        return False
    
    def is_chrome_dn(self, dn):
        dn_segs = dn.split('.')
        num_segs = len(dn_segs)
        alpha_num = 0
        random_len = len(dn_segs[0])
        if random_len >= 10 and random_len <= 10 and shannon_entropy(dn_segs[0]) > 0.30:
            for letter in dn_segs[0]:
                if letter in self.ALPHABET:
                    alpha_num += 1
            if alpha_num == random_len:
                return True
        return False


    def is_filter_domain(self, dn):
        if dn in self.filter_domain:
            return True
        else:
            return False
        """
        if re.search(self.sld_regex, dn) != None:
            return True
        return False
        """
