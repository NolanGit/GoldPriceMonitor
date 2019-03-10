# coding=utf-8
import os
import xlrd
import xlwt
import xlutils3
from xlutils3 import copy
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class Excel_Data_Controller(object):
    '''
        包括：
            create_xls：创建excel
            get_value：获取值
            get_rows_number：获取行数
            get_columns_number：获取列数
            get_values_coordinate：暴力搜索目标值，返回坐标
            set_value_by_force：将坐标位置元素暴力置为目标值
    '''

    def create_xls(self, path=os.path.dirname(__file__), excel_name='excel.xls'):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('sheet 1')
        #sheet.write(0, 0, '')
        workbook.save(excel_name)
        return excel_name

    def get_value(self, excel_file, x, y):
        '''
            输入文件地址、行、列，输出值；行、列从0开始计数
        '''
        workbook = xlrd.open_workbook(excel_file)
        sheet = workbook.sheet_by_index(0)
        try:
            result = sheet.cell(int(x), int(y)).value
            if result == "":
                return None
        except Exception:
            result = None
        return (result)

    def get_rows_number(self, excel_file):
        '''
            输入文件地址，输出行数
        '''
        x = 0
        while True:
            try:
                result = Excel_Data_Controller().get_value(excel_file, x, 0)
                x += 1
                if result == None:
                    x -= 1
                    break
            except Exception:
                print(Exception)
                break
        return x

    def get_columns_number(self, excel_file):
        '''
            输入文件地址，输出列数
        '''
        y = 0
        while True:
            try:
                result = Excel_Data_Controller().get_value(excel_file, 0, y)
                y += 1
                if result == None:
                    y -= 1
                    break
            except Exception:
                print(Exception)
                break
        return y

    def get_values_coordinate(self, excel_file, value):
        '''
            输入文件地址、搜索值，输出搜索值的坐标
        '''
        rows_number = Excel_Data_Controller().get_rows_number(excel_file)
        columns_number = Excel_Data_Controller().get_columns_number(excel_file)
        value_str = str(value)
        if value_str.isdigit():
            value_str = int(value)
        for x in range(rows_number + 1):
            for y in range(columns_number + 1):
                current_value = Excel_Data_Controller().get_value(excel_file, x, y)
                if current_value == value_str:
                    return (x, y)
        return None, None

    def set_value_by_force(self, excel_file, x, y, value):
        '''
            输入文件地址、行、列、目标值，函数会将X行X列的值置为目标值
        '''
        try:
            workbook = xlrd.open_workbook(excel_file)
            workbook = copy.copy(workbook)
            workbook.get_sheet(0).write(int(x), int(y), value)
            workbook.save(excel_file)
            return "done"
        except Exception as e:
            print(e)


'''
edc = Excel_Data_Controller()
print(edc.get_value("excel.xls", 0, 0))
'''
