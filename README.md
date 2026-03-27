# Autonomous-robot
# Hướng Dẫn Cài Đặt Hệ Thống Robot Tự Hành Dò Line & Né Vật Cản (Raspberry Pi 3 + OpenCV)

Tài liệu này hướng dẫn chi tiết các bước thiết lập từ số 0 để chạy mã nguồn nhận diện vạch kẻ đường, phát hiện vật cản bằng cảm biến siêu âm và điều khiển động cơ trên Raspberry Pi 3 Model B.
## 1. Cài Đặt Hệ Điều Hành Lên Thẻ Nhớ (Thao tác trên Laptop)
1. Tải phần mềm **Raspberry Pi Imager** từ trang chủ và cài đặt vào máy tính.
2. Tại giao diện phần mềm, chọn **OS**: `Raspberry Pi OS (32-bit)`.
3. Chọn **Storage**: Thẻ nhớ Micro-SD của bạn.
4. Nhấn vào biểu tượng **Bánh răng cưa (Edit Settings)** để mở cấu hình nâng cao:
   - **Tab General**: Tích chọn thiết lập *Username* và *Password* (Ví dụ user: `pi` và pass: `123`). Hãy ghi nhớ kỹ thông tin này. Đặt Hostname là `raspberrypi`.
   - **Tab Wi-Fi**:
     - *Trường hợp cắm cáp mạng LAN trực tiếp vào Pi*: Để trống toàn bộ thông tin SSID và Password ở tab này.
     - *Trường hợp dùng Wi-Fi*: Tích chọn cấu hình LAN, nhập chính xác Tên và Mật khẩu Wi-Fi nhà bạn (Lưu ý: Pi 3 chỉ nhận sóng 2.4GHz, không nhận sóng 5GHz).
   - **Tab Remote Access**: Bắt buộc phải tích chọn **Enable SSH** và **Use password authentication**.
5. Bấm **NEXT** -> **WRITE** và chờ phần mềm ghi xong hệ điều hành.

## 🖥️ 2. Khởi Động & Truy Cập Raspberry Pi
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
