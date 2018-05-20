#!/usr/bin/python
import re
import sys, getopt

#import pandas as pd

def main(argv):
   mac_address = "00:00:00:00:00:00"
   try:
      opts, args = getopt.getopt(argv,"hm::",["mac-address="])
   except getopt.GetoptError:
      print 'test.py -m <mac-address>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -m <mac-address>'
         sys.exit()
      elif opt in ("-m", "--mac-address"):
         mac_address = arg
   filepath = 'scratch.txt'
   data = parse(filepath, mac_address)
   print(data)

def parse(filepath,mac_address):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file to be parsed
    mac_address: str
        Filepath for file to be parsed
    Returns
    -------
    data : []

    """

    data = []
    with open(filepath, 'r') as file:
        line = file.readline()
        dhcpack_counter = 0
        dhcprequest_counter = 0
        while line:
            word_list = line.split()

            if "DHCPACK" in word_list[5]:
                reg_match = _RegExLib(word_list[9])
                if mac_address in reg_match.mac_address.group():
                    dhcpack_counter = dhcpack_counter + 1

            if "DHCPREQUEST" in word_list[5]:
                reg_match = _RegExLib(word_list[9])
                if mac_address in reg_match.mac_address.group():
                    dhcprequest_counter = dhcprequest_counter + 1

            line = file.readline()

        dict_of_data = {
            'MAC ADDRESS': "00:40:05:6d:7c:a2",
            'DHCPACK': dhcpack_counter,
            'DHCPREQUEST': dhcprequest_counter,
        }
    return dict_of_data


class _RegExLib:
    """Set up regular expressions"""
    # use https://regexper.com to visualise these if required
    _reg_school = re.compile('School = (.*)\n')
    _reg_grade = re.compile('Grade = (.*)\n')
    _reg_name_score = re.compile('(Name|Score)')
    #(.*) are (.*?) .* Jan 15 13:49:59 proxy dhcpd: DHCPACK on 192.168.0.23 to 00:80:ad:01:7e:12 (programming) via eth1
    _reg_dhcpack = re.compile(r'proxy dhcpd: DHCPACK on (.*) to (.*) (.*) (.*)')
    _reg_mac_address = re.compile(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')

    def __init__(self, line):
        # check whether line has a positive match with all of the regular expressions
        self.school = self._reg_school.match(line)
        self.grade = self._reg_grade.match(line)
        self.name_score = self._reg_name_score.search(line)
        self.dhcpack = self._reg_dhcpack.search(line)
        self.mac_address = self._reg_mac_address.search(line)


if __name__ == '__main__':
    main(sys.argv[1:])