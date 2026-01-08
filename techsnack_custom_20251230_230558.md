# [#TechSnack 06] | Anthropic Skills – Bước tiến quan trọng để build AI agent chạy production

## Vấn đề với AI Agent hiện tại

Dạo gần đây ae chắc nghe nhiều về AI Agent. Nhưng vấn đề lớn nhất khi build agent thực thụ là: làm sao để nó vừa thông minh, vừa không bị "ngáo" khi context quá dài? Anthropic vừa đưa ra câu trả lời với **Skills** (hay Agent Skills) – một concept giúp chuẩn hóa cách agent học và thực hiện tác vụ.

## Skills là gì?

Nếu coi LLM là bộ não, Tools là đôi tay, thì Skills chính là **quy trình làm việc (SOP)** được đóng gói sẵn. Thay vì nhét hàng tá instruction vào system prompt, Skills cho phép chúng ta modular hóa kiến thức chuyên môn thành các gói tái sử dụng.

## Giải quyết Context Rot

Điểm cốt lõi của Skills là giải quyết bài toán **Context Rot**. Thông thường, nếu ae nhồi quá nhiều hướng dẫn vào một prompt, model sẽ bắt đầu bị loãng thông tin và giảm hiệu suất. Với Skills, Claude chỉ load thông tin cần thiết khi thực hiện tác vụ (selective context loading), giúp giữ context window luôn sạch sẽ.

## Skills vs Tools (MCP)

Ae cần phân biệt rõ giữa **Skills** và **Tools (MCP)**. Tools là *khả năng* tương tác (như fetch API, query SQL), còn Skills là *bí quyết* để dùng tools đó đúng cách (như quy trình phân tích dữ liệu tài chính). Một agent mạnh nhất là sự kết hợp của cả hai: có công cụ và biết cách dùng công cụ theo đúng quy trình.

## Cấu trúc của một Skill

Cấu trúc của một Skill thường gồm ba phần: instruction (workflow chi tiết), reference documents (guideline, policy) và executable scripts. Việc tích hợp script giúp agent đạt được kết quả mang tính **deterministic** (nhất quán), thay vì chỉ dựa hoàn toàn vào sự suy luận ngẫu nhiên của LLM.

## Giá trị cho Engineer

Đối với engineer, Skills mang lại giá trị lớn trong việc scale hệ thống. Bạn có thể build một bộ Skill chuẩn cho công ty và deploy chúng đồng nhất trên Claude.ai, Claude Code hay qua API. Hiện tại, Anthropic đã mở Skills thành một open standard, cho thấy tham vọng biến đây thành quy chuẩn chung cho toàn bộ hệ sinh thái AI agent.

Giờ đến lượt ae:
- Ae đã thử chia nhỏ logic agent thành các module chuyên biệt chưa?
- Theo ae, việc dùng Skills có giúp debug agent dễ dàng hơn so với prompt truyền thống?
- Chia sẻ trải nghiệm của ae về việc quản lý context window cho agent nhé.

**Happy building!**
