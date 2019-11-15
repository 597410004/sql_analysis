# encoding=utf-8
# 解析sql并取出字段名,字段类型和中文注释
import regex as re
import xlwt


def get_field(read_path, write_path):
    global sheet
    col = 0
    value_title = ["表名", "字段名", "字段类型", "字段注释", "字段长度"]
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('表结构')
    for i in range(len(value_title)):
        sheet.write(0, i, value_title[i])
    with open(read_path, encoding='utf-8') as f:
        contents = f.readlines()
        for content in contents:
            content_list = []
            table_name = re.search(r"(?<==').*?(?=')", content)
            field = re.search(r'(?<=`).*?(?=`)', content)
            type = re.search(r'(?<=`\s+)[a-z]+(?=\(|\s+)', content)
            comment = re.search(r"(?<=COMMENT\s').*?(?=')", content)
            conten_len = re.search(r"(?<=\()[0-9]+(?=\))", content)
            if table_name is not None:
                content_list.append(table_name.group())
            else:
                content_list.append('')
            if field is not None:
                if 'Key' not in field.group():
                    content_list.append(field.group())
            else:
                content_list.append('')
            if type is not None:
                content_list.append(type.group())
            else:
                content_list.append('')
            if comment is not None:
                content_list.append(comment.group())
            else:
                content_list.append('')
            if conten_len is not None:
                content_list.append(conten_len.group())
            elif 'datetime' in content or 'timestamp' in content:
                content_list.append(0)
            else:
                content_list.append('')
            a = list(filter(is_none, content_list))
            if a:
                col = col + 1
                for i in range(len(content_list)):
                    sheet.write(col, i, content_list[i])
    workbook.save(write_path)


def is_none(n):
    return n != ''


if __name__ == '__main__':
    get_field('sql.txt', 'test.xls')
