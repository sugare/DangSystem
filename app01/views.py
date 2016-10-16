from django.http.response import HttpResponse, HttpResponseRedirect
from app01.models import single, multi, judge, rec, mask, survey_data, survey_choice
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import xlrd, random, xlwt, os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

def index_aa(request):      # 登录首页
    return render(request, 'index.html')

def up_users():         # 上传用户
    data = xlrd.open_workbook(r'C:\Users\song\Desktop\info\list1.xls')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    for i in (range(1, nrows + 1)):
        User.objects.create(id=i, username=str(int(table.row_values(i - 1)[0])),
                            password=make_password(str(int(table.row_values(i - 1)[1])), None, 'pbkdf2_sha256'),
                            first_name=table.row_values(i - 1)[2])
    return HttpResponse("upusers successful!")

def up_single_data():       # 上传单选题
    data = xlrd.open_workbook(r'C:\Users\song\Desktop\info\singe.xlsx')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    for i in (range(1, nrows + 1)):
        if table.row_values(i - 1)[5] == 'A':
            mask = ord('A') - 64
        elif table.row_values(i - 1)[5] == 'B':
            mask = ord('B') - 64
        elif table.row_values(i - 1)[5] == 'C':
            mask = ord('C') - 63
        elif table.row_values(i - 1)[5] == 'D':
            mask = ord('D') - 60
        q = single.objects.create(id=i, content=table.row_values(i - 1)[0], question_ans=mask)
        for j in range(1, 5):
            if j == 1:
                q.sin_ans_set.create(content=table.row_values(i - 1)[j], mask=1)
            elif j == 2:
                q.sin_ans_set.create(content=table.row_values(i - 1)[j], mask=2)
            elif j == 3:
                q.sin_ans_set.create(content=table.row_values(i - 1)[j], mask=4)
            elif j == 4:
                q.sin_ans_set.create(content=table.row_values(i - 1)[j], mask=8)
    #return HttpResponse('insert single successful!')

def up_multi_data():       # 上传多选题
    data = xlrd.open_workbook(r'C:\Users\song\Desktop\info\multi.xlsx')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    for i in (range(1, nrows + 1)):
        if table.row_values(i - 1)[5] == 'AB':
            mask = 3
        if table.row_values(i - 1)[5] == 'AC':
            mask = 5
        if table.row_values(i - 1)[5] == 'AD':
            mask = 9
        if table.row_values(i - 1)[5] == 'BC':
            mask = 6
        if table.row_values(i - 1)[5] == 'BD':
            mask = 10
        if table.row_values(i - 1)[5] == 'CD':
            mask = 12
        if table.row_values(i - 1)[5] == 'ABC':
            mask = 7
        if table.row_values(i - 1)[5] == 'ABD':
            mask = 11
        if table.row_values(i - 1)[5] == 'ACD':
            mask = 13
        if table.row_values(i - 1)[5] == 'BCD':
            mask = 14
        if table.row_values(i - 1)[5] == 'ABCD':
            mask = 15

        q = multi.objects.create(id=i, content=table.row_values(i - 1)[0], question_ans=mask)
        for j in range(1, 5):
            if j == 1:
                q.mul_ans_set.create(content=table.row_values(i - 1)[j], mask=1)
            elif j == 2:
                q.mul_ans_set.create(content=table.row_values(i - 1)[j], mask=2)
            elif j == 3:
                q.mul_ans_set.create(content=table.row_values(i - 1)[j], mask=4)
            elif j == 4:
                q.mul_ans_set.create(content=table.row_values(i - 1)[j], mask=8)

    #return HttpResponse('insert multi successful!')

def up_judge_data():       # 上传判断题
    data = xlrd.open_workbook(r'C:\Users\song\Desktop\info\judge.xlsx')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    for i in (range(1, nrows + 1)):
        if table.row_values(i - 1)[1] == 'A':
            mask = 1  # 1 right
        elif table.row_values(i - 1)[1] == 'B':
            mask = 0  # error

        judge.objects.create(id=i, content=table.row_values(i - 1)[0], question_ans=mask)

    #return HttpResponse('insert judge successful!')

