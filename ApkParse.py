#coding=utf-8
'''
Created on 2015年5月18日

@author: hzwangzhiwei
'''

import os
import re
import zipfile

class ApkParse(object):
    '''
    DEMO
    parse = ApkParse(filename, aapt_path)
    parse = ApkParse(u'C:\\Users\\hzwangzhiwei\\Desktop\\mgapp.apk', 'D:/adt_20140321/sdk/build-tools/android-4.4.2/')
    
    print parse.name()
    print parse.package()
    print parse.version()
    print parse.icon_path()
    print parse.mv_icon_to('test_android.png')
    
    '''
    aapt_path = ''
    aapt_content = None
    
    apk_file_path = None
    
    app_version = None
    app_package = None
    app_name = None
    app_icon = None
    
    
    def __init__(self, apk_file_path, aapt_path = ''):
        '''
        Constructor
        '''
        self.aapt_path = aapt_path
        self.apk_file_path = apk_file_path
        
    
    def _get_aapt_content(self):
        self.aapt_content = os.popen(self.aapt_path + "aapt d badging " + self.apk_file_path).read()
        if self.aapt_content == None or self.aapt_content == '':
            self.aapt_content = ''
        
        print self.aapt_content
        return True
    
    
    def _try_to_parse(self):
        pack_version_success = False
        name_icon_success = False
        
        apk_pack_ver_reg = 'package\: name=\'(.*)\' (.*) versionName\=\'(.*)\''
        re_pat = re.compile(apk_pack_ver_reg)
        search_ret = re_pat.search(self.aapt_content)
        if search_ret:
            g = search_ret.groups()
            if g and len(g) == 3:
                self.app_package = g[0]
                self.app_version = g[2]
                pack_version_success = True
        
        apk_name_icon_reg = 'application\: label=\'(.*)\' icon=\'(.*)\''
        re_pat = re.compile(apk_name_icon_reg)
        search_ret = re_pat.search(self.aapt_content)
        if search_ret:
            g = search_ret.groups()
            if g and len(g) == 2:
                self.app_name = g[0]
                self.app_icon = g[1]
                name_icon_success = True
        
        return name_icon_success and pack_version_success
    
    def _check(self):
        if self.aapt_content == None:
            self._get_aapt_content()
        
        if self.app_name != None and self.app_package != None and self.app_version != None and self.app_icon != None:
            return
        
        self._try_to_parse()
        
    def name(self):
        self._check()
        return self.app_name
    
    def package(self):
        self._check()
        return self.app_package
        
    def version(self):
        self._check()
        return self.app_version
    
    def icon_path(self):
        self._check()
        return self.app_icon
    
    def mv_icon_to(self, file_name):
        icon_path = self.icon_path()
        if icon_path:
            zfile = zipfile.ZipFile(self.apk_file_path)
            
            icon_file =  open(file_name, "wb")
            icon_file.write(zfile.read(icon_path))
            icon_file.close()
            zfile.close()
            return True
        return False
    
if __name__ == '__main__':
    parse = ApkParse(u'C:\\Users\\hzwangzhiwei\\Desktop\\mgapp.apk', 'D:/adt_20140321/sdk/build-tools/android-4.4.2/')
    
    print parse.name()
    print parse.package()
    print parse.version()
    print parse.icon_path()
    print parse.mv_icon_to('test_android.png')