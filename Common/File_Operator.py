# coding =utf-8
import os
import time
import shutil
import ctypes
import traceback
import ctypes.wintypes


' A module which is used to operate files'
__author__ = 'N Sun'

class File_Operator(object):
    def format_file_path(self,path):
        # 解决windows系统下'\'的问题
        try:
            if path.find('\\') == (-1):
                return path
            else:
                path = path.replace('\\', '/')
                return path
        except Exception:
            traceback.print_exc()


    def get_latest_file(self,file_path):
        # 接收文件夹路径，返回该文件夹下最新修改的文件路径
        try:
            file_path = self.format_file_path(file_path)
            print('[Getting latest file from] ' + file_path)
            lists = os.listdir(file_path)
            lists.sort(key=lambda fn: os.path.getmtime(file_path + '/' + fn))
            latest_file_path = file_path + '/' + lists[-1]
            print('[Latest file is] ' + latest_file_path)
            return latest_file_path
        except Exception:
            traceback.print_exc()


    def copy_file(self,copyfrom, copyto):
        # 复制'copyfrom'路径（要求为单个文件）至'copyto'路径下
        try:
            shutil.copy(copyfrom, copyto)
        except Exception:
            traceback.print_exc()


    def delete_file_folder(self,dir_path):
        # 删除路径下的文件夹
        try:
            shutil.rmtree(dir_path)
            print('[Deleted] ' + dir_path)
        except Exception:
            traceback.print_exc()


    def get_all_files(self,dir_path):
        # 遍历dir_path下所有文件，包括子目录
        try:
            files = os.listdir(dir_path)
            for file in files:
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    yield file_path
                else:
                    for i in self.get_all_files(file_path):
                        yield i
        except Exception:
            traceback.print_exc()


    def get_folder_files(self,dir_path):
        # 获取dir_path下所有文件，不包括子目录
        try:
            files = os.listdir(dir_path)
            for file in files:
                yield file
        except Exception:
            traceback.print_exc()


    def list_filter(self,target_list, include_string):
        # 接收target_list,include_string，去掉target_list中不包括include_string的数据
        try:
            final_list = []
            for item in target_list:
                if include_string in item:
                    final_list.append(item)
                else:
                    pass  # 如果直接返回None会报错，只能暂且返回字符串None
            return final_list
        except Exception:
            traceback.print_exc()


    def get_relative_path(self,dir_path, relative_path_begin_location):
        # 获取相对路径和起始位置，返回根据起始位置截取后的路径（如：输入"'C:\Users\sunhaoran\test',8",输出'\sunhaoran\test'）
        try:
            return (dir_path[relative_path_begin_location:])
        except Exception:
            traceback.print_exc()


    def get_file_modify_time(self,file_path):
        # 获取文件修改时间，精确至日，格式为YYMMDD
        try:
            timestamp = os.path.getmtime(file_path)
            timestruct = time.localtime(timestamp)
            return time.strftime('%Y%m%d', timestruct)
        except Exception:
            traceback.print_exc()




    def rm(self,p):
        class LPSHFILEOPSTRUCT(ctypes.Structure):

            _fields_ = [
                ('hwnd', ctypes.wintypes.HWND),
                ('wFunc', ctypes.wintypes.UINT),
                ('pFrom', ctypes.wintypes.PCHAR),
                ('pTo', ctypes.wintypes.PCHAR),
                ('fFlags', ctypes.wintypes.INT),
                ('fAnyOperationsAborted', ctypes.wintypes.BOOL),
                ('hNameMappings', ctypes.wintypes.LPVOID),
                ('lpszProgressTitle', ctypes.wintypes.PCHAR)
            ]
        FO_DELETE = 3
        FOF_SILENT = 4
        FOF_NOCONFIRMATION = 16
        FOF_ALLOWUNDO = 64
        FOF_NOCONFIRMMKDIR = 512
        FOF_NOERRORUI = 1024
        FOF_NO_UI = FOF_SILENT | FOF_NOCONFIRMATION | FOF_NOERRORUI | FOF_NOCONFIRMMKDIR

        # 将文件移至回收站
        r = ctypes.windll.shell32.SHFileOperation(LPSHFILEOPSTRUCT(
            hwnd=0,
            wFunc=FO_DELETE,
            pFrom=ctypes.create_string_buffer(p.encode()),
            fFlags=FOF_ALLOWUNDO | FOF_NO_UI
        ))
        if r:
            raise Exception(r)


    def delete_file_which_modify_time_before(self,target_path, target_time, filter_kw1=None, filter_kw2=None):
        # 删除target_path下的修改时间早于target_time，且文件名包括filter_kw1和filter_kw2的文件
        try:
            file_list_generator = self.get_folder_files(target_path)
            file_list = []
            for n in file_list_generator:
                file_list.append(n)
            if filter_kw1 != None:
                file_list = self.list_filter(file_list, filter_kw1)
            if filter_kw2 != None:
                file_list = self.list_filter(file_list, filter_kw2)
            file_modify_time = []
            x = 0
            for x in range(len(file_list)):
                final_path = target_path + '\\' + file_list[x]
                file_modify_time.append(self.get_file_modify_time(final_path))
                if int(file_modify_time[x]) < int(target_time):
                    print(final_path)
                    self.rm(final_path)
                    print("[Deleted] " + final_path)
                else:
                    pass
        except Exception:
            traceback.print_exc()