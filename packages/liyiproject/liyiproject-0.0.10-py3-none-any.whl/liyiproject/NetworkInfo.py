import os
import re


class network():
    """IP_info generate

    """
    def interfaces(self):

        # register the new dictionary and receive the generated information
        dict_ipinfo = {}

        # The ip interface information was extracted
        ip_int_name = os.popen("%sip addr | awk '{print $2}' | grep ':$'"%(self.sbin_path)).read().split("\n")
        for ip_length in range(len(ip_int_name) - 1):
            try:
                dict_ipinfo[re.sub(r'[:]', "", ip_int_name[ip_length])] = \
                    os.popen("%sip addr | grep '%s' | grep inet' ' | awk '{print $2}'"
                             % (self.sbin_path,ip_int_name[ip_length].replace(":", ""))).read().replace("\n", " ")
            except Exception as err:
                dict_ipinfo[re.sub(r'[:]', "", ip_int_name[ip_length])] = ''
        return dict_ipinfo

    def __init__(self):
        self.sbin_path = '/usr/sbin/'

    def local_routings(self):
        dict_route = {"routeinfo": {}}
        try:
            for list_num in range(len(os.popen("%sroute -n | grep -v ^K | grep -v ^D"%(self.sbin_path)).read().split("\n")) - 1):
                list_dict = {}
                a1 = os.popen("%sroute -n | grep -v ^K | grep -v ^D"%(self.sbin_path)).read().split("\n")
                value = re.sub(r'[ ]+', ",", a1[list_num])
                for value_num in range(len(value.split(","))):
                    a = os.popen("%sroute -n | grep -v ^K | grep ^D"%(self.sbin_path)).read().replace("\n", "")
                    title = re.sub(r'[ ]+', ",", a).split(",")[value_num]
                    list_dict[title] = value.split(",")[value_num]
                dict_route['routeinfo']['{}'.format(list_num + 1)] = list_dict
        except Exception as err:
            dict_route['routeinfo']['{}'.format(list_num + 1)] = ''
        return dict_route


if __name__ != "__main__":
    network