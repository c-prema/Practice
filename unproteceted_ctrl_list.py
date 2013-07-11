import sys
import urllib

# To avoind authentication prompt
class myURLopener(urllib.FancyURLopener):

    def http_error_401(self, url, fp, errcode, errmsg, headers, data=None):
        return None


def update_progress(progress, total):
    """ Progress bar """
    percent = int(100 * progress / total)
    line = ('=' * (percent) + '>').ljust(100)
    sys.stdout.write("\r[{0}] {1}%".format(line, percent))
    sys.stdout.flush()

def get_methods(in_file):
    """ Returns all methods"""
    lines = open(in_file).readlines()
    fun_lines = []
    for line in lines: 
        if  line.startswith("def manage_add") or '__init__' in line or 'def manage_afterAdd(' in line:
            continue
        if 'def ' in line and line.strip()[0]!='#':
            fun_name = line.split('def ')[1].split("(")[0]
            fun_lines.append(fun_name)
    return fun_lines

def get_un_protected(url, ctrs_lst):
    """ Returns lists of dictionary containing Protected, Unprotected, Private methods"""
    final_dict= {'Protected':[], 'Unprotected':[], 'Private':[]}
    total_cont = len(ctrs_lst)
    for index, ctr in enumerate(ctrs_lst):
        if ctr.startswith("_"):
            final_dict['Private'].append(ctr)
        else:
            url_opener = myURLopener()
            content = url_opener.open(url+ctr).read()
            if not 'input[type=text]' in content:
                final_dict['Unprotected'].append(ctr)
            else:
                final_dict['Protected'].append(ctr)
        update_progress(index+1, total_cont)
    return final_dict

def write_to_file(filt_dict, out_file):
    """ Writss to file"""
    unprotected_list = filt_dict['Unprotected']
    protected_list = filt_dict['Protected']
    private_list = filt_dict['Private']
    fout = open(out_file, 'w')
    fout.write("Unprotected methods list \n" + \
               '-' * 30 + "\n" +\
               '\n'.join(unprotected_list))
    fout.write("\n\nPrivate methods list \n" + \
               '-' * 30 + "\n" +\
               '\n'.join(private_list))
    fout.write("\n\nProtected methods list \n" + \
               '-' * 30 + "\n" +\
               '\n'.join(protected_list))
    fout.close()
    print "Unprotected methods:", len(unprotected_list)
    print "Private methods:", len(private_list)
    print "Protected methods:", len(protected_list)
    print "Details saved in", out_file

if __name__== "__main__":
    module = sys.argv[1]
    url = "http://192.168.4.129:4547/cms/"+module+"/Controller/"
    in_file = sys.argv[2]
    out_file = "outfile"
    if len(sys.argv) > 3:
        out_file = sys.argv[3]
    total_methods = get_methods(in_file)
    total_count = len(total_methods)
    filtered_dict = get_un_protected(url, total_methods)
    print "\nTotal methods: ", total_count
    write_to_file(filtered_dict, out_file)

