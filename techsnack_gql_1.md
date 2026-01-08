# [#TechSnack 06] | GraphQL – Vì sao Frontend engineer thích nó hơn REST API

Ae làm Frontend chắc không lạ gì cảnh: để render một trang Dashboard, mình phải gọi 3-4 cái API khác nhau. Cái thì lấy profile, cái lấy list bài viết, cái lấy notification. Rồi đôi khi API trả về cả đống data thừa (over-fetching) trong khi mình chỉ cần đúng cái ID và Title.

REST API không sai, nhưng nó không được thiết kế để linh hoạt theo sự thay đổi chóng mặt của UI. Đó là lý do GraphQL trở thành một lựa chọn "vàng" khi đóng vai trò là một Backend for Frontend (BFF) thực thụ.

## GraphQL là gì (theo góc nhìn thực tế)?

Thay vì có hàng chục endpoint như `/users`, `/posts`, `/comments`, GraphQL chỉ dùng một single endpoint duy nhất. Điểm khác biệt nằm ở chỗ: Client (Frontend) sẽ gửi một bản "order" (query) mô tả chính xác những field mình cần, và Server sẽ trả về đúng cấu trúc đó. Schema lúc này đóng vai trò như một bản contract rõ ràng, giúp BE và FE làm việc độc lập mà không cần đợi nhau.

## Ví dụ: Lấy data cho trang Profile

**REST** – 3 requests, nhận thừa data:
```
GET /users/123          → trả về 15 fields (chỉ cần 2)
GET /users/123/posts    → trả về 10 bài (chỉ cần 3)
GET /users/123/followers/count
```

**GraphQL** – 1 request, nhận đúng data:
```graphql
query {
  user(id: 123) {
    name
    avatar
    posts(limit: 3) { title }
    followersCount
  }
}
```

- **REST**: 3 requests, ~5KB payload
- **GraphQL**: 1 request, ~0.8KB payload

## Tại sao GraphQL lại "ngon" cho FE?

- **No Over-fetching & Under-fetching**: Ae chỉ lấy đúng data cần thiết, giúp giảm payload size, cực kỳ quan trọng cho mobile apps hoặc người dùng mạng yếu.
- **One request cho cả page**: Bạn có thể fetch toàn bộ nested data (ví dụ: thông tin user kèm danh sách bài viết và các comment mới nhất) chỉ trong một lần gọi duy nhất.
- **Type-safe & Introspection**: Nhờ Schema được định nghĩa chặt chẽ, các tool như Apollo Studio hay GraphiQL cho phép ae explore API, tự động gợi ý code (auto-complete) và bắt lỗi ngay khi viết query.

## GraphQL trong vai trò BFF

Trong các hệ thống lớn, GraphQL thường là một aggregation layer đứng giữa UI và các microservices. Thay vì bắt Mobile hay Web phải tự đi gom data từ nhiều service, GraphQL layer sẽ lo việc kết nối các nguồn dữ liệu lại. Backend không cần đoán FE cần gì, còn FE thì hoàn toàn làm chủ shape of data mà mình nhận được.

Thực tế production, GraphQL không nhất thiết phải thay thế hoàn toàn REST. Chúng thường coexist: REST cho các task đơn giản, và GraphQL cho các màn hình read-heavy, UI-driven phức tạp.

GraphQL giải quyết tốt bài toán fetching, nhưng việc quản lý mớ data đó ở client side lại là một câu chuyện khác. Ở số sau, mình sẽ nói về Apollo Client và cách nó xử lý cache để tối ưu performance.

## Giờ đến lượt ae:

- Ae đã từng gặp rắc rối gì khi dùng REST cho các UI phức tạp chưa?
- GraphQL có phải là lựa chọn ưu tiên của ae khi làm dự án mới không?
- Cùng chia sẻ trải nghiệm của ae bên dưới nhé!

**Happy coding!! 😄**
