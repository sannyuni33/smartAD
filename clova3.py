import cv2
import requests
import json
from threading import Thread

client_id = "38hNSdXWRhGUHxMpaRoV"
client_secret = "5YF8TJC9YQ"
url = "https://openapi.naver.com/v1/vision/face"
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

# 하나의 이미지에 대한 인식결과를 저장할 리스트
# 성별/나이별 인식횟수 저장
# 10대남자, 20대남자, ..., 60대여자 순서
# 얼굴인식 클래스의 애트리뷰트로 넣어야 openCV 기반, NAVER 기반이 둘 다 접근가능
recog_result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# 이미지파일 이름을 받아서 NAVER API 기반으로 얼굴분석
# openCV도 학습모델 만들어주고 이거랑 같은 역할 하는 메소드 만들어야함.
# '얼굴분석'이라는 메소드가 그 메소드랑 이 메소드를 둘 다 호출하는 식으로 만들거임.


class FaceRecog(Thread):
    def __init__(self, FILE_NAME):
        Thread.__init__(self, FILE_NAME)
        self.FILE_NAME = FILE_NAME

    def run(self):
        self.recog_result = self.naverRecog(self.FILE_NAME)
        self.genderAge = self.extractResult(self.recog_result)
        # 이렇게 하면 (성별, 연령대)튜플을 뱉는데
        # 이 튜플을 서버에 뱉어내서
        # 서버가 쿼리문 돌리고
        # 디스플레이 쓰레드가 디스플레이 클라이언트에게 전달할 방법을 찾아야겠음
        # 전역변수 쓰면 어때요?
        # 이거 안되면 얼굴인식 쓰레드 없애고 그냥 서버에서 객체 생성하게 해야하는데..
        # 아니면 쓰레드로 돌리는데 이 클래스를 서버 파일에서 선언을 하고,,
        # 전역변수를 쓰면 가능하지 않나. 라는 생각까지 해보고 퇴근합니다

    def naverRecog(self, FILE_NAME):
        files = {'image': open(FILE_NAME, 'rb')}
        response = requests.post(url, files=files, headers=headers)
        rescode = response.status_code

        if rescode == 200:
            pass
            # print(response.text)
        else:
            print("Error Code:" + rescode)

        json_data = json.loads(response.text)
        img = cv2.imread(FILE_NAME, cv2.IMREAD_COLOR)

        for i in json_data['faces']:
            x, y, w, h = i['roi'].values()
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            gender = i['gender']['value']
            age = i['age']['value']
            age1, age2 = age.split('~')
            final_age = (int(age1) + int(age2)) / 2

            result = """
                성별: %s
                나이: %s
                """ % (
                    gender,
                    age
                )
            print(result)
            cv2.putText(img, result, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            if gender == 'male':
                if 10 <= final_age < 20:
                    recog_result[0] += 1
                elif 20 <= final_age < 30:
                    recog_result[1] += 1
                elif 30 <= final_age < 40:
                    recog_result[2] += 1
                elif 40 <= final_age < 50:
                    recog_result[3] += 1
                elif 50 <= final_age < 60:
                    recog_result[4] += 1
                else:
                    recog_result[5] += 1
            else:
                if 10 <= final_age < 20:
                    recog_result[6] += 1
                elif 20 <= final_age < 30:
                    recog_result[7] += 1
                elif 30 <= final_age < 40:
                    recog_result[8] += 1
                elif 40 <= final_age < 50:
                    recog_result[9] += 1
                elif 50 <= final_age < 60:
                    recog_result[10] += 1
                else:
                    recog_result[11] += 1

        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # print("이미지 인식결과:")
        # print(recog_result)

        return recog_result

    def extractResult(self, recog_result):
        if max(recog_result) == 0:
            print("인식실패띠 ㅜ")
            return -1, -1
        else:
            max_index = recog_result.index(max(recog_result))

        if max_index == 0:
            genderAge = ('male', 10)
        elif max_index == 1:
            genderAge = ('male', 20)
        elif max_index == 2:
            genderAge = ('male', 30)
        elif max_index == 3:
            genderAge = ('male', 40)
        elif max_index == 4:
            genderAge = ('male', 50)
        elif max_index == 5:
            genderAge = ('male', 60)
        elif max_index == 6:
            genderAge = ('female', 10)
        elif max_index == 7:
            genderAge = ('female', 20)
        elif max_index == 8:
            genderAge = ('female', 30)
        elif max_index == 9:
            genderAge = ('female', 40)
        elif max_index == 10:
            genderAge = ('female', 50)
        elif max_index == 11:
            genderAge = ('female', 60)

        print("최종 결과: ")
        print(genderAge)

        return genderAge


if __name__ == '__main__':
    FRthread = FaceRecog('asiana.jpg')
    FRthread.setDaemon(True)
    FRthread.start()
