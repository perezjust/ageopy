import os
import string
import sys
import traceback
import shutil
import logging
import os.path
import zipfile
import getpass
##import arceditor


##sys.path.append(r"\\ptalfsg001\Geomatics\Users\Justin_Perez\EXPTools\Scripts")
##import expFuncs as expF
##from expFuncs import *

def main():
    
    try:

        with open(os.path.join(os.getcwd(), "my.txt"), "wb") as f:
            f.write(getpass.getuser())
        
##
##        logme = expF.logIt(r"\\ptalwsg003\wwwroot\URS")
##        logme.logMessageHeader("start")
##        logme.logMessage(getpass.getuser())
##        
##        #search_path = r"\\ptalweb001\lws\download"
##        #search_uploads(search_path)
##        
##        logme.logMessage("stop")


    except:
        print traceback.format_exc()
        logme.logTrace()


def attribute_check(gdb_catalog):
    pass
        
        
        

        

def search_uploads(search_path):
    logme.logMessage("naught here")
    for upload_job_path in os.listdir(search_path):
        if os.path.exists(os.path.join(search_path, upload_job_path, "report.txt")):
            pass
        else:
            zipfilelist = []
            for dirpath, dirnames, filenames in os.walk(os.path.join(search_path, upload_job_path)):
                for fi in filenames:
                    if fi.endswith(".zip"):
                        zipfilelist.append(os.path.join(dirpath, fi))
            if len(zipfilelist) != 1:
                logme.logMessage("zipfilelist != 1" + str(upload_job_path))
            else:
                unzip(zipfilelist[0], os.path.join(search_path, upload_job_path))
                find_filegdb_unzipped(os.path.join(search_path, upload_job_path))



def find_filegdb_unzipped(upload_job_path):
    logme.logMessage("and here")
    dot_fgdb_list = []
    fgdb_list = []
    for dirpath, dirnames, filenames in os.walk(upload_job_path):
        if dirpath.endswith(".gdb"):
            dot_fgdb_list.append(dirpath)
    for fgdb_dir in dot_fgdb_list:
        logme.logMessage(arcpy.Describe(fgdb_dir).workspaceFactoryProgID)
        if arcpy.Describe(fgdb_dir).workspaceFactoryProgID == "esriDataSourcesGDB.FileGDBWorkspaceFactory":
            fgdb_list.append(fgdb_dir)
    if len(fgdb_list) != 1:
        logme.logMessage("fgdb_list doesn't have only one acutal fdgb")
        logme.logMessage(fgdb_list)
        print fgdb_list
    else:
        resolved_fgdb_path = sanitize_fgdb_dirname(upload_job_path, fgdb_list[0])
        generate_reciept(upload_job_path, resolved_fgdb_path)



def sanitize_fgdb_dirname(upload_job_path, fgdb_path):
    logme.logMessage("...and here?")
    '''
        Seems like using arcpy, if a file gdb is in a folder with the name ending in ".gdb"
        scripting seems to not find the arcpy.List*Object* objects
    '''
    dot_gdb_dirnames = []
    return_fgdb_path = ""
    dot_gdb_dirnames = [ dirname for dirname in str(os.path.dirname(fgdb_path)).split("\\") if dirname.endswith(".gdb") ]
    if len(dot_gdb_dirnames) > 0:
        new_fgdb_dirname = os.path.join(upload_job_path, "sanitized_fgdb_dirname")
        if os.path.exists(new_fgdb_dirname):
            os.rmdir(new_fgdb_dirname)
        os.mkdir(new_fgdb_dirname)
        shutil.move(fgdb_path, new_fgdb_dirname)
        return_fgdb_path = os.path.join(new_fgdb_dirname, os.path.basename(fgdb_path))
    else:
        return_fgdb_path = fgdb_path
    return return_fgdb_path 



def build_txtfile_name():
    dtn = str(datetime.datetime.now()).split(" ")
    dtn1 = "".join("".join(dtn[1].split(":")).split("."))
    dayValue = "".join(dtn[0].split("-"))
    #txtfile = dayValue + "yyyymmdd" + dtn1 + "hhmmssssss"
    txtfile = "report"
    return txtfile
    


def generate_reciept(download_job_path, fgdb_path):
    #db_catalog = gpF.ESRI_DBBrowser(fgdb_path).build_db_catalog()
    #attribute_check(db_catalog)
    txtpath = os.path.join(download_job_path, build_txtfile_name() + ".txt")
    db_catalog = gpF.ESRI_DBBrowser(fgdb_path).build_db_catalog()
    report_items = []
    for i in db_catalog:
        fl = gpF.featureLayer(i)
        report_items.append(str(fl.count()) + " ---" + str(fl.name))
    with open(txtpath, 'w') as wrt:
        for rptitems in report_items:
            wrt.write(rptitems + "\r\n")

    email_sendto = get_email_sendto(os.path.join(download_job_path, "email.txt"))
    send_email(email_sendto, txtpath)



def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)                        
    return path



def get_email_sendto(email_textfile):
    with open(email_textfile, "r") as readme:
        email_sendto = readme.readline()
    return email_sendto


def send_email(send_to, f):
    #http://stackoverflow.com/questions/16084605/encoding-of-headers-in-mimetext -- maybe this one better
    #http://stackoverflow.com/questions/882712/sending-html-email-using-python
    send_from = "some.name@somedomain.com"
    text = "You have submitted data to .\n\nSee the attached text file for a report of the data processed.\n\nThanks."
    
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.header import Header
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Utils import COMMASPACE, formatdate
    from email import Encoders
    try:

        subject = 'Some Project'
        server = "some.ip.address.number"
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Subject'] = subject
        
        msg.attach( MIMEText(text, "plain"))
        
        part = MIMEBase('application', "txt")   # Change if different file type sent.
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
        logme.logMessage(msg.as_string())
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
    except:
        print traceback.format_exc()




if __name__ == "__main__":
    main()



