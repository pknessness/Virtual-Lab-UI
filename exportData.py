from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename,askdirectory
import shutil
import os, openpyxl, random, boto3, botocore
from tempfile import NamedTemporaryFile
from credentials import ACCESS_KEY, SECRET_KEY

s3_client = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    #aws_session_token=SESSION_TOKEN
    )

bucket = "vlabtesting"
dataBaseDirectory = "raw_data/"

randomization = 0.0001

def download_file(key):
    try:
        file = NamedTemporaryFile(suffix = '.xlsx', delete=True)
        s3_client.download_file(bucket, key, file.name)
        return file.name
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return None
        else:
            raise
    else:
        raise

def export(material, test):
    key = dataBaseDirectory + test + "/" + material + ".xlsx"
    # url = s3_client.generate_presigned_url('get_object', 
    #                                     Params = {'Bucket': bucket, 'Key': key}, 
    #                                     ExpiresIn = 30) #this url will be available for 40 minutes
    #workbook = openpyxl.load_workbook('raw_data\\'+ test +'\\'+ material +'.xlsx')
    file = download_file(key)
    workbook = openpyxl.load_workbook(file)
    for i in workbook:
        for j in i:
            for k in j:
                if(type(k.value) == float):
                    k.value += random.randint(-1,1) * randomization
                    
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    dir = askdirectory() # show an "Open" dialog box and return the path to the selected file
    print(dir)
    src = os.path.abspath(__file__)

    # shutil.copy2('raw_data\\'+material+'.xlsx', dir)
    # shutil.copy2('raw_data\\'+material+'.xlsx', dir)
    workbook.close()
    workbook.save(dir+'/' + material + test +'.xlsx')