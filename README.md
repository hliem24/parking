# 🚗 Smart Parking System - AI Parking Detection Project  

<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
   Smart Parking System - Computer Vision Project
</h2>

<div align="center">
    <p align="center">
        <img src="docs/aiotlab_logo.png" width="170"/>
        <img src="docs/fitdnu_logo.png" width="180"/>
        <img src="docs/dnu_logo.png" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

---

## 📝 1. Giới thiệu hệ thống

**Smart Parking System** là hệ thống giám sát bãi đỗ xe sử dụng **Computer Vision + Machine Learning**:

- 🔍 Phát hiện trạng thái ô đỗ (có xe / trống)
- 🎥 Hiển thị video realtime
- 📊 Ghi lịch sử xe vào/ra
- 🖼 Lưu ảnh khi xe rời bãi

---

## ⚙️ Cơ chế hoạt động

1. Video đầu vào (camera hoặc file)
2. Dùng mask xác định vị trí parking
3. AI phân loại:
   - 🟢 Trống
   - 🔴 Có xe
4. Khi xe rời:
   - Tính thời gian
   - Chụp ảnh
   - Ghi CSV
5. Web hiển thị realtime

---

## 🌟 Tính năng

- 🎥 Video realtime (Flask stream)
- 🧠 AI nhận diện bãi xe
- 📸 Lưu ảnh xe
- 📄 Log CSV
- 🌐 Web dashboard:
  - Xem video
  - Xem lịch sử
  - Tìm kiếm
  - Auto refresh

---

## 🛠 2. Công nghệ

- Python 3.10+
- OpenCV
- NumPy
- Scikit-learn (SVM)
- Flask

---

## 📂 3. Cấu trúc thư mục

- `app.py`: Tệp chạy Web Flask, hiển thị video realtime và lịch sử xe.
- `main.py`: Xử lý AI nhận diện bãi xe, theo dõi xe vào/ra và ghi log.
- `util.py`: Chứa các hàm xử lý model AI và xác định trạng thái ô đỗ.
- `log.csv`: File lưu lịch sử xe (thời gian đỗ, giờ vào/ra, ảnh).

- `model/`: Thư mục chứa model AI.
  - `model.p`: Model học máy dùng để phân loại ô đỗ (có xe / trống).

- `images/`: Thư mục lưu ảnh xe khi rời bãi.

- `templates/`: Thư mục giao diện web.
  - `index.html`: Trang dashboard hiển thị video và lịch sử.

- `mask_1920_1080.png`: Ảnh mask xác định vị trí các ô đỗ xe.

- `parking_1920_1080.mp4`: Video đầu vào dùng để test hệ thống.

## 🚀 4. Hình ảnh các chức năng

<p align="center">
  <img src="docs/project photo/1..png" alt="Ảnh 1" width="800"/>
</p>

<p align="center">
  <em>Các mode trong GAME  </em>
</p>

<p align="center">
  <img src="docs/project photo/2..png" alt="Ảnh 2" width="700"/>
</p>
<p align="center">
  <em>Client hướng dẫn  </em>
</p>


<p align="center">
  <img src="docs/project photo/3..png" alt="Ảnh 3" width="500"/>
 
</p>
<p align="center">
  <em> Client chơi màn  </em>
</p>

<p align="center">
    <img src="docs/project photo/4..png" alt="Ảnh 4" width="450"/>
</p>
<p align="center">
  <em> Giao diện khi vào chơi  </em>
</p>
<p align="center">
    <img src="docs/project photo/5...png" alt="Ảnh 5" width="450"/>
</p>
<p align="center">
  <em> Màn khi mình thua   </em>
</p>
<p align="center">
    <img src="docs/project photo/6..png" alt="Ảnh 6" width="450"/>
</p>
<p align="center">
  <em> Client thoại nhân vật    </em>
</p>
<p align="center">
    <img src="docs/project photo/7..png" alt="Ảnh 7" width="450"/>
</p>
<p align="center">
  <em> Giao diện màn đánh BOSS   </em>
</p>

## 📝 5. Hướng dẫn cài đặt và sử dụng

### 🔧 Yêu cầu hệ thống

- **Python**: Phiên bản 3.9 trở lên  
- **Hệ điều hành**: Windows 10/11 (khuyên dùng), macOS, hoặc Linux  
- **Môi trường phát triển**: IDE (VS Code, PyCharm) hoặc terminal/command prompt  
- **Bộ nhớ**: Tối thiểu 4GB RAM  
- **Phần cứng**: Không yêu cầu webcam (có thể dùng camera nếu mở rộng)  
- **Mạng**: Không yêu cầu (chạy Offline Local)  

---

### 📦 Cài đặt và triển khai

#### Bước 1: Chuẩn bị môi trường

1. **Kiểm tra Python**: Mở terminal/command prompt và chạy:

  - python --version  

2. **Cài đặt thư viện**: Chạy lệnh cài đặt các gói cần thiết:

  - pip install opencv-python numpy flask scikit-learn  

---

#### Bước 2: Kiểm tra cấu trúc thư mục

Đảm bảo các tệp tin được đặt đúng vị trí:

Các file logic:  
- `app.py`: Web server Flask  
- `main.py`: Xử lý video và ghi log  
- `util.py`: AI nhận diện bãi đỗ  

Dữ liệu AI:  
- `model/model.p`  

Tài nguyên:  
- `images/`: Lưu ảnh xe  
- `templates/index.html`: Giao diện web  
- `mask_1920_1080.png`  
- `parking_1920_1080.mp4`  
- `log.csv`  

3. **Kiểm tra kết quả**: Nếu chạy đúng, hệ thống sẽ tự tạo log và ảnh trong quá trình hoạt động.  

---

#### Bước 3: Chạy ứng dụng

**Khởi động hệ thống nhận diện và ghi lịch sử:**

- python main.py  

- Hệ thống sẽ:
  - Nhận diện xe vào/ra  
  - Tính thời gian đỗ  
  - Lưu ảnh vào thư mục `images/`  
  - Ghi dữ liệu vào `log.csv`  

**Khởi động giao diện web:**

- python app.py  

- Mở trình duyệt tại:  
  - http://127.0.0.1:5000  

---

### 🚀 Sử dụng ứng dụng

1. **Xem video realtime**  
   Hiển thị video bãi xe trực tiếp trên web (ô xanh = trống, ô đỏ = có xe).  

2. **Theo dõi trạng thái**  
   Hiển thị số lượng chỗ trống theo thời gian thực.  

3. **Xem lịch sử**  
   Hiển thị danh sách xe ra/vào gồm:
   - Vị trí  
   - Thời gian đỗ  
   - Giờ vào / giờ ra  
   - Ảnh xe  

4. **Tìm kiếm**  
   Nhập vị trí (VD: A10) để lọc dữ liệu nhanh.  

5. **Realtime**  
   Dữ liệu tự động cập nhật liên tục mà không cần reload trang.  

6. **Xem ảnh chi tiết**  
   Click vào ảnh để xem kích thước đầy đủ.  

## 👜Thông tin cá nhân
**Họ tên**: Nguyễn Hoàng Liêm.  
**Lớp**: CNTT 16-03.  
**Email**: liemnguyenhoang22@gmail.com.

© 2026 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

---
