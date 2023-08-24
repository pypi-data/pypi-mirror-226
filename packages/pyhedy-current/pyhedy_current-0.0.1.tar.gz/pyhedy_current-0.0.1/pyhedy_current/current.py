import gevent
from gevent import monkey
"""打断点需要将这个补丁关掉，要不程序变成异步"""
monkey.patch_all()

def pytest_runtestloop(session):
    task = session.config.getoption("--runTask")
    count = int(session.config.getoption("--current"))
    print('参数--runTask:',task)
    print('参数--current:',count)
    print('待执行的用例总数:',len(session.items))
    if task == 'mod':
        """以模块为最小的执行单位"""
        mod_case = {}  #====> {模块:[],模块2:[]}
        """遍历所有的模块信息"""
        for item in session.items:
            """获取用例的模块信息"""
            mod = item.module
            """判断mod_case 这个字典是否又改模块"""
            if mod_case.get(mod):
                """如果有，将用例添加到模块对应的列表中"""
                mod_case[mod].append(item)
            else:
                """如果没有，将模块作为key保存到mod——case中，将值设为空列表"""
                mod_case[mod] = []
                "在将用例加入到列表中"
                mod_case[mod].append(item)
        print(mod_case.values())
        """有多少模块开多少协程"""
        gs = []
        for mod_test_case in mod_case.values():
            g = gevent.spawn(run_task,mod_test_case)
            gs.append(g)
        gevent.joinall(gs)

    else:
        """以用例为最小的执行单位"""
        case_list = session.items
        gs = []
        """根据参数创建对应数量的协程"""
        for i in range(count):
            g = gevent.spawn(run_task,case_list)
            gs.append(g)
        gevent.joinall(gs)
    return True

def run_task(items):
    """判断用例列表是否为空，"""
    while items:
        """获取一条用例"""
        item = items.pop()
        """执行用例"""
        item.ihook.pytest_runtest_protocol(item=item, nextitem=None)

def pytest_addoption(parser):
    """
    添加参数的钩子函数
    :param parser:
    :return:
    """
    """添加参数分组"""
    group = parser.getgroup("pyhedy_current")
    """添加参数和帮助信息"""
    group.addoption(
        "--runTask",
        dest="runTask",
        default=None,
        help='并发执行的任务单位',
    )
    group.addoption(
        "--current",
        dest="current",
        default=None,
        help='运行并行数量.',
    )