import re
import json
from os import walk, path

from summers import Parser


class AnnoParser(Parser):
    """
    注解解析器 (文本解析方式)

    # 注解配置集原型(模型及样例数据)
    {
        "bookRepositoryImpl": {
            "class": "book.infra.repository.BookRepositoryImpl",
            "dependencies": {},
        },
        "mavenRepoImpl": {
            "class": "book.infra.repository.MavenRepoImpl",
            "dependencies": {},
        },
        "gitlabRepoImpl": {
            "class": "book.infra.repository.GitlabRepoImpl",
            "dependencies": {},
        },
        'bookView': {
            "class": "book.views.views_v6.BookView",
            "dependencies": {
                "book_repo": "bookRepositoryImpl",
            }
        },
        "mavenRepositoryImpl": {
            "class": "apps.book.infra.repository.repository2.MavenRepositoryImpl",
            "dependencies": {
                "mvn_api": "mavenApiImpl",
            }
        },
        'gitlabRepositoryImpl': {
            "class": "apps.book.infra.repository.repository3.GitlabRepositoryImpl",
            "dependencies": {
                "git_api": "gitlabApiImpl",
            }
        },
        'repoQueryService': {
            "class": "apps.book.domain.repository.service.RepoQueryService",
            "dependencies": {
                "mvn_repo": "mavenRepositoryImpl",
                "git_repo": "gitlabRepositoryImpl",
            }
        },
    }
    """

    @staticmethod
    def get_annotation(dir_path):
        """
        提取解析结果
        """
        ds = AnnoParser._scan(dir_path)
        conf = AnnoParser._parse(ds)

        # 唯一性校验

        return conf

    @staticmethod
    def _read_text(m_name, file):
        """
        读取文件, 获取文本内容
        """
        filepath = m_name.replace('.', '/') + '/' + file
        with open(filepath, 'r', encoding='utf-8') as f:
            ff = f.read()

        return ff

    @staticmethod
    def _scan(dir_path):
        """
        扫描文件, 获取注解集
        """
        ds = []
        for root, dirs, files in walk(dir_path):
            if '.vscode' not in root and '__' not in root and 'migrations' not in root:
                for file in files:
                    file_obj = {}
                    if '.py' in file:
                        file_path = path.join(root, file)
                        file_name = file_path[2: len(file_path) - 3].replace('/', '.').replace('\\', '.')
                        m_name = file_name[0: file_name.rfind('.')]

                        file_obj['file'] = file_name
                        file_obj['conf'] = ''

                        # 读取文本文件获取注解 (importlib.resources 仅适用于 python3.7+)
                        # txt = resources.read_text(m_name, file)  
                        txt = AnnoParser._read_text(m_name, file)
                        annotations = re.findall(r'@DI.[ \S]+|class [\w]+', txt, re.MULTILINE)

                        # 组装注解对象集
                        for anno in annotations:
                            if '__' not in anno and anno != 'classmethod':
                                if 'class' in anno:
                                    file_obj['conf'] = file_obj['conf'] + anno + "$;$"
                                else:
                                    file_obj['conf'] = file_obj['conf'] + anno
                        ds.append(file_obj)
        return ds

    @staticmethod
    def _parse(ds):
        """
        注解解析集
        """
        di_config = {}

        for ky in ds:
            cls_conf = ky['conf']
            if cls_conf != '' and '@' in cls_conf:
                # print("文件", ky['file'])
                cls_list = cls_conf.split("$;$")
                for cls_str in cls_list:
                    if cls_str != '':
                        cls_str = cls_str.replace('"', "'")
                        try:
                            c_name = re.findall(r'class\s\w+', cls_str)[0].split("class ")[1]
                            f_name = ky['file'] + '.' + c_name
                            if 'name' in cls_str:
                                alias = re.findall(r'name=["\']\w+', cls_str)[0].split("='")[1]
                            else:
                                alias = c_name
                        except Exception as err:
                            print("解析_ERR", err)
                        finally:
                            # 唯一性校验
                            if alias in di_config.keys():
                                raise Exception("类别名存在重复定义, 请检查和修改别名", alias, f_name)

                            di_config[alias] = {"class": f_name}

        print("注解扫描结果", json.dumps(di_config, indent=4, ensure_ascii=False, sort_keys=True))
        return di_config
