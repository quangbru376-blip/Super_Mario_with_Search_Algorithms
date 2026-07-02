# 🍄 Super Mario AI Visualizer

Dự án **Super Mario AI Visualizer** là một ứng dụng mô phỏng các thuật toán Trí tuệ Nhân tạo cốt lõi thông qua giao diện đồ họa được xây dựng bằng `pygame`. Dự án được lấy cảm hứng từ thế giới của tựa game Super Mario nhằm giúp việc học tập và quan sát thuật toán trở nên sinh động và dễ dàng hơn.

---

![Demo Super Mario AI Visualizer](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/menu.gif)

---

## 🎮 Các Thế giới Mô phỏng (Worlds) & Thuật toán

Dự án được chia thành 6 Màn chơi khác nhau, mỗi màn chơi biểu diễn một nhóm thuật toán Tìm kiếm để giải quyết bài toán đặc trưng:

### 🌟 WORLD 1 & 2: Pathfinding (Tìm đường)
*Người chơi sẽ quan sát Mario tìm ra đường đi tới đích bằng các thuật toán tìm kiếm cơ bản và heuristic.*
- **Uninformed Search:**
1. ***Breatdh-First Search (BFS):*** Là thuật toán tìm kiếm theo chiều rộng, thuật toán duyệt qua các node theo từng độ sâu. Sử dụng Queue (FIFO) để lưu trữ dữ liệu.

![Demo BFS](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/bfs.gif)

2. ***Depth-First Search (DFS):*** Là thuật toán tìm kiếm theo chiều sâu, thuật toán sẽ duyệt một nhánh sâu nhất có thể trước khi quay lui. Sử dụng Stack (LIFO) để lưu trữ dữ liệu.

![Demo DFS](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/dfs.gif)

3. ***Uniform Cost Search (UCS):*** Là thuật toán tìm kiếm theo chi phí, thuật toán được mở rộng theo đường đi có chi phí thấp nhất. Sử dụng Priority Queue để ưu tiên các node chi phí thấp trước.

![Demo UCS](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/ucs.gif)

- **Informed Search:**

1. ***Greedy Best-First Search (GBFS):*** Là thuật toán tìm kiếm tham lam, bằng việc sử dụng hàm (heuristic) để đánh giá khoảng cách Manhattan từ vị trí hiện tại tới đích, thuật toán sẽ ưu tiên chọn tuyến đường nhanh nhất nhưng không hẳn là tối ưu nhất.

![Demo GREEDY](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/greedy.gif)

2. ***A\* Search:*** Là thuật toán tìm kiếm thông minh bằng cách sử dụng hàm *f(n) = g(n) + h(n)* với g(n) để đánh giá chi phí và h(n) để đánh giá khoảng cách Manhattan tới đích. Thuật toán sẽ tìm ra đường vừa ngắn và vừa tốn ít chi phi nhất.

![Demo AStar](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/astar.gif)

3. ***IDA*:*** Là thuật toán kết hợp giữa sự tối ưu của **A\*** và sự tiết kiệm không gian bộ nhớ của **DFS**. Thuật toán sẽ tìm kiếm với độ sâu tăng dần theo các ngưỡng chi phí lấy từ hàm *f(n)*

![Demo IDAStar](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/idastar.gif)

### 🌟 WORLD 3: Local Search (Tìm kiếm cục bộ)
*Mario sẽ sử dụng các thuật toán tìm kiếm cục bộ để tìm đường lên đỉnh núi với từng độ cao được đánh số từ 0-9.*
1. ***Simple Hill Climbing:*** Là một trong bốn loại thuật toán leo đồi, thuật toán sẽ liên tục di chuyển tới các hàng xóm có giá trị mục tiêu tốt hơn và dừng lại khi bị kẹt đỉnh cục bộ.

![Demo Simple Hill](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/simple.gif)

2. ***Simulated Annealing:*** Là một thuật toán tìm kiếm cục bộ lấy cảm hứng từ việc luyện kim. Thuật toán sẽ chấp nhận giá trị mục tiêu thấp hơn để thoát khỏi đỉnh cục bộ với khả năng chấp nhận giảm dần theo thời gian.

![Demo Simulated](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/simulated.gif)

3. ***Local Beam Search:*** Là thuật toán tìm kiếm cục bộ được cải tiến từ thuật toán leo đồi. Thuật toán sẽ giữ lại k trạng thái tốt nhất và mở rộng đồng thời các trạng thái. Thuật toán sẽ giảm khả năng bị kẹt ở đỉnh cục bộ với việc khám phá nhiều hướng cùng lúc.

![Demo Beam](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/beam.gif)

