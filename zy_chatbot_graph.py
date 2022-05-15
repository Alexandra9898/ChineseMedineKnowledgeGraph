from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我太笨了，没有办法回答上您的问题，找更聪明的人去吧，别找我啦。'
        res_classify = self.classifier.classify(sent)  # 给问题分好类
        if not res_classify: # 如果不是其中一类
            return answer
        res_sql = self.parser.parser_main(res_classify)  # 如果是其中一类，生成查询sql语言语句
        final_answers = self.searcher.search_main(res_sql)  # 用sql语句找到最后的final answer
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers) # 把最后列表式的结果返回

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('回答:', answer)