def upsurvey():      # 上传调查问卷
    data = xlrd.open_workbook(r'C:\Users\song\Desktop\info\fujia.xls')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    for i in range(5, 10):
        survey_data.objects.create(content=table.row_values(i)[1])

    for j in range(1, 6):
        q = survey_data.objects.get(pk=j)
        q.survey_choice_set.create(choice_text='非常满意', mask=1)
        q.survey_choice_set.create(choice_text='满意', mask=2)
        q.survey_choice_set.create(choice_text='比较满意', mask=3)
        q.survey_choice_set.create(choice_text='一般', mask=4)
        q.survey_choice_set.create(choice_text='不满意', mask=5)
    #return HttpResponse('ok')

def updata(request):        # 将数据导入数据库
    upuser = up_users()
    single = up_single_data()
    multi = up_multi_data()
    judge = up_judge_data()
    survey = upsurvey()
    return HttpResponse('OK')

def acc_login(request):     # 用户登录
    # print(request.POST.get('username'))
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # if rec.objects.filter(user_id=username).count() == 0:
        # u = User.objects.get(username=username)
        if User.objects.filter(username=username).count() == 0 or User.objects.get(
                username=username).rec_set.all().count() == 0:
            '''
            li = []
            for i in rec.objects.all().iterator():
                li.append(i)
            print(username in li)
            '''
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/exam/')
            else:
                return render(request, 'login.html', {'login_err': "Wrong username or password "})
        else:
            return render(request, 'login.html', {'login_err': "You have already submitted papers"})
    else:
        return render(request, 'login.html')

@login_required
def acc_logout(request):    # 用户退出
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

@login_required
def exam(request):      # 考试页面
    qid = []
    for q in range(1, 61):
        qid.append(q)
    random.shuffle(qid)
    c = qid[:20]
    squestion_list = []
    mquestion_list = []
    for i in c:
        a = single.objects.get(pk=i)
        squestion_list.append(a)
        b = multi.objects.get(pk=i)
        mquestion_list.append(b)

    pid = []
    for p in range(1, 31):
        pid.append(p)
    random.shuffle(pid)
    d = pid[:10]
    jquestion_list = []
    for j in d:
        c = judge.objects.get(pk=j)
        jquestion_list.append(c)
    slen = range(1, 21)
    mlen = len(mquestion_list)
    jlen = len(jquestion_list)
    content = {'squestion_list': squestion_list, 'mquestion_list': mquestion_list, 'jquestion_list': jquestion_list,
               'slen': slen, 'mlen': mlen, 'jlen': jlen}
    return render(request, 'exam.html', content)

@login_required
def submit(request):        # 提交考生答案到数据库
    a = request.POST
    user_id = a.getlist('user_id')[0]
    user_set = User.objects.get(username=user_id)
    b = list(a)

    if rec.objects.filter(username_id=user_set.id).count() == 0:
        for i in b:
            if i != 'csrfmiddlewaretoken' and i != 'user_id':
                # print(a.getlist(i))
                # print(a)
                d = a.getlist(i)
                chen = 0
                for j in d:
                    chen += int(j)
                # if rec.objects.filter(username_id=user_set.id).count() == 0:
                user_set.rec_set.create(question_id=i, user_rec=chen)
    else:
        return HttpResponse('you already submit!')
    return HttpResponseRedirect('/survey/')

def survey(request):        # 展示调查问卷
    sid = []
    for q in range(1, 6):
        sid.append(q)
    random.shuffle(sid)

    s_list = []
    for i in sid:
        a = survey_data.objects.get(pk=i)
        s_list.append(a)

    # print(s_list)
    return render(request, 'survey.html', {'question': s_list, 'q0':s_list[0], 'q1':s_list[1],'q2':s_list[2],'q3':s_list[3],'q4':s_list[4]})