### 🌟 WORLD 4: Complex Env (Môi trường phức tạp)
*Mario phải sử dụng thuật toán để tìm đường nhặt hết xu trong môi trường không chắc chắn, bị sương mù che khuất hoặc không biết rõ vị trí của mình.*
1. ***Sensorless Search:*** Là thuật toán giải quyết bài toán khi Mario bị "mù" hoàn toàn thông tin về vị trí. Thay vì tìm kiếm trên các trạng thái đơn lẻ, thuật toán thao tác trên các tập belief states, từ đó đưa ra một chuỗi hành động đảm bảo Mario chắc chắn đến đích dù ban đầu đang đứng ở bất kỳ đâu.

![Demo Sensorless](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/sensorless.gif)

2. ***Partially Observable:*** Là phương pháp áp dụng khi tầm nhìn của Mario bị giới hạn. Dựa vào các thông tin thu thập được từ cảm biến (sensor) tại mỗi bước đi, thuật toán sẽ liên tục cập nhật, suy luận vị trí hiện tại trong "đa vũ trụ" các khả năng để ra quyết định di chuyển tiếp theo một cách hợp lý nhất.

![Demo Partially](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/partially.gif)

3. ***And-Or Search:*** Là thuật toán lập kế hoạch dành cho môi trường phi định định (nondeterministic), nơi một hành động có thể dẫn đến nhiều kết quả khác nhau. Thuật toán sẽ lập ra một kế hoạch dự phòng dạng cây And-Or để đảm bảo Mario luôn có phương án xử lý mọi cạm bẫy có thể xảy ra.

![Demo AndOr](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/andor.gif)

### 🌟 WORLD 5: CSP Solver (Bài toán thỏa mãn ràng buộc)
*Sử dụng các ràng buộc của bài toán, Mario tô màu các ô bản đồ sao cho thỏa mãn ràng buộc.*
1. ***Backtracking Search***: Là một dạng tìm kiếm theo chiều sâu chuyên dụng cho CSP. Thuật toán sẽ thử gán màu cho từng ô bản đồ một, nếu phát hiện một ô vi phạm ràng buộc, nó sẽ quay lui bước trước đó để thử một màu khác.

![Demo Backtracking](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/backgif)

2. ***Forward Checking***: Là kỹ thuật tối ưu hóa kết hợp với **Backtracking**. Mỗi khi Mario tô một màu, thuật toán sẽ nhìn trước và loại bỏ màu đó khỏi danh sách các màu hợp lệ của các ô lân cận chưa được tô. Điều này giúp phát hiện sớm các ngõ cụt và giảm thiểu đáng kể số lần quay lui.

![Demo Forward Checking](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/forward.gif)

3. ***Min Conflicts***: Là thuật toán tìm kiếm cục bộ cho CSP. Thuật toán bắt đầu bằng cách gán màu ngẫu nhiên cho toàn bộ bản đồ. Sau đó ở mỗi bước, Mario sẽ chọn lại màu cho một ô đang bị vi phạm sao cho số lượng xung đột giảm xuống mức thấp nhất cho đến khi bài toán được giải.

![Demo Min Conflicts](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/min.gif)

### 🌟 WORLD 6: Boss Battle (Đối kháng)
*Mario sẽ đối đầu với Boss Bowser được lập trình sử dụng các thuật toán đối kháng qua trò chơi Cờ Caro 3x3.*
1. ***Minimax***: Là thuật toán ra quyết định dựa trên cây trò chơi, giả định cả Mario (MAX) và Bowser (MIN) đều chơi một cách hoàn hảo nhất. Thuật toán sẽ duyệt qua toàn bộ các diễn biến có thể xảy ra, sau đó chọn nước đi tối đa hóa lợi thế cho bản thân và tối thiểu hóa lợi thế của đối thủ.

![Demo Minimax](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/minimax.gif)

2. ***Alpha-Beta Pruning***: Là một bản nâng cấp tối ưu của Minimax. Bằng cách sử dụng hai tham số Alpha và Beta để theo dõi điểm số, thuật toán sẽ cắt bỏ những nhánh cây trò chơi chắc chắn không làm thay đổi kết quả cuối cùng. Điều này giúp Bowser tính toán nước đi nhanh hơn và nhìn sâu hơn vào tương lai.

![Demo Alpha Beta](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/alphabeta.gif)

3. ***Expectimax***: Là thuật toán áp dụng khi đối thủ không hành động hoàn hảo hoặc môi trường có yếu tố ngẫu nhiên. Thay vì luôn chọn giá trị xấu nhất do đối thủ gây ra (MIN), thuật toán sẽ tính *giá trị kỳ vọng* của các nhánh con để đưa ra quyết định linh hoạt và thực tế hơn.

![Demo Expectimax](https://github.com/quangbru376-blip/Super_Mario_with_Search_Algorithms/blob/main/gif/expectimax.gif)

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
