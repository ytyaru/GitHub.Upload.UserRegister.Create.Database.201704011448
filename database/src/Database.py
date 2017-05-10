#!python3
#encoding:utf-8
import configparser
import dataset
import database.src.language.insert.Main
import database.src.api.Main
import database.src.gnu_license.create.Main
import database.src.gnu_license.insert.main
import database.src.license.insert.Main
import database.src.other_repo.insert.Main
import database.src.account.Main
import database.src.repo.insert.Main

class Database:
    def __init__(self):
        self.files = {
            'lang': 'GitHub.Languages.sqlite3',
            'api': 'GitHub.Apis.sqlite3',
            'gnu_license': 'GNU.Licenses.sqlite3',
            'account': 'GitHub.Accounts.sqlite3',
            'license': 'GitHub.Licenses.sqlite3',
            'other_repo': 'GitHub.Repositories.__other__.sqlite3',
            'repo': 'GitHub.Repositories.{user}.sqlite3',
        }        
        self.lang = None
        self.api = None
        self.gnu_license = None
        self.account = None
        self.other_repo = None
        self.repo = None
        
    # 1. 全DBのファイルパス作成
    # 2. マスターDBファイルがないなら
    # 2-1. マスターDBファイル作成
    # 2-2. マスターDBデータ挿入
    # 3. アカウントDBがないなら
    # 3-1. アカウントDBファイル作成
    def Initialize(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        print(config['Path']['DB'])
        print(os.path.abspath(config['Path']['DB']))
        self.dir_db = os.path.abspath(config['Path']['DB'])
        for key in self.files.keys():
            self.files[key] = os.path.join(self.dir_db, self.files[key])
        """
        self.files['lang'] = os.path.join(self.dir_db, self.files['lang'])
        self.files['api'] = os.path.join(self.dir_db, self.files['api'])
        self.files['gnu_license'] = os.path.join(self.dir_db, self.files['gnu_license'])
        self.files['account'] = os.path.join(self.dir_db, self.files['account'])
        self.files['license'] = os.path.join(self.dir_db, self.files['license'])
        self.files['other_repo'] = os.path.join(self.dir_db, self.files['other_repo'])
        self.files['repo'] = os.path.join(self.dir_db, self.files['repo'])
        """
        self.__OpenDb()

    def __OpenDb(self):
        # マスターDB生成（ファイル、テーブル、データ挿入）
        if None is self.lang:
            if not os.path.isfile(self.files['lang']):
                m = database.src.language.Main.Main(self.files['lang'])
                m.Run()
            self.account = dataset.connect('sqlite:///' + self.files['lang'])
        if None is self.api:
            self.api = dataset.connect('sqlite:///' + self.files['api'])
            if not os.path.isfile(self.files['api']):
                m = database.src.api.Main.Main(self.files['api'])
                m.Run()
            self.api = dataset.connect('sqlite:///' + self.files['api'])
        if None is self.gnu_license:
            self.gnu_license = dataset.connect('sqlite:///' + self.files['gnu_license'])
            if not os.path.isfile(self.files['gnu_license']):
                m = database.src.gnu_license.Main.Main(self.files['gnu_license'])
                m.Run()
            self.gnu_license = dataset.connect('sqlite:///' + self.files['gnu_license'])

        # アカウントDB生成（ファイル、テーブル作成。データ挿入はCUIにて行う）
        if None is self.account:
            self.account = dataset.connect('sqlite:///' + self.files['account'])
            if not os.path.isfile(self.files['account']):
                m = database.src.account.Main.Main(self.files['account'])
                m.Create()
            self.account = dataset.connect('sqlite:///' + self.files['account'])

        # DB作成にTokenが必要なもの
        if 0 < self.account['Accounts'].count()
            # ライセンスDB生成（ファイル、テーブル作成。データ挿入）
            if None is self.gnu_license and os.path.isfile(self.files['gnu_license'])):
                # アカウント情報をどうやって渡すか
#                m = database.src.license.Main.Main(self.files['gnu_license'])
#                m.Run()
                pass
            # 他者リポジトリDB生成（ファイル、テーブル作成。データ挿入）
            if None is self.repos:
                self.repos = {}
            for account in self.account['Accounts'].find():
                self.__OpenRepo(account['Username'])

    def __OpenRepo(self, username):
        if not(username in self.repos):
            path = self.files['repo'].replace('{user}', username)
            if None is self.repos and os.path.isfile(path):
                self.repos[username] = dataset.connect('sqlite:///' + path)
                # アカウント情報をどうやって渡すか
#                m = database.src.repo.Main.Main(path)
#                m.Run()

