[#TechSnack 02] | RAG - AI nhớ được context của bạn

Tiếp nối TechSnack về Cursor, hôm nay mình nói về RAG - công nghệ đằng sau việc AI "hiểu" codebase hay documents.

RAG là viết tắt của Retrieval-Augmented Generation. Nghe fancy nhưng ý tưởng đơn giản: thay vì cho AI cả đống text và hy vọng nó nhớ hết, mình cho nó "tìm kiếm" thông tin liên quan trước khi trả lời.

Quy trình hoạt động:
1. Bạn hỏi câu hỏi
2. Hệ thống tìm những phần text liên quan nhất (từ docs, code, database)
3. Gửi câu hỏi + context đó cho AI
4. AI trả lời dựa trên context thực tế

Ví dụ: Cursor sử dụng RAG để khi bạn hỏi về một function, nó sẽ:
- Tìm định nghĩa function đó
- Tìm các nơi nó được gọi
- Tìm tests liên quan
- Rồi mới generate câu trả lời

Điểm hay của RAG là nó giải quyết vấn đề "AI nói bậy" (hallucination). Vì AI được force trả lời dựa trên data thực, không phải bịa ra.

Nếu ae làm chatbot cho company hoặc muốn AI chatbot hiểu documents của mình, RAG là approach phổ biến nhất hiện nay. Có thể implement với LangChain hoặc LlamaIndex khá straightforward.

Ae có đang build gì với RAG không? Share use case của mình nhé!

