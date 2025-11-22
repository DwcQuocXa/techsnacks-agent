# [#TechSnack 01] | Cursor 2.0

Nhận thấy rằng tech community của anh em mình khá đông nhưng hơi im ắng. Thế nên bọn mình quyết định khởi động một series nho nhỏ tên là **#TechSnack**, nơi chia sẻ nhanh về tin công nghệ, startup thú vị, hay mẩu kiến thức ngắn gọn mà anh em dev nào cũng có thể đọc nhanh trong vài phút. Hy vọng series này sẽ giúp thổi hồn lại cho cộng đồng Viet Tech Finland và làm không khí sôi nổi hơn.

## Chủ đề hôm nay: Cursor 2.0

Mình đoán là đa phần ae dev đều đã nghe (hoặc đang dùng) Cursor rồi đko? Với mình thì Cursor gần như cánh tay phải trong việc code. Mình hay dùng nó để giải thích code, lập plan, và brainstorming nhanh với AI.... Giờ thì Cursor vừa ra bản 2.0, với kha khá thứ đáng chú ý:

### **Composer 1 Alpha Model**

Model AI đầu tiên của Cursor, được train trên hàng tỷ lượt dùng real từ dev như ae. Tốc độ là selling point của con AI này (nhanh hơn Claude 3.5 Sonnet tới 4 lần) - hợp cho các task code ngắn, chạy command hay commit nhanh.

→ *Cá nhân mình thấy tốc độ rất quan trọng với mấy việc đơn giản, chứ GPT-5 hay Claude Code đôi khi chậm quá 😄 thà mình làm luôn cho nhanh*

### **Multi-Agent Interface**

Cho phép chạy song song tới 8 agent AI trên cùng codebase, mỗi agent ở một worktree, không ảnh hưởng nhau. Tại sao làm đc thế thì có vẻ họ tạo ra worktree từ ý tưởng từ git branch.

→ *Mình thì không dùng feature này nhiều khi code, nhưng lại dùng khá nhiều khi planning, vì muốn so sánh xem Sonnet 4.5 hay GPT-5 thằng nào plan tốt hơn*

### **Integrated Browser Preview**

Cursor có tích hợp Chrome, cho phép test end-to-end, xem log, inspect DOM,....

→ *Cái này chắc anh em làm FE sẽ cần. Mình bỏ FE tầm nửa năm nay nên chưa có dịp thử.*

---

Ngoài ra còn vài tính năng khác mình chưa trải nghiệm, nên tạm để dành cho các post sau.

## Giờ đến lượt ae:

- Ae dùng Cursor thế nào để tối ưu workflow hoặc tăng productivity?
- Có trick hay setup nào đáng thử không?
- Chia sẻ cho mọi người cùng biết nhé

**Happy coding 😄**
