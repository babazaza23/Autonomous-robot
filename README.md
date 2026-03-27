# Autonomous-robot
Để đăng tải tài liệu lên GitHub, ngôn ngữ chuẩn và thông dụng nhất là **Markdown** (định dạng file `.md`) chứ không phải LaTeX. GitHub được thiết kế để tự động biên dịch các đoạn mã Markdown thành giao diện văn bản có tiêu đề, danh sách và in đậm rất trực quan và đẹp mắt.

Dưới đây là toàn bộ nội dung hướng dẫn được viết bằng mã Markdown. Bạn chỉ cần copy toàn bộ đoạn mã trong khung dưới đây, tạo một file có tên là `README.md` trên kho lưu trữ (repository) GitHub của bạn và dán vào:

# Hướng Dẫn Cài Đặt Hệ Thống Robot Tự Hành Dò Line & Né Vật Cản (Raspberry Pi 3 + OpenCV)

Tài liệu này hướng dẫn chi tiết các bước thiết lập từ số 0 để chạy mã nguồn nhận diện vạch kẻ đường, phát hiện vật cản bằng cảm biến siêu âm và điều khiển động cơ trên Raspberry Pi 3 Model B.

## 🛠 1. Yêu Cầu Phần Cứng
- Mạch Raspberry Pi 3 Model B v1.2 + Thẻ nhớ Micro-SD (tối thiểu 16GB).
- Nguồn cấp: Củ sạc 5V có dòng ra từ 2.5A trở lên (cần cáp Micro-USB lõi to, chất lượng tốt để tránh sụt áp).
- Webcam chuẩn kết nối USB (Khuyên dùng: Logitech C270).
- Cảm biến siêu âm HC-SR04 + 2 Điện trở (1kΩ và 2kΩ) để làm mạch hạ áp.
- Mạch công suất điều khiển động cơ ZY Electronics (L298N) + Khung xe robot 2 bánh.

## 🚀 2. Cài Đặt Hệ Điều Hành Lên Thẻ Nhớ (Thao tác trên Laptop)
1. Tải phần mềm **Raspberry Pi Imager** từ trang chủ và cài đặt vào máy tính.
2. Tại giao diện phần mềm, chọn **OS**: `Raspberry Pi OS (32-bit)`.
3. Chọn **Storage**: Thẻ nhớ Micro-SD của bạn.
4. Nhấn vào biểu tượng **Bánh răng cưa (Edit Settings)** để mở cấu hình nâng cao:
   - **Tab General**: Tích chọn thiết lập *Username* và *Password* (Ví dụ user: `pi` và pass: `123456`). Hãy ghi nhớ kỹ thông tin này. Đặt Hostname là `raspberrypi`.
   - **Tab Wi-Fi**:
     - *Trường hợp cắm cáp mạng LAN trực tiếp vào Pi*: Để trống toàn bộ thông tin SSID và Password ở tab này.
     - *Trường hợp dùng Wi-Fi*: Tích chọn cấu hình LAN, nhập chính xác Tên và Mật khẩu Wi-Fi nhà bạn (Lưu ý: Pi 3 chỉ nhận sóng 2.4GHz, không nhận sóng 5GHz).
   - **Tab Remote Access**: Bắt buộc phải tích chọn **Enable SSH** và **Use password authentication**.
5. Bấm **NEXT** -> **WRITE** và chờ phần mềm ghi xong hệ điều hành.

## 🔌 3. Sơ Đồ Nối Dây Phần Cứng

**A. Module Động Cơ (ZY Electronics / L298N):**
- `IN1` -> GPIO 17 
- `IN2` -> GPIO 18 
- `ENA` -> GPIO 22 *(Bắt buộc phải rút bỏ Jumper ENA trên mạch L298N ra trước khi cắm dây vào)*
- `IN3` -> GPIO 23 
- `IN4` -> GPIO 24 
- `ENB` -> GPIO 25 *(Bắt buộc phải rút bỏ Jumper ENB)*
- Nối chung một dây từ chân `GND` của mạch động cơ vào chân `GND` của Raspberry Pi.

