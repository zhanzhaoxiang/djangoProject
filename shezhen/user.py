import os
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from functools import reduce

import researchrel

top = tkinter.Tk()  # 创建主窗口
top.title('舌诊')  # 窗口标题
top.geometry('600x500')  # 窗口大小

# 实例化标签
label = tkinter.Label(top, text='舌诊', font=('Arial', 20), height=1, width=20)
label.pack()  # 将标签加入窗口

frm = Frame(top)

label = tkinter.Label(top, text='症状', font=('Arial', 15), height=1, width=10)
label.place(x=190, y=50, anchor='w')

label = tkinter.Label(top, text='选择', font=('Arial', 15), height=1, width=10)
label.place(x=300, y=50, anchor='w')

label = tkinter.Label(top, text='舌质颜色：', font=('Arial', 15), height=1, width=10)
label.place(x=200, y=80, anchor='w')

cmb_1 = ttk.Combobox(top, font=('Arial', 14), height=1, width=10, state="readonly")
cmb_1['value'] = ('淡白', '淡红', '红绛', '青紫')
cmb_1.place(x=320, y=80, anchor='w')

label = tkinter.Label(top, text='舌质老嫩：', font=('Arial', 15), height=1, width=10)
label.place(x=200, y=110, anchor='w')

cmb_2 = ttk.Combobox(top, state="readonly", font=('Arial', 14), height=1, width=10)
cmb_2['value'] = ('嫩', '老', '适中')
cmb_2.place(x=320, y=110, anchor='w')

label = tkinter.Label(top, text='舌质胖瘦：', font=('Arial', 15), height=1, width=10)
label.place(x=200, y=140, anchor='w')

cmb_3 = ttk.Combobox(top, state="readonly", font=('Arial', 14), height=1, width=10)
cmb_3['value'] = ('胖', '瘦', '适中')
cmb_3.place(x=320, y=140, anchor='w')

label = tkinter.Label(top, text='舌苔颜色：', font=('Arial', 15), height=1, width=10)
label.place(x=200, y=170, anchor='w')

cmb_4 = ttk.Combobox(top, state="readonly", font=('Arial', 14), height=1, width=10)
cmb_4['value'] = ('白苔', '黄苔', '灰黑苔')
cmb_4.place(x=320, y=170, anchor='w')

label = tkinter.Label(top, text='舌苔厚薄：', font=('Arial', 15), height=1, width=10)
label.place(x=200, y=200, anchor='w')

cmb_5 = ttk.Combobox(top, state="readonly", font=('Arial', 14), height=1, width=10)
cmb_5['value'] = ('光剥无苔', '少苔', '薄苔', '厚苔')
cmb_5.place(x=320, y=200, anchor='w')

label = tkinter.Label(top, text='津液：', font=('Arial', 15), height=1, width=10)
label.place(x=200, y=230, anchor='w')

cmb_6 = ttk.Combobox(top, state="readonly", font=('Arial', 14), height=1, width=10)
cmb_6['value'] = ('润苔', '湿滑苔', '干燥', '燥糙苔', '垢腻苔')
cmb_6.place(x=320, y=230, anchor='w')


def submit():
    temp = []
    for i in [cmb_1, cmb_2, cmb_3, cmb_4, cmb_5, cmb_6]:
        if i.get():
            temp.append(i.get())
        else:
            temp.append('')
    print(temp)
    return temp


# 查询
def search_rel(graph):
    # 输入症状，特征查询
    # while True:
    # 对有这类症状的疾病查询
    labels = ['舌质颜色', '舌质老嫩', '舌质胖瘦', '舌苔颜色', '舌苔厚薄', '津液']
    des = ['舌质颜色(淡白，淡红，红绛，青紫)', '舌质老嫩(嫩，老，适中)', '舌质胖瘦(胖，瘦，适中)', '舌苔颜色(白苔，黄苔，灰黑苔)', '舌苔厚薄(光剥无苔，少苔，薄苔，厚苔)',
           '津液(润苔，湿滑苔，干燥，燥糙苔，垢腻苔)']
    relations = ['disease_tongue_colors', 'disease_tongue_actives', 'disease_tongue_sizes',
                 'disease_coating_colors',
                 'disease_coating_sizes', 'disease_fluids']
    # symptom= [input('请输入{}：'.format(i)) for i in des]

    symptom = submit()
    if len(set(symptom)) != 1:
        print(symptom)
        answer = []
        answers = []  # 每个条件的结果
        # sql查询
        for i in range(len(symptom)):
            if symptom[i]:
                answers.append(graph.run(
                    "MATCH (m:{0})-[r:{1}]-(n:临床意义) where m.name='{2}' return n.name".format(labels[i], relations[i],
                                                                                             symptom[i])).data()
                               )
        for i in range(len(answers)):
            answer.append({str(i['n.name']) for i in answers[i]})
        # print(answer)
        final_answer = reduce(lambda x, y: x & y, answer)  # 对查询结果取交集
        # print(final_answer)
        if final_answer == set():  # 若结果为空，则提示询问医生
            final_answer = {'无结果，请询问医生'}
        # final_answer = '症状：{0}，可能染上的疾病有：{1}'.format('，'.join(symptom), '；'.join(list(final_answer)))
        # print(list(final_answer))
        return list(final_answer)
    else:
        return '0'


def result_show():
    text.delete(1.0, END)
    temp = search_rel(researchrel.rel_neo4j())
    # print(temp)
    for i in temp:
        text.insert(tkinter.END, i + "\n")


button = tkinter.Button(top, command=result_show, text='提交', font=('Arial', 15), height=1, width=6)
button.place(x=250, y=280, anchor='w')


def exits():
    exit()


button = tkinter.Button(top, command=exits, text='退出', font=('Arial', 15), height=1, width=6)
button.place(x=350, y=280, anchor='w')

label = tkinter.Label(top, text='结果', font=('Arial', 15), height=1, width=6)
label.place(x=170, y=320, anchor='w')

text = tkinter.Text(top, font=('Arial', 15), height=6, width=35, fg='blue', selectbackground='black',
                    selectforeground='gray', state="normal")  # 多行文本框
text.place(x=150, y=400, anchor='w')

frm.pack()
top.mainloop()
