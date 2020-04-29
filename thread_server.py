import socketserver
import threading
import datetime
from DB_interface_test import DB_interface

HOST = '192.168.101.125'
PORT = 9999
lock = threading.Lock()  # 동기화 진행하는 스레드 생성


# 사용자 관리, 채팅 메시지 전송을 담당하는 클래스
class UserManager:
    # 사용자 이름, 주소정보를 담는 dict 구조체 생성
    def __init__(self):
        self.users = {}

    # 사용자 ID를 self.users 에 추가
    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send('이미 등록된 사용자에염!'.encode('utf-8'))
            return None

        # 새로운 사용자 등록
        lock.acquire()  # 스레드 동기화를 막는 lock
        self.users[username] = (conn, addr)
        lock.release()  # 사용자를 self.users dict 에 추가 후 lock 해제

        self.sendMessageToAll('[%s]님 입장' % username)
        print('+++ 대화 참여자 [%d명]' % len(self.users))

        return username

    # 사용자 연결 종료 시 사용자 삭제(등록 메서드와 유사한 구조)
    def removeUser(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s]님 퇴장ㅜ' % username)
        print('---대화 참여자 수 [%d]' % len(self.users))

    # 사용자가 전송한 메시지 처리(하나하나의 메시지마다)
    def messageHandler(self, username, msg):
        if msg[0] != '/':
            self.sendMessageToAll('[%s] %s' % (username, msg))
            return

        if msg.strip() == '/quit':
            self.removeUser(username)
            return -1

        if msg.strip() == '/ADs':
            # 실제로는 얼굴 인식 클래스한테 성별, 연령 전달 받아서 인자에 넣어야 함
            최종광고 = db.decide_AD('female', 20)
            print(최종광고)
            return

        if msg.strip() == '/fail':
            # 실제로는 카메라 핸들러한테 위치랑 시간 정보 받아서 인자에 넣어야 함
            많이인식 = db.find_majority('정왕역 1번출구', 17)
            print(많이인식)
            return

        if msg.strip() == '/succ':
            # 제대로 인식해서 결과도출하고 광고까지 결정했으면
            # 인식 결과는 뭐고, 광고판 ID는 뭐고, 날짜랑 시간은 어떻게 되고
            # 어떤 광고 송출했는지까지
            # 인식결과 테이블에 집어 넣어야함
            # 정왕역 1번출구에서 18시에 10대 여자애를 인식해서
            # 윤이버셜 광고를 내보냈다고 치고 프로토타입 작성ㄱㄱ
            # 이것까지는 됬고... 이제 시간 정보를 직접 입력하지말고
            # datetime 모듈 이용해서 실시간 시간 받아와서 인자로 넣어주기 시도 ㄱㄱ
            # 조빱이네
            # 실제로는 카메라 핸들러한테 위치랑 날짜/시간 정보 받고
            # 얼굴 인식 클래스한테 성별, 연령대 받고
            # DB 클래스한테 광고정보 받아야함
            today = datetime.datetime.today()
            date_info = str(today.year)+'.'+str(today.month)+'.'+str(today.day)
            db.insert_recog_result('정왕역 1번출구', 'female', 10, date_info, today.hour, '윤이버셜스튜디오_01')
            return

        if msg.strip() == '/twin':
            # 사용자가 광고판에서 디지털 트윈 광고를 터치했다고 가정하고
            # 광고 테이블에서 해당 광고의 관심지수 필드 값을 증가시켜야함
            # int 형 필드의 값을 증가시키는 쿼리문이 있는지 찾아봐야함
            # 영효헬스의 VR 이미지가 터치됬다고 가정, 관심지수를 10 올리려고 함
            # 인자는 광고 ID랑 관심지수 수치 두 개면 될듯
            # 관심지수를 영어로 하면 interest index 라고 한다
            # 실제로는 광고판 핸들러한테 광고 ID, 관심지수 증가수치 받아서
            # 인자로 넣어야 함
            db.increase_interest_index('영효헬스_01',10)
            return

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode('utf-8'))


class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    # 클라이언트 접속시 클라이언트의 주소 출력
    def handle(self):
        print('[%s] connected.' % self.client_address[0])

        try:
            username = self.registerUsername()  # 등록
            msg = self.request.recv(1024)  # 클라이언트가 뭐라고했는지
            while msg:  # 메시지가 왔으면
                print(msg.decode('utf-8'))
                if self.userman.messageHandler(username, msg.decode('utf-8')) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)
        except Exception as e:
            print(e)

        print('[%s] connection closed.' % self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('Login ID:'.encode('utf-8'))
            username = self.request.recv(1024)
            username = username.decode('utf-8').strip()
            if self.userman.addUser(username, self.request,
                                    self.client_address):
                return username


class ChattingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runServer():
    print('+++ Launch Chatting server...')
    print('+++ Press Ctrl+C to terminate chatting server')

    try:
        server = ChattingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        db.conn.close()
        print('--- BYE BYE')
        server.shutdown()
        server.server_close()


db = DB_interface()
runServer()
