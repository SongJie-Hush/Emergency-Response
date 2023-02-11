import xlrd
import xlwt

def read_excel():
    # 打开文件
    workBook = xlrd.open_workbook('data/HanXueLi_201801.xlsx');
    # 获取sheet内容
    sheet1_content1 = workBook.sheet_by_index(0); # sheet索引从0开始
    # sheet的名称，行数，列数
    print(sheet1_content1.name,sheet1_content1.nrows,sheet1_content1.ncols);
    # 获取整行和整列的值（数组）

    an = "["
    # 获取单元格内容
    for i in range(sheet1_content1.nrows):
        # 判断是否存在坐标
        if sheet1_content1.cell(i,1).ctype == 0 or sheet1_content1.cell(i,2).ctype == 0:
            continue
        an = an + "{'icon':'"
        if
        for j in range(sheet1_content1.ncols):
            an = an +
    print(sheet1_content1.cell(1, 0).value);

    # 获取单元格内容的数据类型
    # Tips: python读取excel中单元格的内容返回的有5种类型 [0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error]
    print(sheet1_content1.cell(1, 0).ctype);


if __name__ == '__main__':
    read_excel();