**B. Cảm Biến Siêu Âm HC-SR04 (LƯU Ý: Nối sai có thể gây cháy mạch Pi):**
- `VCC` -> Chân 5V của Pi.
- `GND` -> Chân GND của Pi.
- `TRIG` -> GPIO 5.
- `ECHO` -> **BẮT BUỘC SỬ DỤNG MẠCH CHIA ÁP BẰNG ĐIỆN TRỞ**:
  - Lấy điện trở 1kΩ: Nối 1 đầu vào chân ECHO của cảm biến, đầu còn lại nối vào chân **GPIO 6** trên Pi.
  - Lấy điện trở 2kΩ: Nối 1 đầu cắm chung vào **GPIO 6**, đầu còn lại nối xuống chân **GND** của Pi.

## 🖥️ 4. Khởi Động & Truy Cập Raspberry Pi
Lắp thẻ nhớ, cắm Webcam vào cổng USB, cắm dây mạng LAN (nếu có dùng), sau đó cắm cáp nguồn và chờ khoảng 3 phút để hệ thống khởi động.

### Tùy chọn A: Dành cho thiết lập KHÔNG CÓ màn hình rời (Headless Setup)
1. Đảm bảo Laptop và Pi đang được kết nối chung một mạng.
2. Trên Laptop, mở Terminal (hoặc Command Prompt trên Windows), gõ lệnh:bash
   ssh pi@raspberrypi.local
   ```
   *(Thay chữ `pi` bằng username bạn đã đặt ở bước 2)*
3. Gõ `yes` nếu hệ thống cảnh báo bảo mật, sau đó nhập Mật khẩu (Lưu ý: Mật khẩu khi gõ sẽ tàng hình, bạn cứ gõ đúng rồi ấn Enter).
4. Khi đã vào được môi trường lệnh của Pi, gõ tiếp: `sudo raspi-config`
5. Trong bảng cài đặt màu xanh dương, sử dụng phím mũi tên chọn **Interface Options** -> **VNC** -> **Yes** -> **Finish**.
6. Tải và mở phần mềm **RealVNC Viewer** trên Laptop. Nhập địa chỉ `raspberrypi.local` vào thanh tìm kiếm, điền username/password để hiển thị giao diện Desktop ảo của Raspberry Pi lên Laptop.

### Tùy chọn B: Dành cho thiết lập CÓ màn hình rời
1. Cắm cáp HDMI từ bo mạch Raspberry Pi vào màn hình máy tính/TV. 
2. Cắm chuột và bàn phím vào các cổng USB của Pi.
3. Giao diện Desktop sẽ hiển thị. Nhấp vào biểu tượng Wi-Fi ở góc phải phía trên màn hình để kết nối mạng (nếu bạn không cắm dây LAN).

## ⚙️ 5. Cài Đặt Thư Viện & Chạy Code 
*Các thao tác dưới đây thực hiện trực tiếp trên giao diện Desktop của Raspberry Pi (hoặc qua cửa sổ RealVNC Viewer).*

1. Mở ứng dụng **Terminal** (biểu tượng màn hình màu đen trên thanh menu) và cập nhật hệ thống:
   ```bash
   sudo apt-get update
   ```
2. Cài đặt thư viện xử lý ảnh OpenCV và mảng toán học Numpy:
   ```bash
   sudo apt-get install python3-opencv python3-numpy -y
   ```
3. Mở phần mềm lập trình: Bấm vào **Menu Start (Logo quả mâm xôi góc trái)** -> Chọn **Programming** -> Mở **Thonny Python IDE**.
4. Dán toàn bộ mã nguồn điều khiển robot vào khung soạn thảo của Thonny. Bấm nút **Save** và lưu ra ngoài Desktop.
5. Đặt xe robot lên sa bàn có vạch line đen. Bấm nút **Run** (biểu tượng Play màu xanh lá cây) trên Thonny để kích chạy hệ thống. 
6. *Mẹo an toàn:* Để dừng động cơ và tắt chương trình, dùng chuột nhấp vào cửa sổ đang hiển thị camera và bấm phím `q` trên bàn phím.
```
