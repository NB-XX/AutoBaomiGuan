import json
import random

# 假设你的JSON字符串保存在变量 json_str 中
json_str = '''[{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1ff622309\",\"resultFlag\":0,\"standardAnswer\":\"C\",\"subCount\":0,\"tqId\":52,\"userAnswer\":\"C\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d22a3d23a9\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":92,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d20904232d\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":61,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1e0c02295\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":23,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1f2b222d9\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":40,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1ef8522cd\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":37,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d225d22399\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":88,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1e2d9229d\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":25,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1e93622b5\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":31,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1c988223d\",\"resultFlag\":0,\"standardAnswer\":\"C\",\"subCount\":0,\"tqId\":1,\"userAnswer\":\"C\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1cec62251\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":6,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1e1cc2299\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":24,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d217ea2365\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":75,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1ca992241\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":2,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1f4d222e1\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":42,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d215cb235d\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":73,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1eb4e22bd\",\"resultFlag\":0,\"standardAnswer\":\"C\",\"subCount\":0,\"tqId\":33,\"userAnswer\":\"C\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d1d40b2265\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":11,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d205d32321\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":58,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d22704239d\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":89,\"userAnswer\":\"D\",\"userScoreRate\":\"0%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d23a4f23e5\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":107,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":3},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d24c872429\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":124,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":3},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d25cd02465\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":139,\"userAnswer\":\"B\",\"userScoreRate\":\"0%\",\"viewTypeId\":3},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d2657b2485\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":147,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":3},{\"parentId\":\"0\",\"qstId\":\"8ad5a748932edc96019631d24b742425\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":123,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":3}]'''

# 将 JSON 字符串转换为 Python 对象
questions = json.loads(json_str)

def randomize_answers(questions):
    options = ['A', 'B', 'C', 'D']
    new_questions = []

    for q in questions:
        # 随机决定是否答对（92% 概率）
        should_be_correct = random.random() > 0.08
        new_q = q.copy()

        if should_be_correct:
            new_q['userAnswer'] = new_q['standardAnswer']
            new_q['userScoreRate'] = '100%'
        else:
            wrong_options = [opt for opt in options if opt != new_q['standardAnswer']]
            new_q['userAnswer'] = random.choice(wrong_options)
            new_q['userScoreRate'] = '0%'

        new_questions.append(new_q)

    return new_questions


def get_answer():
    
    regenerate = True

    while regenerate:
        randomized_data = randomize_answers(questions)
        correct_count = sum(1 for q in randomized_data if q['userScoreRate'] == '100%')
        score = correct_count * 4
        a = eval(input('当前分数为' + str(score) + '是否上传？ 1.上传 2.重新生成 :'))
        if a == 1:
            regenerate = False

    return str(randomized_data)

