import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""



class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
    def proses_string(self,string_datamasuk=''):

        try:
            if " " not in string_datamasuk:
                c_req = string_datamasuk.lower().strip()
                params = []
            else:
                c = string_datamasuk.split(" ", 1)
                c_req = c[0].lower().strip()

                if len(c) > 1:
                    if c_req == 'upload':
                        data = c[1].split(" ", 1)
                        params = data
                    else:
                        try:
                            params = shlex.split(c[1])
                        except Exception as e:
                            logging.warning(f"Parsing error: {e}")
                            params = c[1].split()
            
                else:
                    params = []

            logging.warning(f"Process request: {c_req}")
            if hasattr(self.file, c_req):
                cl = getattr(self.file, c_req)(params)
                return json.dumps(cl)
            else:
                return json.dumps(dict(status='ERROR',data='request tidak dikenali'))
        except Exception:
            return json.dumps(dict(status='ERROR',data=f'Error process: {e}'))

if __name__=='__main__':
    #contoh pemakaian
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))
