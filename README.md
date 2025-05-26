# BKFood - Nền tảng chia sẻ trải nghiệm và quản lý dịch vụ
- [Giới thiệu](#angel-giới-thiệu)
- [Cài đặt](#gear-cài-đặt)
- [Cách sử dụng](#anchor-cách-sử-dụng)
- [Tính năng chính](#anger-tính-năng-chính)

## :angel: Giới thiệu


## :gear: Cài đặt

### 1. Clone dự án từ GitHub:
- Tải dự án về thiết bị của bạn:
    ```bash
    git clone https://github.com/bachthetrollface/SoftwareEngineering-BKFood.git
    ```
- Tới thư mục làm việc của dự án:
    ```bash
    cd SoftwareEngineering-BKFood
    ```
    
### 2. Cài đặt môi trường :
- Dự án cần tới nhiều thư viện liên quan. Hãy dùng lệnh sau để thiết lập môi trường để dự án có thể hoạt động:
    ```bash
    pip install -r requirements.txt
    ```

## :anchor: Cách sử dụng:
  - Kết nối hệ thống với cơ sở dữ liệu đã có sẵn (cập nhật cấu trúc cơ sở dữ liệu):
    ```bash
    # move to Django\'s working directory
    cd bkfood
    ```
    ```bash
    python3 manage.py makemigrations homepage
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
  - Khởi chạy máy chủ bằng lệnh dưới đây và ấn vào địa chỉ bên dưới để truy cập web BKFood.
    ```bash
    python3 manage.py runserver
    ```
  - you may need to use `py` or `python` instead of `python3` for above commands, depending on your OS

## :anger: Tính năng chính: 
### HOMEPAGE:
  - Đăng kí/ Đăng nhập: (bạn cần tạo, nhập mật khẩu >= 8 kí tự)
  - Phần header
  - Hiển thị top dịch vụ theo số sao đã được vote
  - Hiển thị top bài viết có nhiều like nhất
  - Tìm kiếm sản phẩm/dịch vụ:
    - Tìm kiếm nhanh tại header: (Nhập từ khóa bạn muốn tìm kiếm và click search, sẽ được chuyển tới mục tìm kiếm)
    - Tìm kiếm:
      - Theo tag: chọn lọc (phân loại) và sau đó click vào các tag tương ứng.
      - Tìm kiếm và lọc: Nhập từ khóa (có thể thêm các thao tác chọn phân loại, chọn khu vực, thời gian) -> sau đó click search.
    - Kết quả tìm kiếm sẽ được hiển thị bên cạnh, bạn có thể đi tới xem chi tiết hoặc thêm vào giỏ hàng.
### POSTSPAGE: 
  - Bài viết:
    - Hiển thị các bài viết theo thời gian
    - Like và comment
    - Tìm kiếm bài viết
  - restaurant:
    - Hiển thị thông tin cơ bản về nơi cung cấp dịch vụ
### PROFILEPAGE:
  - Hiển thị thông tin cơ bản
  - Hiển thị sản phẩm (đối với cửa hàng)
  - Hiển thị bài viết
  - Đánh giá cửa hàng:
    - Hiển thị số sao đã đánh giá cho cửa hàng
    - Hiển thị số sao của cửa hàng
### SETTINGSPAGE: 
  - Chỉnh sửa thông tin
  - Tạo sản phẩm
  - Tạo bài viết
  - General
  - Product
  - Post (Chỉnh lại giao diện thêm và chỉnh bài viết cho giống giao diện khi mà bài viết được hiện thị)
