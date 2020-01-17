import xlrd
import datetime
import shutil
import time
import os


class Excel_operation():

    def __init__(self,pathname):
        self.pathname = pathname


    # 从指定目录中搜索并返回xlsx文件列表
    def get_xlsx_list(self, pending_dir='pending'):
        res = []
        pending_path = os.path.join(self.pathname, pending_dir)
        for dirpath, dirname, filenames in os.walk(pending_path):
            for filename in filenames:
                if not filename.startswith('~$'):
                    extension = os.path.splitext(filename)[1]
                    if extension in ('.xlsx','.csv','.xls'):
                        res.append(os.path.join(dirpath, filename))
        return res

    # 将已处理的文件改名并存入sloved文件夹
    def solved_backup(self, path_file, target_dir='solved'):
        extension = os.path.splitext(path_file)[1]
        new_name = os.path.join(os.path.split(path_file)[0], os.path.splitext(path_file)[0]+'-'+str(int(round(time.time()*1000)))+extension)
        os.rename(path_file, os.path.join(path_file, new_name))
        path_solved = os.path.join(self.pathname, target_dir)
        if not os.path.exists(path_solved):
            os.mkdir(path_solved)
        shutil.move(new_name,path_solved)
        return new_name

    #按行读取内容
    def read_by_row(self, file_path, sheet_num=0, data_only=True):
        results = []
        wb = xlrd.open_workbook(file_path)
        for sheet in wb.sheets():
            nrow = sheet.nrows
            for i in range(nrow):
                data_one_row = []
                for _ in sheet.row_values(i, start_colx=0, end_colx=None):
                    data_one_row.append(_.strip())
                data_one_row.append(datetime.date.today())
                results.append(data_one_row)

        return results


    # #按行写入所有
    # def write_by_rows(self,filename,sheet_name,datas):
    #     wb = Workbook()
    #     index = 0
    #     wb.create_sheet(sheet_name, index=index)
    #     sheet = wb[sheet_name]
    #     for row in datas:
    #         sheet.append(row)
    #     wb.save(os.path.join(self.pathname,filename))






