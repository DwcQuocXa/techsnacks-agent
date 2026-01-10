# [#TechSnack 07] | Apollo Client – Cache khiến Frontend "nhẹ đầu" hơn rất nhiều

Ae làm Frontend chắc không lạ gì cảnh: fetch data xong, cất vào Redux hay Zustand cho "chắc cú", rồi lại loay hoay sync data khi có update. Re-fetch liên tục thì UI lag, mà không re-fetch thì data lại cũ mèm.

Đây là bài mở đầu cho series **Apollo for GraphQL**. Hôm nay mình sẽ tập trung vào **Apollo Client** và vũ khí lợi hại nhất của nó: **Apollo Cache**.

## Apollo Client là gì?

Apollo Client là một thư viện quản lý state cho JavaScript, được thiết kế đặc biệt để làm việc với GraphQL. Nó không chỉ đơn thuần là một HTTP client để gọi API, mà còn lo luôn việc caching, state management, và UI updates.

Nói cách khác, ae có thể coi Apollo Client như "Redux + React Query" nhưng được tối ưu riêng cho GraphQL. Thay vì tự viết reducer, action, selector loằng ngoằng, Apollo lo hết – ae chỉ cần viết query và dùng.

## Normalized Cache hoạt động như thế nào?

Đây mới là "sauce" bí mật của Apollo. Cache của nó hoạt động như một "local graph database". Thay vì lưu JSON thô, nó băm nhỏ data thành các object phẳng (flat lookup table) dựa trên `__typename` và `id`.

Nhờ cơ chế này, cùng một entity (ví dụ `User:1`) dù xuất hiện ở Dashboard hay Profile page thì cũng chỉ có một bản duy nhất trong cache. Khi ae thực hiện một mutation và server trả về ID đó, Apollo tự động merge field mới và broadcast update cho toàn bộ UI đang lắng nghe.

## Fetch Policy – Điểm cộng lớn nhất

Với `cache-first`, app của bạn sẽ phản hồi ngay lập tức nếu data đã có sẵn. Hoặc với `cache-and-network`, người dùng thấy data cũ ngay và app tự cập nhật bản mới nhất ngầm bên dưới – UX cực kỳ mượt mà.

Sử dụng Apollo Cache đúng cách giúp ae dẹp bỏ được đống boilerplate quản lý state phức tạp. Những tính năng "khó nhằn" như Optimistic UI hay Pagination giờ đây có thể cấu hình trực tiếp qua cache policy thay vì tự viết logic tay.

## Ví dụ thực tế

Khi ae update thông tin cá nhân, thay vì phải gọi `refetchQueries` để load lại toàn bộ danh sách, ae chỉ cần đảm bảo mutation trả về đúng object `User` kèm ID. Toàn bộ các component đang hiển thị tên user đó sẽ tự động thay đổi mà không tốn thêm một network request nào.

## Tóm lại

Apollo Client + Cache chính là combo giúp FE "nhẹ đầu" khi làm việc với GraphQL. Code gọn hơn, ít bug sync data, và app phản hồi nhanh hơn đáng kể.

Số tới trong series này, mình sẽ đi sâu hơn vào **Apollo Federation** – cách scale hệ thống GraphQL khi backend bắt đầu phình to.

## Giờ đến lượt ae:

- Ae đã từng "vật lộn" hay có kỷ niệm đáng nhớ nào với Apollo Cache chưa?
- Có trick nào để handle cache cho các hệ thống phức tạp không?
- Chia sẻ để mọi người cùng bàn nhé!

**Happy coding!! 😁**
