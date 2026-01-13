# [#TechSnack 07] | Apollo Client – Tại sao FE thích dùng nó hơn là tự fetch bằng tay

Ae làm Frontend chắc không lạ gì cảnh: fetch data xong, cất vào Redux hay Zustand cho "chắc cú", rồi lại loay hoay sync data khi có update. Re-fetch liên tục thì UI lag, mà không re-fetch thì data lại cũ mèm.

Đây là bài tiếp nối trong series **GraphQL cho Frontend**. Hôm nay mình sẽ nói về **Apollo Client** – tại sao nó "ngon" hơn việc tự gọi API bằng tay, và ở nửa sau bài viết mình sẽ đi sâu vào **Apollo Cache** – thứ làm nên sự khác biệt thực sự.

---

## Apollo Client là gì?

Nếu ae đã làm việc với REST thì chắc quen với combo `fetch/axios` + `Redux/Zustand` + `React Query`. Apollo Client về bản chất là **tất cả những thứ đó gộp lại**, nhưng được thiết kế riêng cho GraphQL.

Nó không chỉ là một HTTP client để gọi API. Apollo Client lo luôn:
- **Data fetching**: gọi query, mutation
- **Caching**: tự động lưu và cập nhật data
- **State management**: không cần Redux cho server state nữa
- **UI updates**: component tự re-render khi data thay đổi

Nói cách khác, ae có thể coi Apollo Client như **"Redux + React Query" nhưng tối ưu riêng cho GraphQL**. Thay vì tự viết reducer, action, selector loằng ngoằng, Apollo lo hết – ae chỉ cần viết query và dùng.

---

## Core Hooks – Viết ít, làm được nhiều

Apollo Client cung cấp 3 hooks chính mà ae sẽ dùng hầu như mọi lúc:

**1. `useQuery`** – Lấy data

```javascript
const { data, loading, error } = useQuery(GET_USER, {
  variables: { id: "123" }
});
```

Không cần `useEffect`, không cần `useState` cho loading/error. Apollo tự handle hết và component tự re-render khi data về.

**2. `useMutation`** – Thay đổi data

```javascript
const [updateUser, { loading }] = useMutation(UPDATE_USER);

// Gọi khi cần
await updateUser({ variables: { id: "123", name: "New Name" } });
```

Mutation xong, nếu server trả về đúng object với ID, Apollo tự update cache – UI thay đổi mà không cần ae làm gì thêm.

**3. `useLazyQuery`** – Query theo yêu cầu

```javascript
const [searchUsers, { data }] = useLazyQuery(SEARCH_USERS);

// Gọi khi user nhấn nút search
searchUsers({ variables: { keyword: "john" } });
```

Khác với `useQuery` chạy ngay khi component mount, `useLazyQuery` chỉ chạy khi ae gọi – perfect cho search, filter, hay các action do user trigger.

---

## So sánh: Apollo Client vs Tự fetch bằng tay

**Tự fetch + Redux:**
- Boilerplate nhiều: action, reducer, selector loằng ngoằng
- Loading/Error state phải tự handle
- Caching phải tự implement
- Sync data giữa components phức tạp
- Optimistic UI phải tự viết logic
- TypeScript types phải tự define

**Apollo Client:**
- Gần như không có boilerplate
- Loading/Error state có sẵn trong hook
- Caching tự động với Normalized Cache
- Data sync giữa components tự động
- Optimistic UI built-in support
- Types auto-generate từ GraphQL schema

Điểm khác biệt lớn nhất: với Apollo, ae **không cần nghĩ về việc sync data**. Khi mutation thành công, tất cả component đang dùng data đó sẽ tự update.

---

## Apollo Cache – "Sauce" bí mật của Apollo

Đây mới là thứ làm Apollo "đỉnh" hơn hẳn việc tự quản lý state. Cache của nó hoạt động như một **"local graph database"** ngay trong browser.

### Normalized Cache hoạt động như thế nào?

Thay vì lưu JSON thô như response trả về, Apollo băm nhỏ data thành các object phẳng (flat lookup table) dựa trên `__typename` và `id`:

```javascript
// Response từ server
{
  user: {
    id: "1",
    name: "John",
    posts: [
      { id: "101", title: "Hello World" },
      { id: "102", title: "GraphQL rocks" }
    ]
  }
}

// Apollo lưu trong cache
{
  "User:1": { id: "1", name: "John", posts: ["Post:101", "Post:102"] },
  "Post:101": { id: "101", title: "Hello World" },
  "Post:102": { id: "102", title: "GraphQL rocks" }
}
```

Nhờ cơ chế này, cùng một entity (ví dụ `User:1`) dù xuất hiện ở Dashboard hay Profile page thì **chỉ có một bản duy nhất trong cache**. Khi ae mutation và server trả về ID đó, Apollo tự động merge field mới và broadcast update cho toàn bộ UI đang lắng nghe.

### Fetch Policy – Kiểm soát caching behavior

Apollo cho ae toàn quyền quyết định khi nào dùng cache, khi nào gọi network:

- **`cache-first`** (default): Có trong cache thì dùng ngay, không thì mới gọi network
- **`cache-and-network`**: Hiện data cũ ngay lập tức, đồng thời gọi network và update khi có data mới
- **`network-only`**: Luôn gọi network, nhưng vẫn lưu vào cache
- **`cache-only`**: Chỉ đọc từ cache, không gọi network

```javascript
const { data } = useQuery(GET_USER, {
  fetchPolicy: "cache-and-network"
});
```

Với `cache-and-network`, user thấy data cũ ngay lập tức và app tự cập nhật bản mới nhất ngầm bên dưới – **UX cực kỳ mượt mà**.

---

## Ví dụ thực tế

Khi ae update thông tin cá nhân:

```javascript
const [updateUser] = useMutation(UPDATE_USER);

await updateUser({
  variables: { id: "123", name: "New Name" },
  // Không cần refetchQueries nếu mutation trả về đủ fields
});
```

Thay vì phải gọi `refetchQueries` để load lại toàn bộ danh sách, ae chỉ cần đảm bảo mutation trả về đúng object `User` kèm ID. Toàn bộ các component đang hiển thị tên user đó sẽ **tự động thay đổi mà không tốn thêm một network request nào**.

---

## Tóm lại

Apollo Client giúp FE "nhẹ đầu" khi làm việc với GraphQL:
- **Hooks đơn giản**: `useQuery`, `useMutation`, `useLazyQuery` – viết ít, làm được nhiều
- **Normalized Cache**: data được chuẩn hóa, tự động sync giữa các component
- **Fetch Policy**: kiểm soát caching behavior linh hoạt, tối ưu UX

Code gọn hơn, ít bug sync data, và app phản hồi nhanh hơn đáng kể. Những tính năng "khó nhằn" như Optimistic UI hay Pagination giờ đây có thể cấu hình trực tiếp thay vì tự viết logic tay.

Số tới trong series này, mình sẽ đi sâu hơn vào **Apollo Federation** – cách scale hệ thống GraphQL khi backend bắt đầu phình to.

---

## Giờ đến lượt ae:

- Ae đang dùng gì để quản lý server state? Redux, React Query, hay đã chuyển sang Apollo?
- Có ai từng "vật lộn" với việc sync data giữa các component trước khi dùng Apollo không?
- Chia sẻ trải nghiệm của ae bên dưới nhé!

**Happy coding!! 😁**
