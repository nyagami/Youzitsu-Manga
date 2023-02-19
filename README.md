# Youzitsu Manga
Kế thừa từ mã nguồn của <a href="https://github.com/subject-f/guyamoe">Guya.moe</a>

⚠ **Note:** Hướng dẫn cài bên dưới sẽ không được áp dụng cho mọi truyện khác,
vì nó chứa nhiều phần code liên quan đến bộ Kaguya-sama: Love is War.

## Yêu cầu 
- git
- python 3.6.5+
- pip
- virtualenv

## Cài đặt
1. Tạo một môi trường ảo cho project.
```
virtualenv venv
```

2. Clone Guyamoe's source code.
```
git clone https://github.com/appu1232/guyamoe app
```

3. Activate the venv.
```
source ./venv/bin/activate
```

4. Install Guyamoe's dependencies.
```
cd app/
pip3 install -r requirements.txt
```

5. Thay đổi `SECRET_KEY` thành một mã hash ngẫu nhiên.
```
sed -i "s|\"o kawaii koto\"|\"$(openssl rand -base64 32)\"|" guyamoe/settings/base.py
```

6. Chạy bộ assets để test (của guya.moe).
```
python3 init.py
```

Lưu ý: cần phải migrate models của django (chạy lệnh makemigrations, migrate)

7. Tạo superuser.
```
python3 manage.py createsuperuser
```

Cấu trúc của thư mục chứa file ảnh của manga trông như này
```
media
└───manga
    └───<series-slug-name>
        └───001
            ├───001.jpg
            ├───002.jpg
            └───...
```
Ví dụ: `Kaguya-Wants-To-Be-Confessed-To` là `<series-slug-name>`. 

**Note:** Chapter có zero padding: `001`.
Đối với ảnh thì không quan trọng extension (Ví dụ `.jpeg`). Chỉ cần xếp theo thứ tự là dạng số (tự nhiên) hoặc xếp theo alphabet (Ví dụ: `ab` sẽ xếp trước `b`)

## Chạy server
-  `python3 manage.py runserver`

Giờ web có thể xem được trên localhost:8000

## Thông tin khác
Các URL: 

- `/` - home page
- `/about` - about page
- `/admin` - admin view (Đăng nhập bằng user trên)
- `/admin_home` - admin để clear cache
- `/reader/series/<series_slug_name>` - series info and all chapter links
- `/reader/series/<series_slug_name>/<chapter_number>/<page_number>` - cấu trúc của URL cho từng trang truyện
- `/api/series/<series_slug_name>` - API toàn bộ series
- `/media/manga/<series_slug_name>/<chapter_number>/<page_file_name>` - URL cho file ảnh