import numpy as np
import cv2  # pip install opencv-python

class LifeGame():
    def __init__(self, img, lower_lim=2, upper_lim=3, birth_num=3, interval=50):
        self.last_gen = img
        self.lower_lim = lower_lim
        self.upper_lim = upper_lim
        self.birth_num = birth_num
        self.interval = interval
        # セル周囲の非ゼロ要素のカウント用フィルタ
        self.kernel = np.array([[1,1,1],
                                [1,0,1],
                                [1,1,1]])

    def nextGeneration(self):
        exist = (self.last_gen > 0)
        # neighborsはexistの各セルの周囲8マスのTrueの数を格納する配列
        neighbors = cv2.filter2D(exist.astype(np.uint8), -1, self.kernel, borderType=cv2.BORDER_CONSTANT)
        birth = (neighbors == self.birth_num)
        survive = ((self.lower_lim <= neighbors) & (neighbors <= self.upper_lim)) & exist
        # 生まれたセル+生存するセル=次世代
        next_gen = (birth | survive)
        return next_gen.astype(np.uint8) * 255

    def show(self):	# ウィンドウを表示しながら画像を更新する
        while True:
            cv2.namedWindow("LifeGame (press q to Quit)", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            cv2.imshow("LifeGame (press q to Quit)", self.last_gen)
            self.last_gen = self.nextGeneration()
            # qを押すと処理を終了する
            key = cv2.waitKey(self.interval)&0xff
            if key == ord('q'):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # 適当なパターンを作成
    size = (100, 100)
    img = np.random.choice([255, 0], size)
    # 実行
    lg = LifeGame(img.astype(np.uint8))
    lg.show()
