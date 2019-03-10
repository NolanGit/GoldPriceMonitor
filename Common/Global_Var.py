# coding=utf-8
import sys
import xlrd
sys.path.append('../')
sys.path.append('../../')
from Common.Excel_Editor import Excel_Data_Controller

__author__ = 'sunhaoran'


class Global_Var(object):

    def __init__(self, excel_name='excel.xls'):
        self.excel_data_controller = Excel_Data_Controller()
        try:
            self.excel_name = excel_name
            xlrd.open_workbook(self.excel_name)
        except:
            print("created new excel called \"" + excel_name + "\"")
            self.create_xls(excel_name)

    def create_xls(self, excel_name):
        self.excel_name = self.excel_data_controller.create_xls(excel_name=excel_name)

    def set_value(self, name, value):
        x, y = self.excel_data_controller.get_values_coordinate(self.excel_name, name)
        if x == None and y == None:
            x = self.excel_data_controller.get_rows_number(self.excel_name)
            self.excel_data_controller.set_value_by_force(self.excel_name, x, 0, name)
            self.excel_data_controller.set_value_by_force(self.excel_name, x, 1, value)
        else:
            self.excel_data_controller.set_value_by_force(self.excel_name, x, 1, value)
        print("[%s,%s]has been saved to row %s" % (name, value, x))

    def get_value(self, name):
        x, y = self.excel_data_controller.get_values_coordinate(self.excel_name, name)
        if x == None and y == None:
            return "None"
        else:
            y += 1
            result = self.excel_data_controller.get_value(self.excel_name, x, y)
            return result


'''
gv = Global_Var()
gv.set_value('abc', 1)
gv.set_value('bcd', 2)
gv.set_value('cde', 3)
result = gv.get_value('abc')
print(result)
result = gv.get_value('bcd')
print(result)
result = gv.get_value('cde')
print(result)
gv.set_value('cde', 4)
result = gv.get_value('cde')
print(result)
'''