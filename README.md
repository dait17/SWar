# SWar - Game Bắn Súng Không Gian 🚀

![Demo](demo.gif)

## Giới thiệu
SWar là một game bắn súng không gian 2D được phát triển bằng Python và Pygame. Người chơi điều khiển tàu vũ trụ chiến đấu với các đợt kẻ thù, thu thập vật phẩm và đối mặt với boss để hoàn thành các màn chơi.

## Tính năng
- 🎮 Điều khiển tàu vũ trụ với 3 loại tàu khác nhau
- 🔫 Hệ thống vũ khí đa dạng (SuperBlue, FireBall, Shuriken)
- 👾 Nhiều loại kẻ thù: Alien, DragDoll, Boss
- 🎁 Vật phẩm hỗ trợ: năng lượng, máu, nâng cấp vũ khí
- 🗺️ 3 màn chơi với độ khó tăng dần
- 🔊 Âm thanh và hiệu ứng sống động
- 💾 Lưu cài đặt âm lượng

## Cài đặt
1. Clone repository:
   ```bash
   git clone https://github.com/your-username/SWar.git
   cd SWar
   ```

2. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Chạy game:
   ```bash
   cd sources
   python main.py
   ```

## Điều khiển
- **Phím mũi tên**: Di chuyển tàu
- **Phím Space**: Bắn
- **Phím Esc**: Thoát game

## Cấu trúc dự án
```
SWar/
├── sources/          # Mã nguồn chính
├── assets/           # Tài nguyên game
│   ├── img_spaceship/    # Hình ảnh tàu vũ trụ
│   ├── img_enemy/        # Hình ảnh kẻ thù
│   ├── img_background/   # Hình nền
│   ├── sound/           # Âm thanh
│   ├── map/             # Cấu hình màn chơi
│   └── Ship/            # Cấu hình tàu vũ trụ
└── requirements.txt  # Dependencies
```

## Yêu cầu hệ thống
- Python 3.7+
- Pygame 2.1.0+
- Windows/Linux/macOS


