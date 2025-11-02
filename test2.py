import numpy as np

from get_transcript import get_transcript
from test import chatQwen3

translated = [
{'start': np.float64(0.0), 'end': np.float64(2.72), 'text': 'Đừng đến Việt Nam mà không học những mẹo đơn giản này về ẩm thực đường phố.'},
{'start': np.float64(2.9), 'end': np.float64(4.16), 'text': 'Đầu tiên, con voi trong phòng.'},
{'start': np.float64(4.32), 'end': np.float64(5.18), 'text': 'Bạn có bị ngộ độc thực phẩm không?'},
{'start': np.float64(5.44), 'end': np.float64(6.94), 'text': 'Câu trả lời ngắn có lẽ là không.'},
{'start': np.float64(7.1), 'end': np.float64(10.24), 'text': 'Chúng tôi đã sống ở đây được 2 năm và chưa gặp phải những vấn đề như rau sống.'},
{'start': np.float64(10.24), 'end': np.float64(11.24), 'text': 'hoặc nước đá và đồ uống.'},
{'start': np.float64(11.48), 'end': np.float64(14.7), 'text': 'Nếu một gánh hàng rong đường phố đầy ắp người địa phương, 9 lần trong 10 bạn sẽ ổn.'},
{'start': np.float64(14.98), 'end': np.float64(19.16), 'text': 'Đồ uống rẻ nhất bạn có thể gọi tại hầu như bất kỳ nhà hàng hay quán ăn đường phố nào ở Việt Nam là'},
{'start': np.float64(19.16), 'end': np.float64(21.04), 'text': 'Gọi là Chhada hay Trà đá.'},
{'start': np.float64(21.38), 'end': np.float64(24.52), 'text': 'Thường được cung cấp miễn phí tại các nhà cung cấp nhỏ hoặc lên đến 20 cent mỗi cốc.'},
{'start': np.float64(24.76), 'end': np.float64(28.48), 'text': 'Đôi khi bạn đã tìm thấy nó trên bàn hoặc có thể tìm thấy nó được cất giấu sẵn để bạn lấy.'},
{'start': np.float64(28.48), 'end': np.float64(31.22), 'text': 'Hãy tự do lấy mình như thế này nhưng chúng tôi luôn hỏi trước.'},
{'start': np.float64(31.54), 'end': np.float64(34.06), 'text': 'Nếu bạn thấy điều này trên bàn, đó là tương ớt tự làm.'},
{'start': np.float64(34.4), 'end': np.float64(35.52), 'text': 'Đồ này cực kỳ nguy hiểm.'},
{'start': np.float64(36.06), 'end': np.float64(37.68), 'text': 'Cẩn trọng và bắt đầu với một chút.'},
{'start': np.float64(38.08), 'end': np.float64(40.3), 'text': 'Nếu bạn thấy những miếng lau này được phục vụ cho bạn, chúng không phải là miễn phí.'},
{'start': np.float64(40.58), 'end': np.float64(44.94), 'text': '20 cent đến 40 cent cho mỗi lần lau, đây là giá rẻ nhưng đáng lưu ý nếu bạn thấy ở nơi mình đang ở.'},
{'start': np.float64(44.94), 'end': np.float64(45.98), 'text': 'Hãy trả tiền khi bạn xong ăn.'},
{'start': np.float64(46.22), 'end': np.float64(48.72), 'text': 'Nếu bạn có chanh trên bàn, hãy dùng chúng để lau que tăm.'},
{'start': np.float64(49.36), 'end': np.float64(51.8), 'text': 'Họ thường sạch sẽ nhưng tốt hơn là cẩn thận để tránh hối tiếc.'},
{'start': np.float64(52.16), 'end': np.float64(54.42), 'text': 'Chúng tôi sống ở Việt Nam và đăng nội dung như thế này hàng ngày.'},
{'start': np.float64(54.82), 'end': np.float64(56.3), 'text': 'Hãy theo dõi chúng tôi nếu bạn đang lên kế hoạch cho một chuyến đi.'}
]

