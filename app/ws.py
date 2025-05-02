from flask_socketio import SocketIO, emit
from app.models import db, Question
import random
from app.utils.llm_utils import evaluate_answer


socketio = SocketIO(cors_allowed_origins="*")  # 创建SocketIO实例，允许所有来源的跨域请求   

# 注册SocketIO事件
def register_socketio_events(app):
    # 将SocketIO实例与Flask应用实例进行关联，使SocketIO能在Flask应用的上下文环境中工作
    # 整合Flask应用的配置信息，让SocketIO依据这些配置来监听连接请求等
    # 为后续注册和处理SocketIO相关事件奠定基础，确保实时通信功能正常运作
    socketio.init_app(app)  # 初始化SocketIO实例
    
    #处理用户消息事件
    @socketio.on('user_message')
    
    def handle_user_message(data):
        #处理用户回答并获取相关信息
        user_answer = data.get('message')  # 用户刚刚的发言
        prev_question_id = data.get('prev_question_id')  # 上一道题的id，第一轮为none
        used_ids = data.get('used_ids', []) # 前端维护的已问过的问题id列表
        
        # 如果是第一轮，不评价，直接出题
        if not prev_question_id:
            # 从数据库的 Question 表中随机挑选一个 id 不在 used_ids 列表中的问题记录，将其赋值给变量 next_q
            next_q = Question.query.filter(~Question.id.in_(used_ids)).order_by(db.func.rand()).first()
            # 若查询到问题记录，获取问题内容；否则提示题库为空
            next_q_text = next_q.content if next_q else "题库是空欸，请先添加题目讷"

            emit('bot_message', {
                'evaluation': "欢迎来到面试欸，现在要开始第一题了哦~",
                'next_question': next_q_text,  # 向客户端发送下一道题目
                'next_question_id': next_q.id if next_q else None,  # 向客户端发送下一道题目的id
            })  # 向客户端发送下一道题目
            return  # 结束函数执行
        
        # 第二轮及以后：评价+出题
        # 1.获取上一题题干
        prev_q = Question.query.get(prev_question_id)  # 根据上道题的id获取题目对象
        prev_q_text = prev_q.content if prev_q else ""

        # 2.调用封装的prompt函数，获取评价
        evaluation = evaluate_answer(user_answer, prev_q_text)  # 调用评价函数，获取评价结果

        # 3.从数据库中随机挑选一个 id 不在 used_ids 列表中的问题记录，将其赋值给变量 next_q
        # 获取新题
        next_q = Question.query.filter(~Question.id.in_(used_ids)).order_by(db.func.rand()).first()
        next_q_text = next_q.content if next_q else "题库用完咯，请先添加题目。"
        
        emit('bot_response', {
            'evaluation': evaluation,  # 向客户端发送评价结果
            'next_question': next_q_text,  # 向客户端发送下一道题目
            'next_question_id': next_q.id if next_q else None,  # 向客户端发送下一道题目的id
        })  # 获取新题的内容