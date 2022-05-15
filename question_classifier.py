import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.zhongyao_path = os.path.join(cur_dir, 'node/zhongyao.txt')
        self.book_path = os.path.join(cur_dir, 'node/book.txt')
        self.function_path = os.path.join(cur_dir, 'node/function.txt')
        self.cure_path = os.path.join(cur_dir, 'node/cure.txt')
        self.area_path=os.path.join(cur_dir,"node/area.txt")

        # 加载特征词
        self.zhongyao_wds= [i.strip() for i in open(self.zhongyao_path,encoding='gbk') if i.strip()]
        self.book_wds= [i.strip() for i in open(self.book_path,encoding='gbk') if i.strip()]
        self.function_wds= [i.strip() for i in open(self.function_path,encoding='gbk') if i.strip()]
        self.cure_wds= [i.strip() for i in open(self.cure_path,encoding='gbk') if i.strip()]
        self.area_wds=[i.strip() for i in open(self.area_path,encoding='gbk') if i .strip()]
        self.region_words=set(self.zhongyao_wds + self.book_wds + self.function_wds+self.cure_wds+self.area_wds)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.zhongyao_qwds=["什么药",'药',"中药","吃","怎么办","有什么","是什么"]
        self.book_qwds = ["摘录",'出处','来源','哪里来','参考']
        self.function_qwds = ['功能',"什么用","用处","干什么",'有什么用', '有何用', '用处', '用途','有什么好处',
                              '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚',"功效"]
        self.area_qwds=["哪","分布","位置","生长在"]
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '需要', '要',"病","治"]
        self.pinyin_qwds = ["拼音","念","读","发音"]
        self.othername_qws = ['别名','其他名字','他名','叫法']
        self.resource_qwds = ['药材基源']
        self.latin_qwds=["拉丁"]
        self.collect_qwds=["采集","储藏","存储"]
        self.environment_qwds=["环境"]
        self.taste_qwds=["性味","味道","难吃"]
        self.howtouse_qwds=["怎么","用法"]


        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict   # 假设句子里面有"用来" 'args': {'矮脚龙胆': ['zhongyao']}

        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 已知中药（一个实体），求摘录（另一个实体）
        if self.check_words(self.book_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_book'
            question_types.append(question_type)

        # 已知摘录，求中药
        if self.check_words(self.zhongyao_qwds, question) and('book' in types):#
            question_type = 'book_zhongyao'
            question_types.append(question_type)

        # 已知中药，治疗疾病
        if self.check_words(self.cure_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_cure'
            question_types.append(question_type)

        # 已知疾病，求中药
        if self.check_words(self.zhongyao_qwds, question) and('cure' in types): #
            question_type = 'cure_zhongyao'
            question_types.append(question_type)

        # 已知中药，求功能
        if self.check_words(self.function_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_function'
            question_types.append(question_type)

        # 已知功能，求中药
        if self.check_words(self.zhongyao_qwds, question) and ('function' in types):#
            question_type = 'function_zhongyao'
            question_types.append(question_type)

        # 已知中药，求位置
        if self.check_words(self.area_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_area'
            question_types.append(question_type)

        # 已知位置，求中药
        if self.check_words(self.zhongyao_qwds, question) and ('area' in types):#
            question_type = 'area_zhongyao'
            question_types.append(question_type)


        # 已知中药，求其他
        if self.check_words(self.pinyin_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_pinyin'
            question_types.append(question_type)

        if self.check_words(self.othername_qws, question) and ('zhongyao' in types):
            question_type = 'zhongyao_othername'
            question_types.append(question_type)

        if self.check_words(self.resource_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_resource'
            question_types.append(question_type)

        if self.check_words(self.latin_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_latin'
            question_types.append(question_type)

        if self.check_words(self.collect_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_collect'
            question_types.append(question_type)

        if self.check_words(self.environment_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_environment'
            question_types.append(question_type)

        if self.check_words(self.taste_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_taste'
            question_types.append(question_type)

        if self.check_words(self.howtouse_qwds, question) and ('zhongyao' in types):
            question_type = 'zhongyao_howtouse'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该中药的描述信息返回
        if question_types == [] and 'zhongyao' in types:
            question_types.append('zhongyao_desc')

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.zhongyao_wds:
                wd_dict[wd].append('zhongyao')
            if wd in self.book_wds:
                wd_dict[wd].append('book')
            if wd in self.cure_wds:
                wd_dict[wd].append('cure')
            if wd in self.function_wds:
                wd_dict[wd].append('function')
            if wd in self.area_wds:
                wd_dict[wd].append('area')
        return wd_dict # 大概长什么样？--> [“牡丹”：”zhongyao“]

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        print(self.region_tree.iter(question))  ############
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds} #假设句子里面有牡丹 {“牡丹”：“zhongyao”}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)