segments = [{'start': 0.0, 'end': 1.7, 'text': ' 와이파이가 갑자기 안 터지신다고요?'}, {'start': 1.74, 'end': 3.46, 'text': ' 네네 어젯밤부터 갑자기 안 터지더라고요'}, {'start': 3.46, 'end': 5.4, 'text': ' 와이파이 공유기가 좀 오래되긴 했는데'}, {'start': 5.4, 'end': 6.7, 'text': ' 예 제가 한번 봐볼게요'}, {'start': 6.7, 'end': 7.48, 'text': ' 어 예예'}, {'start': 7.48, 'end': 10.72, 'text': ' 아 이거 공유기가 구형이라서 수명이 이거 다 된 거 같은데요'}, {'start': 10.72, 'end': 12.48, 'text': ' 아 그래요? 그럼 새 걸로 바꿔야겠네요'}, {'start': 12.48, 'end': 15.1, 'text': ' 그렇죠 아무래도 새 걸로 교차를 하시는 게 좋으시죠?'}, {'start': 15.26, 'end': 17.08, 'text': ' 어 그러면 새 걸로... 여보?'}, {'start': 17.14, 'end': 18.34, 'text': ' 그래 그럼 새 걸로 교차해주세요'}, {'start': 18.34, 'end': 19.08, 'text': ' 예 알겠습니다'}, {'start': 20.68, 'end': 22.48, 'text': ' 예 설치 다 끝났습니다'}, {'start': 22.48, 'end': 23.32, 'text': ' 아 네 고생하셨어요'}, {'start': 23.32, 'end': 25.1, 'text': ' 그 출장비나 설치비 같은 게...'}, {'start': 25.1, 'end': 25.66, 'text': ' 아 없습니다'}, {'start': 26.400000000000002, 'end': 27.82, 'text': ' 이거는 서비스 차원이기 때문에'}, {'start': 27.82, 'end': 29.34, 'text': ' 예 그럼 저는 들어가보겠습니다'}, {'start': 29.34, 'end': 30.78, 'text': ' 네 감사해요'}, {'start': 30.78, 'end': 32.84, 'text': ' 어이구 요즘 세상이 참 좋아졌어'}, {'start': 32.84, 'end': 34.76, 'text': ' 옛날에는 뭐 출장비나 설치비니가...'}, {'start': 34.76, 'end': 35.48, 'text': ' 잠깐만요'}, {'start': 36.58, 'end': 38.58, 'text': ' 아 예 예 뭐 궁금하신 점이라도'}, {'start': 38.58, 'end': 40.2, 'text': ' 이거 공유기가 원래 이렇게 커요?'}, {'start': 42.26, 'end': 44.92, 'text': ' 아유 요즘 뭐 포지다 파이브지다 해가지고'}, {'start': 44.92, 'end': 47.34, 'text': ' 속도 따라가려면 보통 공유기로는 안 돼요'}, {'start': 47.34, 'end': 50.06, 'text': ' 그래 여보 그 슈퍼 컴퓨터는 엄청 크대잖아'}, {'start': 50.06, 'end': 51.22, 'text': ' 이거는 큰 것도 아니야'}, {'start': 51.22, 'end': 52.94, 'text': ' 응 그래? 꼭 게임기 같은데'}, {'start': 53.660000000000004, 'end': 56.4, 'text': ' 아니 무슨 게임기는 게임기야 여보'}, {'start': 56.4, 'end': 58.32, 'text': ' 저거 딱 봐도 공유기 같이 생겼구만 어?'}, {'start': 58.32, 'end': 60.04, 'text': ' 아유 사부님 농담도 잘하십니다'}, {'start': 60.04, 'end': 61.28, 'text': ' 예 그럼 자른님만 들어'}, {'start': 61.28, 'end': 61.56, 'text': ' 알겠습니다'}, {'start': 62.8, 'end': 64.74, 'text': ' 어 왔어 밥은'}, {'start': 64.74, 'end': 66.14, 'text': ' 우와 아빠 풀스 샀어?'}, {'start': 66.22, 'end': 66.48, 'text': ' 풀스?'}, {'start': 66.52, 'end': 68.38, 'text': ' 어 풀스 풀스 어 풀스 샀지'}, {'start': 68.38, 'end': 68.84, 'text': ' 어 어 어'}, {'start': 68.84, 'end': 69.7, 'text': ' 아 예 예 풀스죠'}, {'start': 69.7, 'end': 71.04, 'text': ' 저게 모델명이 풀스예요'}, {'start': 71.04, 'end': 71.94, 'text': ' 플래시 스피드'}, {'start': 71.94, 'end': 73.22, 'text': ' 비처럼 빠른 공유기 뭐 이런'}, {'start': 73.22, 'end': 75.04, 'text': ' 아유 아드님이 똑똑하시네요'}, {'start': 75.04, 'end': 76.5, 'text': ' 왜 공유기 모델명을 어떻게 알아?'}, {'start': 79.06, 'end': 80.54, 'text': ' 아 아 아'}, {'start': 80.54, 'end': 81.86, 'text': ' 그거 학교에서 배웠지'}, {'start': 81.86, 'end': 83.44, 'text': ' 학교에서 공유기 이름을 가르쳐?'}, {'start': 83.5, 'end': 85.38, 'text': ' 아 그거 기가 시간에 다 배우는 거야'}, {'start': 85.38, 'end': 86.88, 'text': ' 기가 와이파이 그런 거 다'}, {'start': 88.32, 'end': 89.74, 'text': ' 뭐야 다들 왜 그렇게 당황해'}, {'start': 89.74, 'end': 92.16, 'text': ' 아유 여보 뭔 와이파이 공유기 가지고 뭘 그래'}, {'start': 92.16, 'end': 93.14, 'text': ' 얼른 들어가서 쉬어'}, {'start': 93.14, 'end': 94.52, 'text': ' 드라마 곧 시작할 시간이잖아'}, {'start': 94.52, 'end': 96.04, 'text': ' 예 사부님 그럼 저도 들어가 보겠습니다'}, {'start': 96.04, 'end': 98.08, 'text': ' 아 엄마 내가 알아서 밥 차려 먹을게'}, {'start': 98.08, 'end': 100.4, 'text': ' 어 오빠 나 여기 지금 와이파이 공유기 바꿨거든?'}, {'start': 101.86, 'end': 103.7, 'text': ' 어 근데 크기가 되게 크거든?'}, {'start': 103.84, 'end': 104.6, 'text': ' 이름이 풀스래'}, {'start': 104.6, 'end': 104.94, 'text': ' 풀스?'}, {'start': 105.12, 'end': 106.1, 'text': ' 뭐 플래시 스테이션만 하는 거야?'}, {'start': 106.3, 'end': 106.98, 'text': ' 어? 플래시 스테이...'}, {'start': 106.98, 'end': 108.44, 'text': ' 아 예 형님 잘 지내시죠'}, {'start': 108.44, 'end': 108.9, 'text': ' 뭐야?'}, {'start': 109.26, 'end': 110.74, 'text': ' 어 박사방 오랜만이야 잘 지내지?'}, {'start': 111.0, 'end': 111.88, 'text': ' 아 잘 지내죠'}, {'start': 111.88, 'end': 114.06, 'text': ' 아 저 형님 저 이번에 공유기 바꿨어요'}, {'start': 114.06, 'end': 114.98, 'text': ' 저 이제 풀스라고'}, {'start': 117.03999999999999, 'end': 119.18, 'text': ' 아 그거 알지 그거 알지 풀스'}, {'start': 119.18, 'end': 120.18, 'text': ' 아 그거 뭐야 그거'}, {'start': 120.18, 'end': 120.82, 'text': ' 플래시 스피드'}, {'start': 120.82, 'end': 121.8, 'text': ' 어 그래 그거 플래시 파트'}, {'start': 121.8, 'end': 123.86, 'text': ' 요즘 이게 유행이잖아요'}, {'start': 123.86, 'end': 125.46, 'text': ' 아니 그니까 그니까 그 요즘 유행이죠'}, {'start': 125.46, 'end': 126.6, 'text': ' 솔직히 말해 이거 뭐야?'}, {'start': 126.68, 'end': 128.1, 'text': ' 어 해서나가지고 운전 중이라서'}, {'start': 128.1, 'end': 129.56, 'text': ' 한 달 뒤에 다시 돌아갈게 미안해'}, {'start': 129.56, 'end': 130.44, 'text': ' 여보세요 여보세요'}, {'start': 130.44, 'end': 131.52, 'text': ' 너 차 없잖아'}, {'start': 131.52, 'end': 132.12, 'text': ' 똘똘'}, {'start': 132.12, 'end': 134.16, 'text': ' 솔직히 말해'}, {'start': 134.16, 'end': 135.06, 'text': ' 이거 뭐야?'}, {'start': 137.66, 'end': 138.8, 'text': ' 3초 준다'}, {'start': 138.8, 'end': 140.0, 'text': ' 3'}, {'start': 140.92, 'end': 141.54, 'text': ' 2'}, {'start': 142.32, 'end': 142.94, 'text': ' 1'}, {'start': 142.94, 'end': 144.52, 'text': ' 야 박현석 가방만 넣고 나온다며'}, {'start': 144.52, 'end': 144.96, 'text': ' 가방 넣고 다 넣어'}, {'start': 144.96, 'end': 146.88, 'text': ' 와 풀스다'}, {'start': 146.88, 'end': 149.16, 'text': ' 그냥 풀스도 아니고 풀스 프로네'}, {'start': 149.16, 'end': 150.3, 'text': ' 진짜 부럽다'}, {'start': 150.3, 'end': 152.08, 'text': ' 이 VR이랑 4K도 지원 되잖아요 그쵸'}, {'start': 152.08, 'end': 153.92, 'text': ' 와 4K로 게임하면 무슨 느낌일까'}, {'start': 153.92, 'end': 155.74, 'text': ' 우와 진짜 핵 때문에 저석 박칠 일도 없고'}, {'start': 155.74, 'end': 157.72, 'text': ' 진짜 현질 일도면 오직하는 양상용 게임에서는'}, {'start': 157.72, 'end': 159.62, 'text': ' 절대 느낄 수 없는 그 콘솔 감성 아시죠'}, {'start': 159.62, 'end': 162.1, 'text': ' 나도 패드로 손만 느낌해서 게임하고 싶다'}, {'start': 162.1, 'end': 163.78, 'text': ' 아줌마줌마 저도 가끔 와서 이거 해도 되죠'}, {'start': 168.8, 'end': 169.84, 'text': ' 플래시 스테이션'}]
# list_target_duration = [float(seg['end']-seg['start']) for seg in translated]
# print(list_target_duration)

# print(translated["text"])
# vocals_path = "split_temp\\vocals.wav"
#
# transcript = get_transcript(vocals_path)
# transcript_seg = transcript["segments"]
#
# segments = []
# for seg in transcript_seg:
#     segments.append({
#         "start": seg["start"],
#         "end": seg["end"],
#         "text": seg["text"]
#     })
#
# print(segments)

# orin_lang_code = transcript["language"]
# print(transcript_seg)
#
# result = chatQwen3(segments, origin_lang_code="ko", target_lang_code="vi")
# for r in result:
#     print(r["text"])
#
# print(len([seg["text"] for seg in segments]), "-", len([res["text"] for res in result]))
# # duration_list = []
# # for res in result:
# #     duration = res["end"] - res["start"]
# #     duration_list.append(duration)
# duration_list = [res["end"] - res["start"] for res in result]
#
# print([duration for duration in duration_list if duration > 0])
#
# print(f"len duration: {len(duration_list)}")
#
# count_positive = sum(duration > 0 for duration in duration_list)
# print(f"len duration > 0: {count_positive}")