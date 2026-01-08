# [#TechSnack 11] | Vibe Coding Tools – Bong bóng Prototyping đang xì hơi?

Thời gian trước, ai trong giới tech cũng nói về "Vibe Coding" – khả năng dùng AI tạo ra app từ một *prompt* trong vài phút.  Hứa hẹn về *productivity* và tốc độ *development* là rất lớn. TechSnack số 6 mình cx giới thiệu về Lovable - một tool Vibe Code phổ biến. Nhưng dữ liệu mới nhất từ Barclays cho thấy một thực tế phũ phàng: traffic của các tools hàng đầu đang lao dốc không phanh. Vercel v0 giảm **64%** kể từ tháng 5, Lovable giảm **40%**, và Bolt.new giảm **27%**. Toàn các kì lân gọi hàng chục, trăm triệu đô nhưng dự là sắp cút :D 

## "Great demo, now throw it in the trash"

Ben Collins (CEO Woz) chia sẻ một tình huống mà nhiều *engineer* sẽ thấy quen thuộc: Product Manager dùng AI tạo ra một cái *prototype* rất xịn và mang đi khoe. Engineering team nhìn vào và bảo: **"Great, we understand what you want,"** và sau đó **"throws the whole thing in the trash"** để *rewrite* từ đầu.

Tại sao? Vì cái mà AI sinh ra thường là cái họ gọi là **"spaghetti code — everything is tangled together, you can’t tell what’s doing what and it’s full of shortcuts that will come back to bite you later."** Nó được tối ưu cho việc "chạy được ngay" để làm demo, chứ không phải để *maintain* hay *scale* trong môi trường *production*.

## Security Holes: Khi AI "đi tắt"

Vấn đề nghiêm trọng hơn nằm ở *security*. Brad Eckert (CTO Woz) chỉ ra rằng các hệ thống tự động thường chọn con đường dễ nhất: **"It’s easier for an automated system to just dump user photos into a public storage bucket where anyone with the URL can access them."**

Eckert chia sẻ thêm về hậu quả: **"We’ve seen that happen multiple times. Someone uploads their driver’s license photo, and suddenly it’s just sitting there on the internet."** Những lỗi ngớ ngẩn này là điều không thể chấp nhận được với các hệ thống *enterprise*.

## Reality Check

Cộng đồng đang dần nhận ra rằng *prototyping* chỉ là phần dễ. Phần khó là biến nó thành một sản phẩm *secure*, *scalable* và *maintainable*. Như Collins trích dẫn một câu nói nổi tiếng tại MIT: **"Solve hard problems. Don’t pretend they’re easier than they are."**

AI vẫn là một công cụ hỗ trợ tuyệt vời để *visualize* ý tưởng, nhưng việc ảo tưởng rằng nó có thể thay thế hoàn toàn *engineering expertise* đang khiến nhiều dự án đi vào ngõ cụt.

## Góc nhìn cá nhân

Hồi trước mình có nghe một người anh chia sẻ rằng không nên "vibe code" mà hãy *pair programming* cùng với AI. Mình hoàn toàn đồng ý và đang áp dụng triệt để.

*Workflow* giờ không còn là viết code nữa mà đổi thành *planning* + *review* + nghĩ nhiều hơn về việc làm sao để *guide* AI đi đúng ý mình một cách nhanh và tiện nhất.

## Giờ đến lượt ae:
- Ae đã bao giờ phải "đập đi xây lại" code do AI viết chưa?
- Ae nghĩ sao về tương lai của *vibe coding*? Liệu nó sẽ chết yểu hay tiến hóa thành dạng khác?

**Happy building!** 😄
