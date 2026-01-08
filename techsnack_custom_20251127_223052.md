# [#TechSnack 06] | AI Engineering: Sách gối đầu cho Foundation Model

Sau nhiều tuần nói về các công cụ và patterns mới như RAG, Langfuse, hay Agentic workflow, mình nhận ra tất cả những kiến thức này đều được hệ thống hóa trong một cuốn sách rất đáng chú ý. Đó là **"AI Engineering: Building Applications with Foundation Models"** của Chip Huyen.

Đây là cuốn sách đang là best-seller trên O’Reilly, và được cộng đồng engineer đánh giá là tài liệu uy tín nhất về "New AI Stack" hiện nay.

## AI Engineering là gì?

Khác biệt lớn nhất là cuốn sách này không tập trung vào việc train model từ đầu (như các sách ML Engineering truyền thống). Nó tập trung vào **AI Engineering** — tức là làm thế nào để xây dựng các *application* đáng tin cậy, chi phí hợp lý, và có thể scale, dựa trên các Foundation Model (LLM) có sẵn.

Nói cách khác, nó coi model là một *commodity* (hàng hóa có sẵn) và tập trung vào tầng **application layer** để tạo ra sự khác biệt trong sản phẩm. Đây là cuốn sách gối đầu cho ai đang làm việc với LLM chạy production.

## Các chủ đề kỹ thuật cốt lõi

Cuốn sách đi sâu vào các chủ đề mà ae engineer đang vật lộn hàng ngày khi đưa AI vào sản phẩm:

1.  **RAG & Context Engineering:** Không chỉ là RAG cơ bản mà còn là cách tối ưu hóa retrieval, data preparation (chunking, deduplication), và đảm bảo nguồn context luôn sạch.
2.  **Evaluation & Observability:** Đây là phần quan trọng bậc nhất. Nó bàn về việc làm sao để đánh giá chất lượng output của LLM (dùng **LLM-as-a-judge**) và cách trace toàn bộ flow (giống như Langfuse mà mình từng nói) để dễ dàng **debugging**.
3.  **Agents & Orchestration:** Các pattern để xây dựng Agentic workflow phức tạp (kiểu như LangGraph), cách planning và tool use hiệu quả.
4.  **Inference Optimization:** Làm sao để giảm **latency** và **cost** khi serving Foundation Models, bao gồm cả các chiến lược cho deployment.

## Cuốn sách này dành cho ai?

Rất rõ ràng: cuốn sách này dành cho các **engineer** đang chuyển từ traditional ML sang LLM, hoặc các **developer** muốn build LLM app lên production.

Nó cung cấp một framework có cấu trúc để giải quyết các vấn đề thực tế: từ prompt engineering, versioning, cho đến deployment và **scalability**. Nếu bạn đang phải đối mặt với LiteLLM timeouts, cần framework evaluation, hay đang thiết kế multi-agent systems, đây chính là tài liệu bạn cần.

## Giờ đến lượt ae:

- Ae đã đọc cuốn này chưa? Cảm nhận của ae về cách tác giả Chip Huyen hệ thống hóa kiến thức thế nào?
- Hoặc ae có cuốn sách/tài liệu nào khác về LLM Engineering mà ae thấy đáng đọc không?

Chia sẻ cho cộng đồng Viet Tech Finland cùng biết nhé!

**Happy building 😁**