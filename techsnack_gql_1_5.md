# [#TechSnack 06.5] | Hiểu GraphQL đúng cách: Query, Mutation và một data graph duy nhất

Ở số TechSnack trước, mình đã nói về GraphQL như một BFF hoàn hảo cho frontend. Tuy nhiên, thực tế nhiều team vẫn đang dùng GraphQL theo kiểu "bình mới rượu cũ" – tức là bê nguyên tư duy RESTful vào syntax mới.

Hôm nay, mình cùng nhìn lại bản chất kiến trúc của GraphQL để hiểu tại sao nó không chỉ là "REST với syntax khác", mà là một cách tiếp cận dữ liệu hoàn toàn khác biệt.

## GraphQL nhìn dữ liệu như một "data graph"

Trong REST, ae thường tư duy theo từng endpoint riêng lẻ. Với GraphQL, hãy tưởng tượng toàn bộ dữ liệu hệ thống là một **nested object** khổng lồ hay một **data graph** duy nhất.

```
User ──→ Posts ──→ Comments ──→ Author
  │                    │
  └──→ Followers       └──→ Likes
```

Khi frontend query, nó giống như đang "đi bộ" trong graph: từ User qua Posts, rồi xuống Comments. Tất cả chỉ nằm trong một request duy nhất:

```graphql
query {
  user(id: 1) {
    name
    posts {
      title
      comments {
        content
        author { name }
      }
    }
  }
}
```

Một request, lấy được cả cây data – không over-fetching, không under-fetching.

## Query vs Mutation – Không chỉ là GET vs POST

Nhiều ae dev mới thường đánh đồng Query là GET và Mutation là POST/PUT. Tuy nhiên, về mặt system, chúng có sự khác biệt rất lớn về cách thực thi.

**Query – Chạy song song (parallel):**

```graphql
query {
  user(id: 1) { name }      # ┐
  posts(limit: 5) { title } # ├─ 3 field này chạy ĐỒNG THỜI
  notifications { count }   # ┘
}
```

Server có thể fetch cả 3 cùng lúc → latency thấp hơn.

**Mutation – Chạy tuần tự (serial):**

```graphql
mutation {
  createPost(title: "Hello") { id }  # Chạy trước
  updateUser(name: "Duc") { name }   # Chạy sau
}
```

Chạy lần lượt để đảm bảo tính nhất quán (ví dụ: post phải tạo xong mới update user).

**Điểm "ăn tiền"**: Mutation luôn trả về data mới:

```graphql
mutation {
  updateUser(id: 1, name: "Duc Nguyen") {
    id
    name        # ← Nhận ngay giá trị mới
    updatedAt   # ← Sync UI lập tức, không cần refetch
  }
}
```

## Apollo – Bộ công cụ để vận hành Data Graph

Để hiện thực hóa và vận hành cái graph này một cách chuyên nghiệp, ae cần một hệ sinh thái như **Apollo**. Apollo không đơn thuần là một thư viện fetch data, nó là một **data layer** thực thụ.

Nó cung cấp tooling cho cả backend (Apollo Server) và frontend (Apollo Client), giúp quản lý schema, tracking performance và đặc biệt là xử lý caching – thứ mà chúng ta sẽ đào sâu ở số tới.

## Giờ đến lượt ae:

- Ae có đang gặp khó khăn khi thiết kế Schema để nó không bị biến thành một mớ hỗn độn (spaghetti schema) không?
- Khi nào ae thấy dùng Mutation vẫn chưa đủ và cần đến Subscription?

Chia sẻ trải nghiệm của ae ở phần comment nhé.

**Happy building!! 😁**
