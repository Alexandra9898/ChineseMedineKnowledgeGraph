# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args): #{'args': {'矮脚龙胆': ['zhongyao'], '辞典': ['book']},
                                       # 'question_types': ['book_zhongyao', 'zhongyao_desc']}
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict #{"zhongyao":[矮脚龙胆，矮地茶]，”book“:[辞海]}

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']  # 从classifier的输出里提取
        entity_dict = self.build_entitydict(args) # #{"zhongyao":[矮脚龙胆，矮地茶]，”book“:[辞海]}
        question_types = res_classify['question_types']  # 从classifier的输出里提取
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'zhongyao_book': #sql_transfer(zhongyao_sympton,zhongyao)
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'book_zhongyao':
                sql = self.sql_transfer(question_type, entity_dict.get('book'))

            if question_type == 'zhongyao_cure':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'cure_zhongyao':
                sql = self.sql_transfer(question_type, entity_dict.get('cure'))

            if question_type == 'zhongyao_function':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'function_zhongyao':
                sql = self.sql_transfer(question_type, entity_dict.get('function'))

            if question_type == 'zhongyao_area':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'area_zhongyao':
                sql = self.sql_transfer(question_type, entity_dict.get('area'))

            if question_type == 'zhongyao_pinyin':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'zhongyao_collect':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'zhongyao_othername':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'zhongyao_resource':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'zhongyao_latin':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'zhongyao_environment':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'zhongyao_taste':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'zhongyao_howtouse':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if question_type == 'zhongyao_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('zhongyao'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)
        return sqls # 转化成sql语句

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:  # 如果没有实体，那么返回[]
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'zhongyao_pinyin':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return m.name, m.pinyin".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'zhongyao_othername':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return m.name, m.othername".format(i) for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'zhongyao_resource':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return m.name, m.resource".format(i) for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'zhongyao_latin':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return m.name, m.latin".format(i) for i in entities]

        elif question_type == 'zhongyao_collect':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return m.name, m.collect".format(i) for i in entities]

        elif question_type == 'zhongyao_environment':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return m.name, m.environment".format(i) for i in entities]

        elif question_type == 'zhongyao_taste':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return m.name, m.taste".format(i) for i in entities]
        # 查询疾病的治疗方式
        elif question_type == 'zhongyao_howtouse':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return m.name, m.howtouse".format(i) for i in entities]

 #####  # 查询疾病的相关介绍
        elif question_type == 'zhongyao_desc':
            sql = ["MATCH (m:zhongyao) where m.name = '{0}' return properties(m)".format(i) for i in entities]
        # 查询疾病有哪些症状
        elif question_type == 'zhongyao_cure':
            sql = ["MATCH (m:zhongyao)-[r:cure]->(n:cure) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'zhongyao_book':
            sql = ["MATCH (m:zhongyao)-[r:book]->(n:book) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'zhongyao_function':
            sql = ["MATCH (m:zhongyao)-[r:function]->(n:function) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'zhongyao_area':
            sql = ["MATCH (m:zhongyao)-[r:area]->(n:area) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'cure_zhongyao':
            sql = ["MATCH (m:zhongyao)-[r:cure]->(n:cure) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'book_zhongyao':
            sql = ["MATCH (m:zhongyao)-[r:book]->(n:book) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'function_zhongyao':
            sql = ["MATCH (m:zhongyao)-[r:function]->(n:function) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'area_zhongyao':
            sql = ["MATCH (m:zhongyao)-[r:area]->(n:area) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()