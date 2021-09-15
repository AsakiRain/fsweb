import asyncio
import aiomysql
import hashlib
import os
class UseMysql:
    def __init__(self):
        self.conn = None
        self.pool = None
    async def initpool(self):
        __pool = await aiomysql.create_pool( #双下划线表示这是一个完全的私有变量，单下划线形式上表示私有，但是仍然可以被访问到
            host='localhost',
            port=3306,
            user='usersystem',
            password='ssr129631',
            db='usersystem',
            autocommit = False,
            minsize = 1,
            maxsize= 5, 
        )
        return __pool
    async def getcursor(self):
        conn = await self.pool.acquire()
        cur = await conn.cursor()
        return conn,cur
    async def returncursor(self,conn,cur):
        if cur:
            await cur.close()
        await self.pool.release(conn)
    async def query(self,query,param=None):
        conn,cur = await self.getcursor()
        try:
            await cur.execute(query,param)
            return await cur.fetchall()
        except:
            print('内部错误')
        finally:    #finally会无条件执行，尽管return存在，但是else不会在return后面执行
            await self.returncursor(conn,cur)
        #以上面的注释语句为例，从内到外分析
        #os.urandom() 
        #   This function returns random bytes from an OS-specific randomness source.
        #   The returned data should be unpredictable enough for cryptographic applications, 
        #   though its exact quality depends on the OS implementation.
        #   On Windows, it will use CryptGenRandom() to work.
        #Reference: https://docs.python.org/3/library/os.html
        #os.urandom(16) 会生成一个16字节的 bytes 对象，用 list() 可以将每一位作为列表的一项，并返回一个列表
        #实际使用中不加 list() 也可以
        #lambda 匿名函数：对于给定的 x ，做冒号之后的操作并返回结果，如 lambda x: x + 1 将会得到2
        #在这里，对于给定x，将其转换为 16 进制（形如'0x1b'）的字符串后，进行判断
        #如果字符串长度 >= 4 就返回字符串'/x'，即不用补足0；如果不足4位，则补一个0
        #在实际使用中由于不需要'/x'标志指示 16 进制，所以仅返回''或者'0'
        #之后，再将返回结果加上实际 16 进制后的值，得到新的一项
        #map(操作函数, 一个或多个序列, ...)，将序列中的每一项取出，运行给定的操作函数得到返回值，用其替换序列中的原值
        #在这里 lambda 匿名函数是操作函数，os.urandom(16) 是一个序列，经过操作，原序列变成每一项都只有两个字符的新序列
        #str.join(序列)，其中str是连接符号，这里不需要所以为空；序列是map函数返回的新序列

# async def test():
#     mysqlobj = await getamysqlobj()
#     r = await mysqlobj.query("select user,name from user")
#     for i in r:
#         print(i)
# async def getamysqlobj():
#     mysqlobj = UseMysql()
#     pool = await mysqlobj.initpool()
#     mysqlobj.pool = pool
#     return mysqlobj

# loop = asyncio.get_event_loop()
# loop.run_until_complete(test())