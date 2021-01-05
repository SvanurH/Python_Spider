import pymongo

class storage:
  def __init__(self,data,database='python',table='blibli'):  # 接收参数		
	self.data = data
    self.database = database
    self.table = table
		
  def __link(self):  # 连接数据库
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[self.database]
    col = db[self.table]
    return col
  
  def __insert(self):  #插入数据
    col = self.__link()
    col.insert_one(self.data)
    
	def run(self):  # 运行
		self.__insert()
