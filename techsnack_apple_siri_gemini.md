# [#TechSnack 10] | Apple x Google Gemini: Khi "người khổng lồ" chọn gốc rễ

Thỏa thuận nhiều năm giữa Apple và Google để đưa Gemini vào sâu trong iOS không đơn thuần là một bản hợp đồng thương mại. Đó là lời giải cho bài toán: Khi cơn sốt (hype) qua đi, đâu là thứ thực sự neo đậu lại trong một sản phẩm 2 tỷ người dùng?

Việc Sam Altman chứng kiến ChatGPT bị đẩy xuống vai trò "phụ tá" cho các truy vấn phức tạp, nhường sân diễn mặc định cho Gemini, đã để lại một câu hỏi lớn: **Tại sao Apple lại chọn Google?**

---

## Apple không chọn theo benchmark

Apple không chọn model dựa trên điểm số benchmark hay sự hào nhoáng của các bản demo. Họ chọn dựa trên khả năng "thực chiến" ở quy mô 2 tỷ thiết bị.

Trong khi OpenAI có thể tạo ra những bước nhảy vọt đầy kinh ngạc, họ vẫn thiếu một thứ cốt tử: **sự tự chủ hoàn toàn về hạ tầng**. OpenAI vẫn đang phải nương nhờ vào Microsoft Azure. Google thì khác – họ nắm giữ cả model lẫn hệ sinh thái đám mây riêng biệt, từ TPU cho đến data center.

Apple không tìm kiếm model thông minh nhất tại một thời điểm nhất định. Họ tìm kiếm một đối tác có khả năng vận hành ổn định trong 10 năm tới.

---

## Inference at Scale – Điểm mấu chốt của deal

Google đã chứng minh được năng lực vận hành AI trên hàng trăm triệu thiết bị Samsung Galaxy. Với Apple, đó là bằng chứng về sự ổn định – thứ họ đặt làm ưu tiên tối thượng.

Kiến trúc Apple áp dụng là **Hybrid AI**: kết hợp giữa xử lý on-device và cloud.
- **On-device**: Các task đơn giản như tóm tắt thông báo, chỉnh sửa ảnh chạy trên Apple Neural Engine
- **Cloud (Gemini)**: Với các truy vấn cần "world knowledge" hoặc tính toán nặng, Siri sẽ chuyển tiếp sang Gemini

Sự kết hợp này đòi hỏi một nền tảng hạ tầng cực kỳ bền bỉ. Google có cả model lẫn cloud riêng, trong khi OpenAI vẫn phải phụ thuộc Microsoft. Đó là điểm khác biệt quyết định.

---

## Privacy không phải marketing

Với Apple, Privacy là một **system design decision**. Khi tích hợp Gemini, họ sử dụng **Private Cloud Compute (PCC)** – một lớp bọc để đảm bảo:
- Mọi dữ liệu gửi đi đều được anonymization (ẩn danh hóa)
- Google cam kết không lưu trữ hay dùng dữ liệu này để train model

Việc Apple nhấn mạnh vào tiêu chuẩn bảo mật khi tích hợp Gemini cho thấy họ tìm thấy ở Google một sự tương đồng trong cách thiết kế hệ thống có kiểm soát. Apple không cần sở hữu bộ não, họ chỉ cần kiểm soát tay chân và phản xạ của hệ điều hành.

---

## Bài học về giá trị cốt lõi

Giới công nghệ rất dễ bị cuốn theo những "cơn sốt" nhất thời. Nhưng khi xây dựng một sản phẩm mang tính di sản, những kỹ sư tại Apple đã chọn nhìn vào gốc rễ.

Sự chiến thắng của Google trong thương vụ này không đến từ việc họ có model "thông minh nhất" tại một thời điểm nhất định, mà đến từ sự cặm cụi xây dựng hạ tầng suốt hàng thập kỷ. OpenAI có thể có những bước nhảy vọt, nhưng Google có nền móng vững chãi để đảm bảo sự ổn định cho hàng tỷ người dùng.

---

## Tóm lại

- Apple chọn Gemini vì khả năng **inference at scale** – không phải benchmark
- **Hybrid AI** (on-device + cloud) là kiến trúc mặc định cho sản phẩm consumer
- **Private Cloud Compute** giữ vững lời hứa bảo mật khi dùng AI bên thứ ba
- Google thắng nhờ **hạ tầng tự chủ** (TPU + Cloud) được xây dựng suốt hàng thập kỷ

---

## Giờ đến lượt ae:

- Ae nghĩ OpenAI có nên đầu tư hạ tầng riêng để thoát khỏi sự phụ thuộc vào Microsoft không?
- Với kinh nghiệm của ae, "gốc rễ" (infrastructure) quan trọng thế nào khi scale một ứng dụng AI?

**Happy coding!! 😁**
