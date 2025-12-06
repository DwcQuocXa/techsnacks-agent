# [#TechSnack 05] | Langfuse – observability cho LLM app chạy production

Lần số techsnack 03, mình có viết về Langchain như 1 framework để build LLM app. Nhưng lúc lên production thì câu hỏi quen thuộc lại quay về: **"User kêu AI trả lời ngu, mình debug kiểu gì?"**

Hôm nay thử bàn nhanh về **Langfuse** - một open source platform khá mạnh cho LLM observability + evaluation + prompt management.

## Langfuse giải quyết bài toán gì?

Về bản chất, Langfuse giúp ae "nhìn xuyên" toàn bộ lifecycle của một LLM call: input, output, tool call, retry, latency, cost,… đều được trace lại.

Thay vì chỉ log vài dòng text, bạn có một trace tree của cả flow: user query → RAG retrieval → LLM → tools → final answer.

Từ đó debug dễ hơn, optimize prompt dễ hơn, và biết chính xác tiền đang "chảy" vào model nào.

## Langfuse có gì đáng chú ý?

- Open source (MIT), self-host bằng Docker rất thẳng, dùng chung codebase với Langfuse Cloud.
- Backend mới (v3) dùng ClickHouse nên scale tốt cho lượng trace lớn.
- Có SDK cho Python, TypeScript/JavaScript, integrate ngon với LangChain, OpenAI API, v.v.
- Hỗ trợ evaluation (LLM-as-a-judge, metric custom), prompt versioning, dataset cho A/B test.

Nói ngắn gọn: không phải chỉ log viewer, mà là một LLM engineering platform để cả team cùng làm việc trên cùng data.

## Một ví dụ dùng Langfuse rất thực tế

Giả sử ae build một RAG chatbot cho nội bộ công ty:

Backend Node.js/Express gọi OpenAI API + vector DB.

Bạn cài SDK Langfuse, wrap mỗi request thành một trace:

- observation cho bước semantic search
- observation cho mỗi LLM call
- log thêm metadata: user_id, tenant, document_id,…

Khi user kêu: **"Chatbot trả lời sai về policy nghỉ phép."**

Bạn vào Langfuse:

- filter theo user_id / thời gian
- mở trace, xem rõ context nào được retrieve, prompt version nào được dùng, model trả ra text gì

Thấy vấn đề là chunk policy bị thiếu → bạn:

- fix pipeline chunking hoặc index lại
- chỉnh prompt trong Langfuse UI (tạo prompt version mới)
- deploy prompt mới không cần redeploy backend.

Song song, bạn setup evaluation rule: mọi câu trả lời về "policy" sẽ được LLM chấm score "correctness". Dashboard cho thấy sau khi đổi prompt, score trung bình tăng, cost/req giữ nguyên.

## Vì sao dev nên quan tâm?

- ✅ Debug LLM app nhanh hơn rất nhiều so với grep log thô.
- ✅ Có cơ sở dữ liệu thực tế để optimize: latency, cost, quality.
- ✅ Phù hợp cho cả side project (self-host free) lẫn production lớn (enterprise feature).

## Giờ đến lượt ae:

- Ae đang trace LLM app bằng gì?
- Có tình huống production nào khiến ae thấy cần một tool kiểu Langfuse không?
- Cmt chia sẻ để mọi người cùng bàn cách quan sát và tối ưu LLM app nhé.

**Happy coding!! 😁**


