import pygame.image

from spaceship import Spaceship
from attackSystem import AttackSystem as Att
from gameTools import *
from game import Game


from sound import Sound


class Player:
    def __init__(self):
        self.spaceship = self._shipInit('..\\assets\\Ship\\ship1.json')
        self.bullets = Att.getBullets("superblue")

    def _loadInfo(self, shipPath):
        return HandleJson.readFile(shipPath)

    def _loadImgList(self, listPath: list):
        img = []
        try:
            for path in listPath:
                img.append(Image.load(path))
        except Exception:
            pass
        return img

    def _shipInit(self, path):
        """
        Tao doi tuong phi thuyen
        :param path:
        :return:
        """
        # vị trí phi thuyền khi mới được khởi tạo (giữa màn hình theo trục ngang, dưới cửa sổ màn hình 100px)
        pos = [Game.srect.width // 2, Game.srect.height + 100]
        sp = self._setShip(path, pos.copy())
        # để phi thuyền tự chạy lên cửa sổ màn hình
        sp.moveTo(0, -250, 6)

        # tạo HpBox để hiển thị hp người chơi
        hpRect = pygame.Rect(0, 0, 80, 20)
        hpRect.top = Screen.sRect.top + 20
        hpRect.right = Screen.sRect.right - 20
        sp.setShoHpCustom(hpRect)

        # truyền âm thanh khi nổ cho phi thuyền người chơi
        sp.setExplosionSound(Sound.playerExplosionSound)
        return sp

    def _setShip(self, shipPath: str, pos):
        """
        Tao phi thuyen thong qu du lieu duoc luu trong file json
        :param shipPath: duong dan file
        :param pos: vi tri phi thuyen
        :return: doi tuong phi thuyen (Spaceship)
        """
        shipInfo = HandleJson.readFile(shipPath)
        imgList = self._loadImgList(shipInfo.get('imgPathList'))
        return Spaceship(imgList, pos, shipInfo.get('size'), shipInfo.get('vel'), shipInfo.get('hp'), True)

    def setShip(self, imgList, size, vel, maxHp):
        """
        thiet lap phi thuyen moi (ho tro cho Item changeShip)
        :param imgList: danh sach anh cua phi thuyen
        :param size: [chieu dai, chieu rong] ([width, height])
        :param vel:
        :param maxHp:
        """
        try:
            self.spaceship.changeShip(imgList, size, vel, maxHp)
        except Exception:
            pass

    def setBullets(self, bulletName):
        """
        Doi dan moi (Ho tro Item changeBullets)
        :param bulletName: ten loai dan
        """
        self.bullets = Att.getBullets(bulletName)
        self.bullets.setLevel(1)

    def _movementKey(self):
        """
        Tao 1 vector 2 chieu voi chieu dua vao su kien nhan phim tu ban phim
        :return: vector2D
        """
        # bắt sự kiện nhấn phím
        keyPress = pygame.key.get_pressed()
        # khởi tạo đối tượng vector 2 chiều
        v = pygame.Vector2([0, 0])
        if keyPress[pygame.K_a]: # trái
            v.x = -1
        elif keyPress[pygame.K_d]: # phải
            v.x = 1
        if keyPress[pygame.K_w]: # lên
            v.y = -1
        elif keyPress[pygame.K_s]: # xuống
            v.y = 1
        if v.length() > 1:
            # chuẩn hóa vector để vector trở thành vector đơn vị (chỉ còn chỉ hướng) nếu độ dài của nó lớn hơn 1
            return v.normalize()
        return v

    def _movement(self):
        """
        xu ly di chuyen
        """
        v = self._movementKey()
        self.spaceship.rect.x += self.spaceship.vel * v.x
        self.spaceship.rect.y += self.spaceship.vel * v.y
        # đảm bảo phi thuyền luôn nằm trong cửa sổ game
        self.spaceship.ensuringInScreen()

    def _shot(self):
        """
        Xu ly ban
        """
        # bắt sự kiện nhấn phím 'space'
        keyPress = pygame.key.get_pressed()
        # kiểm tra sự kiện và trạng thái sẵn sàng bắn của đạn
        if keyPress[pygame.K_SPACE] and self.bullets.readyShoot():
            # tạo danh sách đạn
            bl = self.bullets.getBullets(self.spaceship.getBulletPos())
            # gửi đạn vào chương trình chính
            Game.ExtendPlayerBullet(bl)
            # tạo hiệu ứng giật khi bắn
            self.spaceship.shotEffect(self.bullets.recoil)
            # phát âm thanh bắn
            Sound.shotSound_play()

    def update(self):
        """
        Cap nhât doi tuong Player
        """
        self.spaceship.update()
        self._movement()
        self._shot()
