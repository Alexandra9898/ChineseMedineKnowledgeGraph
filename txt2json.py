'''turn txt to json'''
import os
import json
import re

class txt2json:
    def __init__(self):
        self.location_list=self.get_location_list()
        self.content_dict=self.get_json()


    def get_location_list(self):
        with open("./data/location.txt","r",encoding="utf-8") as f:
            location_list=f.readlines()
        return location_list

    def get_json(self):
        txt_list=[]
        total_dict={}
        path = 'C:\\Users\\Alexandra\\Desktop\\知识图谱项目\\NER_project\\test_data\\all_zhongyao'
        for root,dirs,files in os.walk(path):
            for file in files:
                txt_list.append(os.path.join(root,file))

        for txt in txt_list:
            with open(txt,"r") as f:
                content=f.readlines()
                content=[i.strip() for i in content]
                content_dict={}
                for item in content:
                    item_tuple=tuple(item.split(':'))
                    value=item_tuple[1]
                    if item_tuple[0] in ("原形态"):
                        pass

                    if item_tuple[0] in ("出处"):
                        a = r'《(.*?)》'
                        slotList = re.findall(a, item_tuple[1])
                        value=slotList
                        pass

                    if item_tuple[0] in ("化学成份"):
                        pass

                    if item_tuple[0] in ("各家论述"):
                        pass

                    if item_tuple[0] in ("备注"):
                        pass

                    if item_tuple[0] in ("毒性"):
                        pass

                    if item_tuple[0] in ("归经"):
                        pass

                    if item_tuple[0] in ("功能主治"):
                        pass

                    if item_tuple[0] in ("生境分布"):
                        if item_tuple[1].find(r"资源分布：")!=-1:
                            t1 = re.split(r"资源分布：", item_tuple[1])
                            t1[0]=t1[0].replace("生态环境：","")
                            locations=[]
                            for location in self.location_list:
                                if location.strip() in t1[1]:
                                    locations.append(location.strip())
                            t1[1]=locations
                            value={"生态环境":t1[0],"资源分布":t1[1]}
                            print(value)
                        pass

                    if item_tuple[0] in ("附方"):
                        pass

                    if item_tuple[0] in ("出处"):

                        pass

                    if item_tuple[0] in ("药理作用"):
                        pass

                    if item_tuple[0] in ("药物名称"):
                        pass

                    if item_tuple[0] in ("来源"):
                        cut1 = item_tuple[1].find("药材基源：") + 5
                        cut2 = item_tuple[1].find("拉丁植物动物矿物名：") - 1
                        cut3 = item_tuple[1].find("拉丁植物动物矿物名：") + 10
                        cut4 = item_tuple[1].find("采收和储藏：")
                        cut5 = item_tuple[1].find("采收和储藏：") + 6
                        origin_dict={}
                        if item_tuple[1].find("药材基源：")!=-1:
                            origin_dict["药材基源"]=item_tuple[1][cut1:cut2].strip()
                        if item_tuple[1].find("拉丁植物动物矿物名：")!=-1:
                            origin_dict["拉丁植物动物矿物名"]=item_tuple[1][cut3:cut4].strip()
                        if item_tuple[1].find("采收和储藏：")!=-1:
                            origin_dict["采收和储藏"]=item_tuple[1][cut5:-1].strip()
                        if origin_dict!={}:
                            value=origin_dict
                        pass

                    if item_tuple[0] in ("性状"):
                        pass

                    if item_tuple[0] in ("英文名"):
                        pass

                    if item_tuple[0] in ("别名"):
                        value = item_tuple[1].split("、")
                        pass

                    if item_tuple[0] in ("出处"):
                        pass

                    if item_tuple[0] in ("拼音名"):
                        pass

                    if item_tuple[0] in ("用法用量"):
                        pass

                    if item_tuple[0] in ("功能主治"):
                        l1 = item_tuple[1].strip("。").split("。")
                        sym_dict = {}
                        if len(l1) == 2:
                            l1[0] = re.split(r"[，；、]", l1[0])
                            sym_dict["功能"] = l1[0]
                            l1[1] = re.split(r"[，；、]", l1[1])
                            sym_dict["主治"] = [i.replace("主","").replace("用于","") for i in l1[1]]
                            value=sym_dict
                        pass

                    if item_tuple[0] in ("临床应用"):
                        pass

                    if item_tuple[0] in ("摘录"):
                        value="".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item_tuple[1]))
                        pass


                    content_dict[item_tuple[0]] = value

                with open("./data/data_json/data_json4_stack.txt","a",encoding="utf-8") as f_in:
                    json.dump(content_dict, f_in,ensure_ascii=False)
                    f_in.write("\n")
                    print("已转换{}为json".format(txt))

                total_dict[content_dict["药物名称"]]=content_dict
                # total_dict[content_dict["药物名称"]] = content_dict
        # return total_dict
        # with open("./data/data_json/data_json_total4.txt","w",encoding="utf-8") as f_in:
        #     json.dump(total_dict, f_in,ensure_ascii=False)
        #     f_in.write("\n")
        #     print("转换完成")
txt2json=txt2json()



