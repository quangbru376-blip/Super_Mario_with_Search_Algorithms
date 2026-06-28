# 🍄 Super Mario AI Visualizer

Chào mừng bạn đến với dự án **Super Mario AI Visualizer**! Đây là một ứng dụng mô phỏng trực quan các thuật toán Trí tuệ Nhân tạo (Artificial Intelligence) cốt lõi thông qua giao diện đồ họa được xây dựng bằng `pygame`. Dự án lấy cảm hứng từ thế giới của tựa game Super Mario nổi tiếng nhằm giúp việc học và quan sát thuật toán trở nên sinh động và dễ hiểu hơn.

---

## 🎮 Các Thế giới Mô phỏng (Worlds) & Thuật toán

Dự án được chia thành các "World" (Màn chơi) khác nhau, mỗi màn biểu diễn một nhóm thuật toán Tìm kiếm và Giải quyết vấn đề đặc trưng:

### 🌟 WORLD 1 & 2: Pathfinding (Tìm đường)
*Người chơi sẽ quan sát Mario tìm con đường đi thu thập xu hoặc giải cứu công chúa bằng các thuật toán tìm kiếm cơ bản và heuristic.*
- **Uninformed Search:** Breatdh-First Search (BFS), Depth-First Search (DFS), Uniform Cost Search (UCS)
- **Informed Search:** Greedy Best-First Search (GBFS), A* Search, IDA*

### 🌟 WORLD 3: Local Search (Tìm kiếm cục bộ)
*Mô phỏng thuật toán tối ưu hóa trạng thái cục bộ để vượt qua các chướng ngại vật/địa hình.*
- Simple Hill Climbing (Leo đồi)
- Simulated Annealing (Luyện kim)
- Local Beam Search

### 🌟 WORLD 4: Complex Env (Môi trường phức tạp)
*Mario phải hoạt động trong môi trường không chắc chắn, có sương mù che khuất hoặc không biết rõ vị trí của mình.*
- **Sensorless Search:** (Không cảm biến) Tìm đường đi mù qua tập các trạng thái (belief state).
- **Partially Observable:** (Quan sát một phần) Đa vũ trụ, suy luận vị trí dựa trên cảm biến.
- **And-Or Search:** Lập kế hoạch phi định định (nondeterministic) đề phòng cạm bẫy.

### 🌟 WORLD 5: CSP Solver (Bài toán thỏa mãn ràng buộc)
*Áp dụng ràng buộc để Mario sắp xếp các đồ vật hoặc giải bài toán Sudoku/Graph Coloring (tương tự).*
- Backtracking Search
- Forward Checking
- Min Conflicts

### 🌟 WORLD 6: Boss Battle (Đối kháng)
*Mario sẽ đối đầu với Boss Bowser qua trò chơi Cờ Caro (Tic-Tac-Toe) 3x3.*
- Minimax
- Alpha-Beta Pruning (Tỉa nhánh Alpha-Beta)
- Expectimax

---

## 🛠 Hướng dẫn Cài đặt & Chạy ứng dụng

### Yêu cầu hệ thống
- Python 3.8 trở lên.

### Bước 1: Clone dự án hoặc tải mã nguồn về máy
```bash
git clone <url-repo-cua-ban>
cd Final_project_pygame
```

### Bước 2: Cài đặt các thư viện phụ thuộc
Sử dụng `pip` để cài đặt các package cần thiết (như `pygame`, `opencv-python`, ...):
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng
Khởi động giao diện chính của chương trình:
```bash
python main.py
```
*(Bạn cũng có thể chạy bằng file `run_game.bat` trên Windows hoặc `run_game.sh` trên Linux/macOS).*

---

## 📂 Cấu trúc Thư mục

```text
Final_project_pygame/
│
├── algorithms/           # Cài đặt các thuật toán AI
│   ├── core.py           # Các lớp cơ sở (Node, Problem, Game)
│   ├── pathfinding.py    # BFS, DFS, UCS, A*, GBFS
│   ├── local_search.py   # Hill Climbing, Simulated Annealing
│   ├── complex_env.py    # Sensorless, Partially Observable, And-Or Search
│   ├── csp.py            # Backtracking, Forward Checking, Min Conflicts
│   └── adversarial.py    # Minimax, Alpha-Beta Pruning, Expectimax
│
├── worlds/               # Giao diện đồ họa Pygame mô phỏng từng thế giới
│   ├── base_world.py     # Lớp cha BasePyGameWorld chứa giao diện dùng chung
│   ├── maze_world.py     # (World 1 & 2) Mô phỏng Pathfinding
│   ├── local_world.py    # (World 3) Mô phỏng Local Search
│   ├── fog_world.py      # (World 4) Mô phỏng Complex Env
│   ├── csp_world.py      # (World 5) Mô phỏng Constraint Satisfaction
│   └── boss_world.py     # (World 6) Mô phỏng Adversarial Search (Caro 3x3)
│
├── resources/            # Tài nguyên đồ họa (hình ảnh Mario, coin, gạch...) và video nền
├── scratch/              # Thư mục nháp (có thể tạo ra trong quá trình gỡ lỗi hoặc phát triển)
│
├── main.py               # File khởi chạy chính, chứa menu tổng chọn các World
├── config.py             # Cấu hình chung về hằng số, bản đồ (maps), màu sắc, tải Asset
├── ui.py                 # Các thành phần giao diện UI dùng chung (Button, ComboBox, LogPanel)
├── run_game.bat          # Script chạy ứng dụng nhanh trên Windows
├── run_game.sh           # Script chạy ứng dụng nhanh trên Linux/macOS
└── requirements.txt      # Danh sách thư viện Python cần thiết
```

---

**Chúc bạn có những trải nghiệm thú vị với Trí tuệ Nhân tạo trong thế giới của Super Mario! 🍄✨**
