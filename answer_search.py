from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474",auth=("neo4j","123456"))
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                final_answer = self.answer_prettify(question_type, ress)
                if final_answer:
                    final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answer):
        final_answer = []
        if not answer:
            return ''
        if question_type == 'zhongyao_pinyin':
            desc = answer[0]['m.pinyin']
            subject = answer[0]['m.name']
            final_answer = '{0}的拼音是:{1}'.format(subject, desc)

        elif question_type == 'zhongyao_othername':
            desc = "、".join(answer[0]['m.othername'])
            subject = answer[0]['m.name']
            final_answer = '{0}的别名有：{1}'.format(subject, desc)

        elif question_type == 'zhongyao_resource':
            desc = answer[0]['m.resource']
            subject = answer[0]['m.name']
            final_answer = '{0}的药材基源有：{1}'.format(subject, desc)

        elif question_type == 'zhongyao_latin':
            desc = answer[0]['m.latin']
            subject = answer[0]['m.name']
            final_answer = '{0}的拉丁文有：{1}'.format(subject, desc)

        elif question_type == 'zhongyao_collect':
            desc = answer[0]['m.collect']
            subject = answer[0]['m.name']
            final_answer = '{0}的采集和存储方法有：{1}'.format(subject, desc)

        elif question_type == 'zhongyao_environment':
            desc = answer[0]['m.environment']
            subject = answer[0]['m.name']
            final_answer = '{0}的生长环境是：{1}'.format(subject, desc)

        elif question_type == 'zhongyao_taste':
            desc = answer[0]['m.taste']
            subject = answer[0]['m.name']
            final_answer = '{0}的性味是：{1}'.format(subject, desc)

        elif question_type == 'zhongyao_howtouse':
            desc = answer[0]['m.howtouse']
            subject = answer[0]['m.name']
            final_answer = '{0}的用法用量是：{1}'.format(subject, desc)



        elif question_type == 'zhongyao_desc':
            desc = dict(answer[0])
            final_answer="\n"
            for j in desc.items():
                for i in j[1].items():
                    content = i[1]
                    if i[0] == "othername":
                        content = "、".join(i[1])
                    final_answer += "{0}:{1}".format(i[0], content) + "\n"

        elif question_type == 'zhongyao_cure':
            desc = [i['n.name'] for i in answer]
            subject = answer[0]['m.name']
            final_answer = '{0}主治有：{1}'.format(subject,'、'.join(desc))

        elif question_type == 'zhongyao_book':
            desc = [i['n.name'] for i in answer]
            subject = answer[0]['m.name']
            final_answer = '{0}摘录于：{1}'.format(subject, '、'.join(desc))

        elif question_type == 'zhongyao_function':
            desc = [i['n.name'] for i in answer]
            subject = answer[0]['m.name']
            final_answer = '{0}功能有：{1}'.format(subject, '、'.join(desc))

        elif question_type == 'zhongyao_area':
            desc = [i['n.name'] for i in answer]
            subject = answer[0]['m.name']
            final_answer = '{0}分布地点有：{1}'.format(subject, '、'.join(desc))

        elif question_type == 'function_zhongyao':
            desc = [i['m.name'] for i in answer]
            subject = answer[0]['n.name']
            final_answer = '想要{0}可以吃的中药有：{1}'.format(subject,'、'.join(desc))

        elif question_type == 'cure_zhongyao':
            desc = [i['m.name'] for i in answer]
            subject = answer[0]['n.name']
            final_answer = '患有{0}可以吃的中药有：{1}'.format(subject,'、'.join(desc))

        elif question_type == 'book_zhongyao':
            desc = [i['m.name'] for i in answer]
            subject = answer[0]['n.name']
            final_answer = '摘录于《{0}》的中药有：{1}'.format(subject,'、'.join(desc))

        elif question_type == 'area_zhongyao':
            desc = [i['m.name'] for i in answer]
            subject = answer[0]['n.name']
            final_answer = '生长在{0}的中药有：{1}'.format(subject,'、'.join(desc))

        return final_answer




if __name__ == '__main__':
    searcher = AnswerSearcher()