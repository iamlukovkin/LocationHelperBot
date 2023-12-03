class GDrive:
    def __init__(self, credentials, scope):
        '''
        Class of functions for working with Google Drive.
        
        credentials: GDrive credentials :obj:`str`
        scope: GDrive scope :obj:`str`
        '''
        print(f'Launching module {__name__}')
        self.credentials = credentials
        self.scope = scope
        self.Auth()
    
    
    def Auth(self):
        '''
        Repeat authentification to GDrive.
        '''
        from pydrive2.auth import GoogleAuth
        from pydrive2.auth import ServiceAccountCredentials
        from pydrive2.drive import GoogleDrive
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials, self.scope)
        gauth.Authorize()
        self.drive = GoogleDrive(auth=gauth)
        print('Authentification success!')
        return self.drive


    def CreateFolder(self, title: str, parent_folder_id: str):
        '''
        Creating new folder inside user's GDrive.

        title: name of new folder. :obj:`str`
        parent_folder_id: id of folder where will located new folder :obj:`str`

        return: id of created folder \n
        rtype: :obj:`str`
        '''
        self.Auth()
        folder_metadata = {
            'title': title,
            'parents':[{'id': parent_folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder

    
    def GetFromFolder(self, folder_id):
        '''
        Getting list of files from GDrive folder.

        folder_id: id of folder from will taken list of files :obj:`str`

        return: file_list\n
        rtype: :obj:`dict`
        '''
        self.Auth()
        file_list = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        return file_list
    

    def SendFile(self, file_path, title, folder_parent):
        '''
        Sending user files to GDrive.

        GFile: all file's info getted by GetFromFolder function. :obj:`dict`
        folder_path: path where located the sending file. :obj:`str`
        folder: id of GDrive folder where will located sending files. :obj:`str`

        return: none\n
        rtype: :obj:`None`
        '''
        self.Auth()
        file = self.drive.CreateFile()
        file['title'] = title
        file['parents'] =[{'id': folder_parent}]
        file.SetContentFile(file_path)
        file.Upload()
        return file

    
    def DeleteFile(self, file_id):
        '''
        Deleting user files from GDrive.

        GFile: all file's info getted by GetFromFolder function. :obj:`dict`
        
        return: none\n
        rtype:  :obj`None`
        '''
        self.Auth()
        file = self.drive.CreateFile({"id": file_id})
        file.Delete()
    
    def GetFile(self, title, FileID, folder_path):
        '''
        Downloading user files from GDrive.

        FileID: all file's info getted by GetFromFolder function. :obj:`dict`
        folder_path: path where required file will be downloaded. :obj:`str`

        return: path of downloaded file\n
        rtype:  :obj`str`
        '''
        self.Auth()
        
        file = self.drive.CreateFile({'id': FileID})
        file_path = f'{folder_path}/{title}'
        file.GetContentFile(file_path)
        return file_path

async def conn_google_drive(credentials: str, scope: str):
    return GDrive(credentials, scope)
