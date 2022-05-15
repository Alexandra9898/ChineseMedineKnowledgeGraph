import os
import json
from py2neo import Graph,Node
class ZhongyaoGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/data_json/data_json4_stack.txt')
        self.g = Graph("http://localhost:7474",auth=("neo4j","123456"))


    def read_nodes(self):
        # 共７类节点
        zhongyao_infos=[]

        zhongyaos = []  # 中药
        books = []  # 摘录
        cures = []  # 主治症状
        functions=[]
        areas=[]

        # 构建节点实体关系
        rels_book = []  # 中药－摘录关系
        rels_cure = []  # 疾病－症状食物关系
        rels_function = []
        rels_area=[]


        for data in open(self.data_path, encoding="utf-8"):
            print("来了")
            zhongyao_dict = {}  # 每一条数据都要建立一个空字典
            data_json = json.loads(data)  # 加载一条data


            if "药物名称" in data_json:
                zhongyao = data_json['药物名称']  # 获取
                zhongyao_dict['name'] = zhongyao  # 放到中药属性
                zhongyaos.append(zhongyao)  # 实体加进去


            if "拼音名" in data_json:
                pinyin=data_json["拼音名"]
                zhongyao_dict["pinyin"]=pinyin


            if "别名" in data_json:
                other_name=data_json["别名"]
                zhongyao_dict["other_name"]=other_name


            if "来源" in data_json: ####
                origin=data_json["来源"]
                if "药材基源" in origin:
                    zhongyao_dict["resource"]=origin["药材基源"]
                if "拉丁植物动物矿物名" in origin:
                    zhongyao_dict["latin"] = origin["拉丁植物动物矿物名"]
                if "采收和储藏" in origin:
                    zhongyao_dict["collect"]=origin["采收和储藏"]
                if type(origin)==str:
                    zhongyao_dict["origin"]=origin

            if "生境分布" in data_json:
                the_location=data_json["生境分布"]
                if type(the_location)==str:
                    continue
                else:
                    if "生态环境" in the_location:
                        zhongyao_dict["environment"]=the_location["生态环境"]
                    if "资源分布" in the_location:
                        the_area = the_location["资源分布"]
                        for i in the_area:
                            rels_area.append([zhongyao, i])
                        areas+=the_area
                    else:
                        zhongyao_dict["location"]=the_location

            if "性味" in data_json:
                the_taste=data_json["性味"]
                zhongyao_dict["taste"]=the_taste

            if "功能主治" in data_json:
                the_symptom=data_json["功能主治"]
                if type(the_symptom)==str:
                    continue
                else:
                    if "功能" in the_symptom:
                        the_function=the_symptom["功能"]
                        for i in the_function:
                            rels_function.append([zhongyao,i])
                        functions+=the_function
                    if "主治" in the_symptom:
                        the_cure = the_symptom["主治"]
                        for i in the_cure:
                            rels_cure.append([zhongyao, i])
                        cures += the_cure

            if "用法用量" in data_json:
                howtouse=data_json["用法用量"]
                zhongyao_dict["howtouse"]=howtouse

            if "摘录" in data_json:  # node
                the_book=data_json["摘录"]
                rels_book.append([zhongyao,the_book])
                books.append(the_book)


            zhongyao_infos.append(zhongyao_dict)
        return zhongyao_infos,set(zhongyaos),set(books),set(cures),set(functions),set(areas),rels_book,rels_cure,rels_function,rels_area

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心中药的节点'''
    def create_zhongyaos_nodes(self, zhongyao_infos):
        count = 0
        for zhongyao_dict in zhongyao_infos:
            print(zhongyao_dict)
            node = Node("zhongyao", name=zhongyao_dict.get('name'), pinyin=zhongyao_dict.get('pinyin'),
                        othername=zhongyao_dict.get('other_name'),resource=zhongyao_dict.get('resource'),
                        latin=zhongyao_dict.get('latin'),collect=zhongyao_dict.get('collect'),
                        origin=zhongyao_dict.get('origin'),environment=zhongyao_dict.get('environment'),
                        location=zhongyao_dict.get('location'),function_cure=zhongyao_dict.get('function_cure'),
                        howtouse=zhongyao_dict.get('howtouse'))
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        zhongyao_infos,zhongyaos,books,cures,functions,areas,rels_book,rels_cure,rels_function,rels_area = self.read_nodes()
        self.create_zhongyaos_nodes(zhongyao_infos)
        self.create_node('book', books)
        print(len(books))
        self.create_node('cure', cures)
        print(len(cures))
        self.create_node('function', functions)
        print(len(functions))
        self.create_node('area',areas)
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        zhongyao_infos,zhongyaos,books,cures,functions,areas,rels_book,rels_cure,rels_function,rels_area = self.read_nodes()
        self.create_relationship('zhongyao', 'cure', rels_cure, 'cure', '主治')
        self.create_relationship('zhongyao', 'book', rels_book, 'book', '摘录')
        self.create_relationship('zhongyao', 'function', rels_function, 'function', '功能')
        self.create_relationship('zhongyao','area',rels_area,'area',"资源分布")
    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        zhongyao_infos,zhongyaos,books,cures,functions,areas,rels_book,rels_cure,rels_function,rels_area = self.read_nodes()
        f_zhongyao = open('./node/zhongyao.txt', 'w')
        f_book = open('./node/book.txt', 'w')
        f_function = open('./node/function.txt', 'w')
        f_cure = open('./node/cure.txt', 'w')
        f_area = open('./node/area.txt', 'w')

        f_zhongyao.write('\n'.join(list(zhongyaos)))
        f_book.write('\n'.join(list(books)))
        f_function.write('\n'.join(list(functions)))
        f_cure.write('\n'.join(list(cures)))
        f_area.write('\n'.join(list(areas)))

        f_zhongyao.close()
        f_book.close()
        f_function.close()
        f_cure.close()
        f_area.close()

        return



if __name__ == '__main__':
    handler = ZhongyaoGraph()
    handler.g.run('match (n) detach delete n')
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")
    handler.create_graphrels()
    handler.export_data()
print(ZhongyaoGraph().read_nodes())