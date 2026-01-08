# [#TechSnack 16] | FPT × NVIDIA – Một deal hạ tầng AI, không chỉ là mua GPU

Hôm qua mình có hỏi chính AI market intelligence product mà mình và team đang build ở AlphaSense  về Vietnam Stock Market Outlook 2026. Report 20 trang, nhưng có một câu khiến mình dừng lại: "The technology sector, led by FPT, is transitioning from a low-cost outsourcing model to a high-value AI and global IT services provider." Mình chợt nhớ lại deal FPT × NVIDIA hồi năm ngoái — một cú đặt cược lớn vào AI infrastructure. Nên hôm nay mình muốn đào sâu hơn và chia sẻ với ae trên TechSnack.

Tháng 4/2024, FPT và NVIDIA công bố quan hệ đối tác chiến lược với kế hoạch đầu tư khoảng **200 triệu USD** để xây dựng **AI Factory** sử dụng công nghệ NVIDIA. Nhiều người nhìn vào con số và nghĩ đơn giản là FPT "gom" GPU H100 về làm dịch vụ. Nhưng nếu soi kỹ dưới góc độ engineering, đây là một nước đi chiến lược về **hạ tầng + hệ sinh thái**, mang lợi ích rõ ràng cho cả hai bên.

## FPT được gì từ deal này?

Thứ FPT đầu tư không chỉ là chip, mà là **toàn bộ AI stack của NVIDIA**.

Thông qua việc trở thành **NVIDIA Service Provider Partner** và hướng tới vai trò **Global System Integrator**, FPT có quyền tiếp cận sâu vào:

- GPU H100 / H200 Tensor Core
- NVIDIA AI Enterprise (software, framework, optimized runtime)
- Các framework như **NeMo** (train/fine-tune LLM) và **NVIDIA NIM** (tối ưu inference)
- Reference architecture cho AI workload chạy production

Điều này giúp FPT hoàn thiện chuỗi giá trị AI: **compute → platform → solution → service**, thay vì chỉ làm outsourcing hoặc application layer như trước.

Về mặt engineering, FPT có lợi thế:

- Rút ngắn đáng kể thời gian setup môi trường và deploy AI system
- TCO (Total Cost of Ownership) tốt hơn tới **45%** nhờ hạ tầng tối ưu
- Tối ưu hóa latency cho inference workload
- Build các giải pháp GenAI "may đo" cho từng ngành, không chỉ demo PoC

## Bài toán Sovereign AI và Cloud chủ quyền

Một điểm cực kỳ quan trọng là **AI Factory của FPT đóng vai trò như sovereign cloud**.

Với các domain nhạy cảm như Banking, Finance, Government hay Manufacturing, việc data không được "xuất ngoại" là requirement sống còn. Bằng cách build AI Factory tại **Việt Nam và Nhật Bản**, FPT cung cấp hạ tầng cho phép doanh nghiệp dùng sức mạnh của H100/H200 mà vẫn đảm bảo **data residency** và bảo mật tuyệt đối.

Đây là điểm mà các public cloud quốc tế đôi khi chưa đáp ứng linh hoạt được tại thị trường bản địa.

## NVIDIA được gì?

Với NVIDIA, đây không chỉ là bán thêm GPU.

FPT là một trong những tập đoàn công nghệ lớn nhất Việt Nam, có **network khách hàng rất rộng** ở Việt Nam, Nhật Bản, Hàn Quốc và nhiều thị trường khác. Thông qua FPT, NVIDIA:

- Mở rộng footprint tại Đông Nam Á bằng một đối tác bản địa mạnh
- Đẩy nhanh adoption của **CUDA + NVIDIA AI Enterprise** vào nhiều ngành công nghiệp
- Giảm friction khi tiếp cận các market yêu cầu sovereign AI
- Tạo ra các case study thực tế về AI chủ quyền

Deal này align rất rõ với tầm nhìn của Jensen Huang: **AI không chỉ nằm ở Big Tech Mỹ, mà cần được "localize" qua các hub khu vực.** FPT đóng vai trò như một "AI gateway" cho NVIDIA tại Việt Nam và một phần châu Á.

## Đây là win–win hay chỉ hype?

Nhìn từ góc độ kỹ thuật, đây là **win–win có điều kiện**.

- FPT có hạ tầng mạnh, nhưng bài toán khó là **build được AI solution đủ sâu**, không chỉ dừng ở infra
- NVIDIA có ecosystem mạnh, nhưng cần **đối tác địa phương đủ lớn** để scale adoption

Nếu FPT tận dụng được AI Factory để build **real production system** (banking, manufacturing, automotive…), thì đây là bước chuyển rất lớn từ IT services sang **AI infrastructure + AI solution provider**.

## Giờ đến lượt ae:

- Ae nhìn deal này thiên về **hạ tầng**, **dịch vụ**, hay **AI sản phẩm**?
- Sovereign AI có thực sự là lợi thế cạnh tranh dài hạn không?
- Với dev/engineer, liệu việc sở hữu hạ tầng GPU khủng có giúp ae dễ dàng triển khai các hệ thống RAG hay Fine-tuning quy mô lớn hơn không?

Cmt chia sẻ góc nhìn kỹ thuật của ae nhé!

**Happy building!**
