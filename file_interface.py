import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.join(current_dir, 'files')
        os.chdir(target_dir)
        # print(os.getcwd())
        # os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def upload(self, params=[]):
        try:
            filename = params[0]
            content_base64 = params[1]
            content = base64.b64decode(content_base64)
            with open(filename, 'wb') as f:
                f.write(content)
            return dict(status='OK', data='Successfully upload file')
        except Exception as e:
            return dict(status='ERROR', data=str(e))
        
    def delete(self, params=[]):
        try:
            filename = params[0]
            os.remove(filename)
            return dict(status='OK', data='Successfully delete file')
        except Exception as e:
            return dict(status='ERROR', data=str(e))



if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))
