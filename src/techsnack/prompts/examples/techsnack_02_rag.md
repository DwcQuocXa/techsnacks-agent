# [#TechSnack 02] | RAG – Khi AI biết tra Google trước khi trả lời

Tuần trước mình nói về Cursor 2.0 – một tool quá quen với ae dev.

Hôm nay thử nói về một khái niệm mà anh em chắc nghe nhiều: **RAG (Retrieval-Augmented Generation)**.

Nếu nói đơn giản, thì RAG giúp AI… **biết tra Google trước khi trả lời**.

Tức là thay vì chỉ dựa vào dữ liệu nó được train (và có khi đã cũ mèm), RAG cho phép AI tự đi tìm tài liệu, đọc, rồi mới nói.

Vì thế, câu trả lời sẽ chính xác, cập nhật và có cơ sở hơn nhiều.

## Cách RAG hoạt động

1. Khi bạn gửi câu hỏi, hệ thống sẽ biến câu hỏi thành **vector** – tức là dạng số để máy hiểu.
2. Nó so khớp vector đó với kho dữ liệu (document, wiki, nội bộ công ty, v.v.) để tìm thông tin liên quan.
3. Sau đó, nó ghép mớ thông tin tìm được vào prompt gốc.
4. Cuối cùng, LLM (kiểu GPT, Claude, v.v.) sẽ generate câu trả lời dựa trên cả hai nguồn: kiến thức sẵn có + thông tin mới tìm.

**Kết quả là AI vừa "biết" như trước, vừa "tra cứu" được như người thật.**

## Tại sao nó quan trọng với ae dev chưa làm AI?

Vì RAG đang là xương sống của các ứng dụng AI thật sự chạy production.

- ✅ Không cần train model mới mỗi lần data đổi
- ✅ Giảm hẳn "ảo tưởng sức mạnh" (hallucination) của AI
- ✅ Dễ debug vì biết nó lấy thông tin từ đâu
- ✅ Áp dụng được ngay cho nội bộ: document search, chatbot công ty, Q&A hệ thống, report automation,…

Các big tech như AWS, Google, NVIDIA, Microsoft đều đã build tool quanh RAG để làm chatbot, search nội bộ, hay fraud detection.

## Một ví dụ dễ hiểu

Giả sử bạn làm ở công ty có cả nghìn file PDF specs.

Trước đây tìm thông tin mất cả buổi, giờ bạn chỉ hỏi:

> "Spec của module X trong version mới là gì?"

RAG sẽ tự tìm trong kho tài liệu, lấy đúng đoạn liên quan rồi synthesize ra câu trả lời ngắn gọn.

Không cần ai gõ lệnh grep hay search thủ công nữa.

## Tóm lại:

Nếu LLM là **"não"**, thì RAG chính là **"bộ nhớ ngoài + Google Search"** của AI.

Đây là cách mà thế hệ công cụ như ChatGPT Enterprise, Claude for Teams, hay nhiều assistant nội bộ vận hành thực tế.

## Giờ đến lượt ae:

- Ae đã từng thử build RAG app chưa?
- Nếu chưa, feature nào trong ý tưởng này khiến ae thấy muốn thử nhất?
- Cmt chia sẻ để ae cùng bàn nhé. Hi vọng sẽ được lắng nghe nhiều ý tưởng hay và những chia sẻ của anh em về cách ứng dụng hệ thống RAG, cũng như làm thế nào để tối ưu một hệ thống RAG cho hiệu quả nhất.

**Happy building 😁**
