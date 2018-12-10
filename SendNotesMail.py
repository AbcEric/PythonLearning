#
# IBM Lotus Notes V8.5邮件读写
#
# 环境：Python3.6
#
# 需要完善的地方：
# 1. 如何传入用户名密码？运行可以不启动Notes客户端
# 2. 如何确保不同的用户可以切换？

import os
import tempfile
import copy
import sys
import datetime
from win32com.client import DispatchEx
from win32com.client import makepy


class NoAttachmentException(Exception):
    def __init__(self, value=None):
        Exception.__init__(self, value)


class Extract():
    def __init__(self, document):
        """初始化
            @param document: The Notes Document that will be extract
        """
        self.document = document

    def __get_temp_path(self):
        temp_index, temp_path = tempfile.mkstemp()
        os.close(temp_index)
        return temp_path

    def get_attachment(self, filepath=None):
        """Get attachments of a document
            @param filepath
             The path want to save file
             if not given, then current directory will be used
        """
        attachment_packs = []

        for item in range(len(self.document.Items)):
            t_item = self.document.Items[item]
            if t_item.Name == '$FILE':
                attachment_path = self.__get_temp_path()
                filename = t_item.Values[0]
                filebase, separator, file_extension = filename.rpartition('.')
                attahment = self.document.GetAttachment(filename)
                attahment.ExtractFile(attachment_path)
                attachment_content = open(attachment_path, 'rb').read()
                os.remove(attachment_path)
                attachment_packs.append((filebase, file_extension, attachment_content))

        if len(attachment_packs) == 0:
            raise NoAttachmentException('No attachment in document. ')

        for pack in attachment_packs:
            filename = pack[0] + '.' + pack[1]
            if filepath:
                filename = filepath + filename
            with open(filename, 'wb') as fh:
                fh.write(pack[2])

    # 修改为取指定数目的文档：
    def extract(self, num=5):
        """提取Document
            @param document: notes文档
            @return dict:
             subject -> 主题
             date ->日期
             From -> 发件人
             To -> 收件人
             body -> 主体
        """
        result = []
        item = {}
        #result['subject'] = self.document.GetItemValue('Subject')[0].strip()
        i = 0
        for doc in self.document:
            item['subject'] = doc.GetItemValue('Subject')[0].strip()
            item['From'] = doc.GetItemValue('From')[0].strip()
            result.append(copy.deepcopy(item))
            i += 1
            if i > num:
                break
        '''
        # result['date'] = self.document.GetItemValue('PostedDate')[0]          # ????
        '''
        # result['From'] = self.document.GetItemValue('From')[0].strip()
        # result['To'] = self.document.GetItemValue('SendTo')
        # result['body'] = self.document.GetItemValue('Body')[0].strip()

        return result


class NotesMail():
    # 发送读取邮件有关的操作
    def __init__(self, server, file):
        """Initialize
            @param server
             Server's name of Notes
            @param file
             Your data file, usually ends with '.nsf'
        """
        self.session = DispatchEx('Notes.NotesSession')
        self.server = self.session.GetEnvironmentString("MailServer", True)
        self.db = self.session.GetDatabase(server, file)
        self.db.OPENMAIL
        self.myviews = []

    def send_mail(self, receiver, subject, body=None):
        """发送邮件
            @param receiver: 收件人
            @param subject: 主题
            @param body: 内容
        """
        doc = self.db.CREATEDOCUMENT
        doc.sendto = receiver
        doc.Subject = subject
        if body:
            doc.Body = body
        doc.SEND(0, receiver)

    def get_views(self):
        for view in self.db.Views:
            if view.IsFolder:
                print("ViewName=", view.name)
                self.myviews.append(view.name)

    def get_documents(self, view_name):
        """
            @return generator
        """
        documents = []
        folder = self.db.GetView(view_name)
        if not folder:
            raise Exception('Folder {0} not found. '.format(view_name))
        document = folder.GetFirstDocument
        while document:
            # print("Document=", document)
            documents.append(document)
            document = folder.GetNextDocument(document)

        return documents

    def read_mail(self, view, attachment=False):
        """Read the latest mail
            @param view: The view(fold) to access
            @param attachment: Boolean, whether get attachment
            @return, dict: Info of a mail
        """
        result = {}

        # 只读Inbox内容：
        if "Inbox" not in view:
            return result

        documents = self.get_documents(view)
        # print("Get_Documents=", view, documents)
        if len(documents) != 0:
            # 只取最新的文档：
            # latest_document = documents[-1:][0]

            # 取指定数目的文档：将输入修改为列表
            # extra_obj = Extract(latest_document)
            extra_obj = Extract(documents)
            result = extra_obj.extract(10)

            # 取附件未做修改，需要完善：
            if attachment:
                extra_obj.get_attachment()

        return result


def main():
    # 修改为正确的用户名：
    # recivers = ['xxxx@abchina.com']
    if len(sys.argv) < 3:
        print("Usage: SendNotesMail send_user recv_user")
        print("SendNotesMail mail\kfzx\yyyy xxxx@abchina.com")
        exit(1)

    sender = sys.argv[1]
    recivers = sys.argv[2]

    makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
    makepy.GenerateFromTypeLibSpec('Lotus Notes Automation Classes')

    mail = NotesMail('ZH_NSD@ABC', sender)

    print("1. Send mail")
    mail.send_mail(recivers, 'test sender', 'This is a test mail body ')

    print("2. Get views")
    mail.get_views()

    print("3. Read mail")
    for view in mail.myviews:
        info = mail.read_mail(view, attachment=False)
        print(view, info)

if __name__ == '__main__':
    main()
