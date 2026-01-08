# [#TechSnack 06] | Google – Kẻ thắng sau cùng trong cuộc đua AI?

Gần đây ae dev hay bàn về Nvidia stock hay OpenAI ra model mới. Nhưng nếu nhìn kỹ vào **tầng hạ tầng (infrastructure)** và **kiến trúc model**, có vẻ **Google** đang nắm trong tay những quân bài mạnh nhất để thắng đường dài.

Lý do nằm ở chiến lược **Vertical Integration** – tích hợp dọc từ **chip → cloud → model → data → end-user** mà gần như **không ai khác có được**, kể cả Nvidia hay OpenAI.

---

## 1. Hardware: TPU vs GPU

Trong khi cả thế giới tranh nhau mua GPU H100 của Nvidia với giá cắt cổ, Google đã âm thầm tối ưu dòng **TPU (Tensor Processing Unit)** suốt hơn 10 năm nay.
Điểm khác biệt nằm ở chỗ: GPU của Nvidia là **general-purpose** (đa dụng), còn TPU là **ASIC (Application-Specific Integrated Circuit)** – chip được thiết kế riêng cho tác vụ AI.

* **Hiệu năng/Chi phí:** TPU v7 (Ironwood) cho **hiệu suất trên mỗi đô cao gấp 4 lần** H100 trong workload transformer.
* **Tiết kiệm năng lượng:** mỗi cluster TPU tiêu thụ **ít hơn 60–65% điện năng** so với setup GPU tương đương.
* **Kết nối nội bộ:** TPU v7 có thể nối **tới 9.216 chip qua interconnect 9.6 Tbps**, trong khi Nvidia NVL72 chỉ nối được 72 GPU – khác biệt gần **hai bậc độ lớn** về scale.

Ngoài ra, TPU cluster của Google dùng **optical switch fabric**, giúp giảm latency giao tiếp giữa chip khi training model lớn (kiểu Gemini 3).
Khi inference trở thành phần tốn kém nhất trong vòng đời AI (chiếm tới **75% tổng compute cost**), hiệu năng/chi phí này là thứ quyết định ai sống sót lâu nhất.

Thế nên không lạ khi **Meta, Anthropic, thậm chí OpenAI** đang xem xét thuê hoặc mua TPU capacity của Google. Nvidia đang bị chính khách hàng lớn nhất của mình tìm cách “thoát thuế phần cứng”.

---

## 2. Model & Software: Gemini vs OpenAI

Trên mặt trận model, **Gemini 3** vừa có màn bứt tốc mạnh mẽ – vượt GPT-5.1 trong nhiều benchmark:

* GPQA (Science): 91.9% vs 88.1%
* MMMU-Pro (Multimodal): 81.0% vs 76.0%
* ARC-AGI-2 (Reasoning): 31.1% vs 17.6%
* LiveCodeBench (Coding): 2,439 Elo vs 2,243

Quan trọng hơn: **Gemini được train hoàn toàn trên TPU**, chứng minh TPU đủ sức chạy frontier model mà không cần GPU của Nvidia.

Điểm chí mạng là **OpenAI không có hạ tầng riêng** – toàn bộ compute phụ thuộc vào Azure và GPU Nvidia. Khi margin của Nvidia vẫn ở mức **73–75%**, OpenAI bị “ăn” chi phí nặng nề.
Nếu Microsoft siết cost hoặc Nvidia tăng giá, họ sẽ kẹt.

Ngược lại, Google làm chủ từ đầu đến cuối:
**Chip (TPU) → Cloud → Model (Gemini) → Data (Search/YouTube) → Device (Android).**

Điều này cho phép họ tối ưu theo chiều dọc.
Ví dụ: Google có thể **quantize model xuống 8-bit hoặc 4-bit** để khớp chính xác với kiến trúc TPU v7, giảm latency inference tới mức mà model cùng size chạy trên GPU khó mà đuổi kịp.

---

## 3. Nvidia: Đế chế bắt đầu lung lay

Nvidia vẫn thống trị với **90%+ thị phần AI accelerator**, nhưng bài toán đang đổi chiều.
Với biên lợi nhuận 75%, các hyperscaler như Google, AWS, Microsoft, Meta **đều có động lực mạnh để tự làm chip riêng** (TPU, Trainium, Maia, MTIA…).

Khi thị trường chuyển từ *training* sang *inference* – vốn **tốn gấp 15 lần compute** và chiếm phần lớn chi phí vận hành – Nvidia đang ở thế bất lợi: GPU vốn được thiết kế cho giai đoạn training.

Vấn đề còn nằm ở chu kỳ thay thế chip: mỗi khi Nvidia ra thế hệ mới (Blackwell, Rubin…), thế hệ trước gần như “mất giá ngay lập tức”.
Nhiều datacenter đang đối mặt bài toán **khấu hao hàng tỷ USD** vì chip cũ nhanh chóng lỗi thời về hiệu năng/watt.

---

## Tóm lại

Cuộc đua AI giờ không còn là *ai có model thông minh hơn*, mà là **ai chạy được model đó với chi phí thấp nhất và ổn định nhất ở quy mô toàn cầu.**

* **OpenAI**: model mạnh, nhưng hạ tầng phụ thuộc và burn rate cao.
* **Nvidia**: lợi nhuận siêu cao, nhưng bị chính khách hàng tìm cách “cắt cổ chai”.
* **Google**: sở hữu cả silicon, cloud, model và user base — một chuỗi tích hợp dọc hoàn chỉnh.

Khi inference thống trị và GPU bắt đầu mất vị thế, rất có thể Google sẽ là **kẻ thắng sau cùng trong cuộc đua AI**.

---

**Giờ đến lượt ae:**

* Ae dev dạo này code, test hay gọi API của Gemini nhiều hơn GPT/Claude không?
* Ae có thấy tốc độ inference của Gemini gần đây mượt hơn rõ rệt không?
* Cmt chia sẻ trải nghiệm thực tế để cộng đồng Viet Tech cùng bàn nhé.

**Happy coding!**
