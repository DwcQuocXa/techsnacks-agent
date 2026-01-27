# [#TechSnack 06] | Apollo Server & Federation: Khi GraphQL cần "chia để trị"

Chào ae, sau vài số TechSnack bàn về AI và Observability, tuần này chúng ta quay lại với một chủ đề cực kỳ thực chiến trong kiến trúc hệ thống: **GraphQL at scale**. 

Đa số ae khi mới tiếp cận GraphQL đều thấy rất "sướng": một endpoint duy nhất, một schema, FE muốn lấy gì thì query nấy. Nhưng khi hệ thống phình to, nhiều team cùng nhảy vào một codebase, cái schema đó nhanh chóng trở thành một "bãi rác" khổng lồ. Việc merge code trở thành nỗi ác mộng, và một lỗi nhỏ ở resolver của team A có thể kéo sập toàn bộ gateway. Đó là lúc chúng ta cần nói về **Apollo Federation**.

---

## Apollo Server – Không chỉ là cái cổng parse query

Trước khi nói về Federation, hãy định vị lại **Apollo Server**. Nhiều người nhầm tưởng nó chỉ là một thư viện để parse query string thành dữ liệu. Thực tế, Apollo Server đóng vai trò là một **GraphQL runtime** thực thụ.

Nó quản lý toàn bộ lifecycle của một request: từ việc validate schema, định tuyến resolver, xử lý context (auth, logging), cho đến performance hooks (caching, batching). Apollo Server cực kỳ linh hoạt vì nó có thể đứng trước bất kỳ nguồn data nào: REST API cũ, gRPC, Database, hay thậm chí là một serverless function. 

Tuy nhiên, nếu ae chỉ dùng một Apollo Server duy nhất cho toàn bộ hệ thống (Monolithic GraphQL), ae sẽ sớm đụng trần về khả năng scale nhân sự và quản lý ownership.

---

## GraphQL backend không phải REST backend

Trong thế giới REST, việc chia microservices rất tự nhiên: mỗi team quản một cụm endpoint riêng. Nhưng với GraphQL, chúng ta hứa với FE về một **Unified Graph** (một sơ đồ dữ liệu hợp nhất). 

Nếu ae cố ép hàng chục microservices vào một file schema duy nhất, ae sẽ gặp các vấn đề:
- **Schema Conflict**: Team A và Team B cùng muốn đặt tên type là `Product` nhưng cấu trúc khác nhau
- **Deployment Bottleneck**: Một thay đổi nhỏ cũng bắt buộc phải deploy lại toàn bộ monolith backend
- **Ownership mập mờ**: Ai là người chịu trách nhiệm khi query `user { orders }` bị chậm?

Vấn đề không nằm ở GraphQL, mà nằm ở cách chúng ta tổ chức ownership của schema. Đây là lúc Apollo Federation giải quyết bài toán này bằng cách chia nhỏ schema thành các **Subgraphs**.

---

## Apollo Federation: Kiến trúc Microservices cho GraphQL

Apollo Federation cho phép ae chia nhỏ một schema lớn thành nhiều schema nhỏ (subgraph), mỗi subgraph được sở hữu và vận hành bởi một team độc lập. Một thành phần gọi là **Gateway** (hoặc Apollo Router) sẽ đứng ở giữa để tổng hợp (compose) các subgraph này thành một **Supergraph** duy nhất cho FE.

Điểm hay nhất của Federation là khả năng **Entity Resolution**. Ví dụ: Team User quản lý type `User`, nhưng Team Order muốn mở rộng type `User` để thêm field `recentOrders`. 

```graphql
# Subgraph: Accounts
type User @key(fields: "id") {
  id: ID!
  username: String!
}

# Subgraph: Orders
extend type User @key(fields: "id") {
  id: ID! @external
  recentOrders: [Order]
}
```

Với directive `@key`, Apollo Router sẽ biết cách "nhảy" từ service Accounts sang service Orders để lấy dữ liệu cho cùng một object `User`. FE vẫn chỉ thấy một schema đồng nhất, không hề biết backend đang chia tách thế nào. 

---

## Federation Directives cần nắm

Ngoài `@key`, Federation còn có một số directives quan trọng:
- **`@external`**: Đánh dấu field được định nghĩa ở subgraph khác
- **`@requires`**: Field này cần data từ field khác để resolve (ví dụ: tính `totalPrice` cần `quantity` và `unitPrice`)
- **`@provides`**: Subgraph này có thể cung cấp thêm field cho entity của subgraph khác
- **`@shareable`** (Federation v2): Cho phép nhiều subgraphs cùng resolve một field

Hiểu rõ các directives này sẽ giúp ae thiết kế schema boundaries hợp lý và tránh những lỗi runtime khó debug.

---

## Khi nào nên dùng Federation?

Nếu ae đang làm việc trong một tổ chức có từ 3 team backend trở lên, Federation mang lại những lợi ích rõ ràng:
- **Ownership rõ ràng**: Team Product sở hữu Product subgraph, team Review sở hữu Review subgraph. Không ai đụng vào code của ai
- **Deploy độc lập**: Team Review có thể update logic tính sao mà không cần quan tâm team Product đang làm gì, miễn là không phá vỡ schema contract
- **Hiệu năng tối ưu**: Với **Apollo Router** (viết bằng Rust), query planning và fetch song song từ các subgraph có latency cực thấp

Tuy nhiên, đừng "over-engineering". Nếu backend của ae chỉ có một vài service đơn giản, việc duy trì Federation Gateway và schema registry có thể mang lại nhiều overhead hơn là lợi ích.

---

## Tóm lại

- **Apollo Server** là runtime mạnh mẽ để build GraphQL backend, không chỉ là query parser
- **Monolithic GraphQL** sẽ gây nghẽn cổ chai khi team size và hệ thống lớn dần
- **Apollo Federation** giúp chia nhỏ schema thành các **Subgraphs** theo domain
- **Entity Resolution** với `@key` là core concept – cho phép một entity được extend bởi nhiều services
- **Apollo Router/Gateway** đóng vai trò orchestrator, giúp FE vẫn có trải nghiệm unified API

---

## Giờ đến lượt ae:

- Hệ thống GraphQL của ae hiện tại là Monolith hay đã phân rã?
- Ae có gặp khó khăn gì khi làm việc với Federation (như n+1 cross-service hay tracing) không?
- Chia sẻ kinh nghiệm "đau thương" hoặc thành công của ae bên dưới nhé!

**Happy coding!! 😁**