def surveydata(request):        # 记录调查数据
    a = request.POST
    print(a)
    '''
    print(a.lists)
    print(type(a.get('6',str(1))))

    ['appendlist', 'clear', 'copy', 'dict', 'encoding', 'fromkeys', 'get',
    'getlist', 'items', 'keys', 'lists', 'pop', 'popitem', 'setdefault',
    'setlist', 'setlistdefault', 'update', 'urlencode', 'values']
    '''
    for i in range(1, 6):
        #print(type(int(str(i))))
        q = survey_data.objects.get(pk=i)
        #print(int(a.get(str(i))))

        selected_choice = q.survey_choice_set.get(mask=int(a.get(str(i), str(i))))
        if a.get(str(i), 6) == 6:
            selected_choice.votes += 0
            selected_choice.save()
        else:
            selected_choice.votes += 1
            selected_choice.save()

    return render(request, 'game1.html')

def cul_mask(request):  # 计算总成绩
    a = rec.objects.all()
    # print(a)
    b = []
    for i in a:
        b.append(i.username_id)

    c = set(b)
    # print(c)
    for i in c:
        d = User.objects.get(pk=i)

        s = d.rec_set.all().filter(question_id__startswith='s')
        s_ma = 0
        for j in range(s.count()):
            if int(s.values_list()[j][3]) == single.objects.get(pk=int(s.values_list()[j][2][1:3])).question_ans:
                s_ma += 2
        # print(s_ma)

        m = d.rec_set.all().filter(question_id__startswith='m')
        m_ma = 0
        for j in range(m.count()):
            if int(m.values_list()[j][3]) == multi.objects.get(pk=int(m.values_list()[j][2][1:3])).question_ans:
                m_ma += 2
        # print(m_ma)
        u = d.rec_set.all().filter(question_id__startswith='j')
        j_ma = 0
        for j in range(u.count()):

            if int(u.values_list()[j][3]) == judge.objects.get(pk=int(u.values_list()[j][2][1:3])).question_ans:
                j_ma += 1
        # print(j_ma)

        total = s_ma + m_ma + j_ma
        if mask.objects.filter(user_id=d.username).count() == 0:
            mask.objects.create(user_id=d.username, username=d.first_name, s_mask=s_ma, m_mask=m_ma, j_mask=j_ma,
                                total=total)
    return render(request, 'download.html')

def download_mask(request):     # 下载成绩单
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('results', cell_overwrite_ok=True)

    sheet2 = workbook.add_sheet('survey', cell_overwrite_ok=True)
    sheet2.write(0, 0, '问题\选项')
    sheet2.write(0, 1, 'A.非常满意')
    sheet2.write(0, 2, 'B.满意')
    sheet2.write(0, 3, 'C.比较满意')
    sheet2.write(0, 4, 'D.一般')
    sheet2.write(0, 5, 'E.不满意')
    for i in range(1, 6):
        a = survey_data.objects.get(pk=i)
        sheet2.write(i, 0, a.content)
        for j in range(1, 6):
            sheet2.write(i, j, a.survey_choice_set.get(mask=j).votes)

    sheet1.write(0, 0, 'student_id')
    sheet1.write(0, 1, 'name')
    sheet1.write(0, 2, 'single')
    sheet1.write(0, 3, 'multi')
    sheet1.write(0, 4, 'judge')
    sheet1.write(0, 5, 'total')
    for i in range(1, mask.objects.all().count() + 1):
        sheet1.write(i, 0, mask.objects.get(pk=i).user_id)
        sheet1.write(i, 1, mask.objects.get(pk=i).username)
        sheet1.write(i, 2, mask.objects.get(pk=i).s_mask)
        sheet1.write(i, 3, mask.objects.get(pk=i).m_mask)
        sheet1.write(i, 4, mask.objects.get(pk=i).j_mask)
        sheet1.write(i, 5, mask.objects.get(pk=i).total)
    # workbook.save(r'C:\Users\song\Desktop\dang\mask.xls')
    response = HttpResponse(content_type='application/msexcel')
    response['Content-Disposition'] = 'attachment; filename=results.xls'
    workbook.save(response)
    return response

def upload(request):        # 上传页面
    return render(request, 'upload.html')

def upload_file(request):       # 上传文件
    if request.method == "POST":    # 请求方法为POST时，进行处理
        print(request.POST)
        myFile = request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join(r"C:\Users\song\Desktop\info",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        #destination = open(/static/, myFile.name, 'wb+')
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse('OK')
