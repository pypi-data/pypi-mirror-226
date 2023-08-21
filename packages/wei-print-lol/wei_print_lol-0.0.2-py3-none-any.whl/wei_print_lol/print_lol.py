def print_lol(the_list):
    """
    打印列表的每一项，各项单独占一行，列表可以是嵌套列表
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)


def print_lol2(msg):
    """
    测试打印
    """
    print(f'{msg}')
