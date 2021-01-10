# -*- coding: utf-8 -*-


def input_course_id(course_count):
    selected_course_id = 0
    while True:
        str_input = input("请根据课程中序号，选择你要打开的课程网页: ")
        try:
            if int(str_input) == 0:
                print('已关闭课程输入......')
                return selected_course_id
            elif 0 < int(str_input) < course_count:
                selected_course_id = int(str_input)
                break
            else:
                print('未按照要求输入......(提示:仅能输入单一课程序号)')
                continue
        except ValueError:
            print('输入的字符有误......(提示:仅能输入数字)')
            continue
    return selected_course_id


def input_selected_course_id(index_of_selected_course_handle, selected_course_handles_dict):
    for selected_course in selected_course_handles_dict:
        print("\n******课程序号: " + str(
            selected_course_handles_dict[selected_course]) + ' | 课程名称:' + selected_course + "******\n")
    selected_course_id = 0
    while True:
        str_input = input("请根据课程中序号，选择你要打开的课程网页: ")
        try:
            if 0 <= int(str_input) <= index_of_selected_course_handle:
                selected_course_id = int(str_input)
                break
            else:
                print('未按照要求输入......(提示:仅能输入单一课程序号)')
                continue
        except ValueError:
            print('输入的字符有误......(提示:仅能输入数字)')
            continue
    return selected_course_id


def input_stu_card_id(stu_cards_count):
    selected_stu_cards_id = 0
    while True:
        str_input = input("请根据课程中序号，选择你要打开的课程网页: ")
        try:
            if 0 < int(str_input) < stu_cards_count:
                selected_stu_cards_id = int(str_input)
                break
            else:
                print('未按照要求输入......(提示:仅能输入单一课程序号)')
                continue
        except ValueError:
            print('输入的字符有误......(提示:仅能输入数字)')
            continue
    return selected_stu_cards_id
