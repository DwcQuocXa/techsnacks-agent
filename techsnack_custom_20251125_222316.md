[#TechSnack 06] | Lovable – Unicorn AI app builder cho thời “prompt là code”

Nếu mấy số trước mình nói nhiều về RAG, Langfuse, LLM app,… thì hôm nay chuyển sang một “con hàng” đang khá hot trong giới builder: **Lovable** – AI app builder vừa lên unicorn, build full-stack app từ… prompt.

Trong bối cảnh dev nào cũng bị dí deadline, product team cần prototype liên tục, thì các nền tảng kiểu Lovable đang thay đổi cách chúng ta ship app ra production.

---

## Lovable là gì?

Lovable là một **AI-powered app builder / code editor trên cloud**, cho phép:

- Gõ mô tả bằng natural language → generate **full-stack web app**
- Từ landing page, dashboard, internal tool… đến app có auth, role-based access, payment
- Tích hợp sẵn với GitHub, Supabase, Stripe, custom API

Khác với nhiều no-code tool truyền thống, Lovable vẫn chơi stack quen thuộc của dev: **React + Vite**, có export code, sync GitHub hai chiều, nên không bị khóa chặt trong một “walled garden”.

---

## Workflow cơ bản: từ idea đến app chạy được

Flow làm việc điển hình:

1. **Plan**: mô tả use case, entity, role, workflow ở mức business.
2. **Prompt**: ném toàn bộ mô tả vào Lovable, thêm yêu cầu về UI, stack, integration.
3. **Build**: AI generate skeleton + logic chính, wiring screen, form, API call.
4. **Debug**: dùng AI-assisted bug fixing để sửa lỗi, refine UI, chỉnh flow.
5. **Deploy**: publish trực tiếp lên lovable.app hoặc hook CI/CD qua GitHub.

Theo feedback dev, những thứ trước đây mất vài tuần POC, giờ rút còn vài giờ – nhất là với **internal tool, workflow automation, admin dashboard**.

---

## Workflow automation – mảng Lovable làm khá tốt

Lovable đang được dùng nhiều cho:

- **Task / request management**: form, approval flow, notification logic.
- **Business process automation**: CRM mini, expense tracking, document + e-sign flow.
- **Real-time dashboard**: KPI dashboard, performance review, remote workforce tool.
- **Integration**: nối với third-party service để tạo automation khá phức tạp mà không cần viết nhiều code glue.

AI generate scaffold, còn dev hoặc PM vẫn có thể **edit thủ công** để đảm bảo logic đúng với business rule – cân bằng giữa tốc độ và độ kiểm soát.

---

## Dev nên quan tâm ở điểm nào?

- Prototyping cực nhanh cho product team, PM có thể tự build bản đầu.
- Dev tập trung vào phần “hard” (architecture, data model, integration khó) thay vì UI/CRUD lặp lại.
- Có GitHub sync + export code → không bị lock-in hoàn toàn.
- Nhược điểm: với requirement quá phức tạp, vẫn phải manual fix khá nhiều, không phải “one-click to perfect app”.

---

Giờ đến lượt ae:

- Ae đã thử dùng Lovable (hoặc tool AI app builder tương tự) cho side project hay internal tool chưa?
- Theo ae, ranh giới hợp lý giữa “để AI build” và “tự code” nên nằm ở đâu?

Cmt chia sẻ góc nhìn, mình nghĩ đây sẽ là chủ đề anh em dev bàn khá lâu trong vài năm tới.