# 🍄 Super Mario AI Visualizer

Chào mừng bạn đến với dự án **Super Mario AI Visualizer**! Đây là một ứng dụng mô phỏng trực quan các thuật toán Trí tuệ Nhân tạo (Artificial Intelligence) cốt lõi thông qua giao diện đồ họa được xây dựng bằng `pygame`. Dự án được lấy cảm hứng từ thế giới của tựa game Super Mario nhằm giúp việc học tập và quan sát thuật toán trở nên sinh động và dễ dàng hơn.

---

## 🎮 Các Thế giới Mô phỏng (Worlds) & Thuật toán

Dự án được chia thành 6 Màn chơi khác nhau, mỗi màn chơi biểu diễn một nhóm thuật toán Tìm kiếm để giải quyết bài toán đặc trưng:

### 🌟 WORLD 1 & 2: Pathfinding (Tìm đường)
*Người chơi sẽ quan sát Mario tìm ra đường đi tới đích bằng các thuật toán tìm kiếm cơ bản và heuristic.*
- **Uninformed Search:**
1. ***Breatdh-First Search (BFS):*** Là thuật toán tìm kiếm theo chiều rộng, thuật toán duyệt qua các node theo từng độ sâu. Sử dụng Queue (FIFO) để lưu trữ dữ liệu.
2. ***Depth-First Search (DFS):*** Là thuật toán tìm kiếm theo chiều sâu, thuật toán sẽ duyệt một nhánh sâu nhất có thể trước khi quay lui. Sử dụng Stack (LIFO) để lưu trữ dữ liệu.
3. ***Uniform Cost Search (UCS):*** Là thuật toán tìm kiếm theo chi phí, thuật toán được mở rộng theo đường đi có chi phí thấp nhất. Sử dụng Priority Queue để ưu tiên các node chi phí thấp trước.
- **Informed Search:**
1. ***Greedy Best-First Search (GBFS):*** Là thuật toán tìm kiếm tham lam, bằng việc sử dụng hàm (heuristic) để đánh giá khoảng cách Manhattan từ vị trí hiện tại tới đích, thuật toán sẽ ưu tiên chọn tuyến đường nhanh nhất nhưng không hẳn là tối ưu nhất.
2. ***A\* Search:*** Là thuật toán tìm kiếm thông minh bằng cách sử dụng hàm *f(n) = g(n) + h(n)* với g(n) để đánh giá chi phí và h(n) để đánh giá khoảng cách Manhattan tới đích. Thuật toán sẽ tìm ra đường vừa ngắn và vừa tốn ít chi phi nhất.
3. ***IDA*:*** Là thuật toán kết hợp giữa sự tối ưu của **A\*** và sự tiết kiệm không gian bộ nhớ của **DFS**. Thuật toán sẽ tìm kiếm với độ sâu tăng dần theo các ngưỡng chi phí lấy từ hàm *f(n)*

### 🌟 WORLD 3: Local Search (Tìm kiếm cục bộ)
*Mario sẽ sử dụng các thuật toán tìm kiếm cục bộ để tìm đường lên đỉnh núi với từng độ cao được đánh số từ 0-9.*
1. ***Simple Hill Climbing:*** Là một trong bốn loại thuật toán leo đồi, thuật toán sẽ liên tục di chuyển tới các hàng xóm có giá trị mục tiêu tốt hơn và dừng lại khi bị kẹt đỉnh cục bộ.
2. ***Simulated Annealing:*** Là một thuật toán tìm kiếm cục bộ lấy cảm hứng từ việc luyện kim. Thuật toán sẽ chấp nhận giá trị mục tiêu thấp hơn để thoát khỏi đỉnh cục bộ với khả năng chấp nhận giảm dần theo thời gian.
3. ***Local Beam Search:*** Là thuật toán tìm kiếm cục bộ được cải tiến từ thuật toán leo đồi. Thuật toán sẽ giữ lại k trạng thái tốt nhất và mở rộng đồng thời các trạng thái. Thuật toán sẽ giảm khả năng bị kẹt ở đỉnh cục bộ với việc khám phá nhiều hướng cùng lúc.

### 🌟 WORLD 4: Complex Env (Môi trường phức tạp)
*Mario phải sử dụng thuật toán để tìm đường nhặt hết xu trong môi trường không chắc chắn, bị sương mù che khuất hoặc không biết rõ vị trí của mình.*
- **Sensorless Search:** (Không cảm biến) Tìm đường đi mù qua tập các trạng thái (belief state).
- **Partially Observable:** (Quan sát một phần) Đa vũ trụ, suy luận vị trí dựa trên cảm biến.
- **And-Or Search:** Lập kế hoạch phi định định (nondeterministic) đề phòng cạm bẫy.

### 🌟 WORLD 5: CSP Solver (Bài toán thỏa mãn ràng buộc)
*Sử dụng các ràng buộc của bài toán, Mario tô màu các ô bản đồ sao cho thỏa mãn ràng buộc.*
- Backtracking Search
- Forward Checking
- Min Conflicts

### 🌟 WORLD 6: Boss Battle (Đối kháng)
*Mario sẽ đối đầu với Boss Bowser được lập trình sử dụng các thuật toán đối kháng qua trò chơi Cờ Caro 3x3.*
- Minimax
- Alpha-Beta Pruning (Tỉa nhánh Alpha-Beta)
- Expectimax

---

## 🛠 Hướng dẫn Cài đặt & Chạy ứng dụng

### Yêu cầu hệ thống
- Python 3.8 trở lên.

### Bước 1: Clone dự án hoặc tải mã nguồn về máy
```bash
git clone https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms.git
cd Final_project_pygame
```

### Bước 2: Chạy ứng dụng
Khởi động giao diện chính của chương trình, 2 file điểm vào chương trình sau đã tích hợp sẵn trình kiểm tra thư viện, khởi tạo môi trường ảo (venv) và chạy chương trình

```bash
run_game.bat
```
Cho Windows hoặc
```bash
run_game.sh
```
Cho Linux/macOS

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
│
├── main.py               # File khởi chạy chính, chứa menu tổng chọn các World
├── config.py             # Cấu hình chung về hằng số, bản đồ (maps), màu sắc, tải Asset
├── ui.py                 # Các thành phần giao diện UI dùng chung (Button, ComboBox, LogPanel)
├── run_game.bat          # Script chạy ứng dụng nhanh trên Windows
├── run_game.sh           # Script chạy ứng dụng nhanh trên Linux/macOS
└── requirements.txt      # Danh sách thư viện Python cần thiết
```

---

**Chúc bạn có những trải nghiệm thú vị khi sử dụng các thuật toán Trí tuệ Nhân tạo trong thế giới của Super Mario! 🍄✨**
=======
