# Bảng thuật ngữ (Glossary) — Anh → Việt

Bảng này giữ cho cách dịch thuật ngữ **nhất quán xuyên suốt cả cuốn sách**. Khi gặp thuật ngữ mới, thêm vào đây trước. Quy ước: lần đầu xuất hiện trong mỗi chương ghi `tiếng Việt (english term)`, các lần sau dùng cột "Tiếng Việt". Kế thừa các thuật ngữ chung từ `books/ddia/glossary.md` (database, cache, throughput, latency, scalability…).

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| system design interview | phỏng vấn thiết kế hệ thống | |
| back-of-the-envelope estimation | ước lượng nhanh trên giấy (back-of-the-envelope) | giữ kèm tiếng Anh lần đầu |
| scale / scaling | mở rộng | |
| vertical scaling / scale up | mở rộng theo chiều dọc | |
| horizontal scaling / scale out | mở rộng theo chiều ngang | |
| web tier | tầng web | |
| data tier | tầng dữ liệu | |
| cache tier | tầng đệm | |
| load balancer | bộ cân bằng tải | |
| database replication | sao chép cơ sở dữ liệu | |
| master/slave | master/slave | giữ nguyên, chú thích chủ/tớ lần đầu |
| failover | chuyển đổi dự phòng (failover) | |
| CDN (content delivery network) | mạng phân phối nội dung (CDN) | giữ "CDN" |
| stateless | không trạng thái | |
| stateful | có trạng thái | |
| sticky session | phiên dính (sticky session) | |
| session data | dữ liệu phiên | |
| data center | trung tâm dữ liệu | |
| geoDNS | geoDNS | giữ nguyên |
| message queue | hàng đợi thông điệp | |
| producer / consumer | bên sản xuất / bên tiêu thụ (producer/consumer) | |
| publisher / subscriber | bên phát / bên đăng ký (pub/sub) | |
| logging / metrics / automation | ghi log / số liệu / tự động hóa | |
| sharding | phân mảnh (sharding) | giữ kèm tiếng Anh |
| shard / sharding key | mảnh (shard) / khóa phân mảnh | |
| resharding | tái phân mảnh | |
| celebrity problem / hotspot key | vấn đề người nổi tiếng / khóa điểm nóng | |
| denormalization | phi chuẩn hóa | |
| QPS (queries per second) | QPS (truy vấn/giây) | giữ "QPS" |
| peak QPS | QPS đỉnh | |
| DAU (daily active users) | DAU (người dùng hoạt động hằng ngày) | giữ "DAU" |
| SLA | SLA | giữ nguyên |
| availability | tính sẵn sàng | |
| rate limiter / rate limiting | bộ giới hạn tốc độ / giới hạn tốc độ | |
| throttle / throttling | tiết lưu (throttling) | |
| token bucket | thùng token (token bucket) | |
| leaking bucket | thùng rò (leaking bucket) | |
| sliding window | cửa sổ trượt | |
| fixed window counter | bộ đếm cửa sổ cố định | |
| consistent hashing | băm nhất quán (consistent hashing) | |
| hash ring | vòng băm | |
| virtual node | nút ảo | |
| key-value store | kho khóa-giá trị (key-value store) | |
| CAP theorem | định lý CAP | |
| consistency | tính nhất quán | |
| partition tolerance | chịu phân mảnh mạng (partition tolerance) | |
| quorum | nhóm túc số (quorum) | như ddia |
| eventual consistency | nhất quán cuối cùng | |
| vector clock | đồng hồ vector | |
| gossip protocol | giao thức gossip | |
| hinted handoff | bàn giao có gợi ý (hinted handoff) | |
| anti-entropy | chống entropy (anti-entropy) | |
| Merkle tree | cây Merkle | |
| tombstone | bia mộ (tombstone) | |
| SSTable / memtable | SSTable / memtable | giữ nguyên |
| Bloom filter | bộ lọc Bloom | |
| unique ID generator | bộ sinh ID duy nhất | |
| ticket server | máy chủ cấp vé (ticket server) | |
| snowflake | snowflake | giữ nguyên (cách tiếp cận Twitter) |
| URL shortener | bộ rút gọn URL | |
| hash collision | đụng độ băm | |
| base 62 conversion | chuyển cơ số 62 | |
| redirect (301/302) | chuyển hướng (301/302) | |
| web crawler | trình thu thập web (web crawler) | |
| seed URLs | các URL hạt giống | |
| URL frontier | biên giới URL (URL frontier) | giữ kèm tiếng Anh |
| politeness | tính lịch sự (politeness) | crawler |
| freshness | độ tươi mới | |
| robots.txt | robots.txt | giữ nguyên |
| spider trap | bẫy nhện (spider trap) | |
| notification system | hệ thống thông báo | |
| push notification | thông báo đẩy | |
| fanout | fan-out | giữ nguyên như ddia |
| fanout on write / on read | fan-out lúc ghi / lúc đọc | |
| news feed | bảng tin (news feed) | |
| chat system | hệ thống chat | giữ "chat" |
| WebSocket | WebSocket | giữ nguyên |
| long polling | long polling | giữ nguyên, chú thích lần đầu |
| heartbeat | nhịp tim (heartbeat) | |
| online presence | trạng thái trực tuyến (presence) | |
| service discovery | khám phá dịch vụ (service discovery) | |
| search autocomplete | gợi ý tìm kiếm tự động (autocomplete) | |
| trie | cây trie | |
| data sampling | lấy mẫu dữ liệu | |
| browser cache | bộ nhớ đệm trình duyệt | |
| video transcoding | chuyển mã video (transcoding) | |
| DAG (directed acyclic graph) | đồ thị có hướng không chu trình (DAG) | giữ "DAG" |
| presigned URL | URL ký sẵn (presigned URL) | |
| blob storage | kho blob | |
| block server | máy chủ khối (block server) | Google Drive |
| delta sync | đồng bộ phần thay đổi (delta sync) | |
| compression | nén | |
| conflict resolution | giải quyết xung đột | |
| cold storage | kho lưu trữ lạnh | |
| API gateway | API gateway | giữ nguyên |
| microservice | microservice | giữ nguyên |
| single point of failure | điểm hỏng đơn (single point of failure) | |
| back-of-envelope | ước lượng nhanh | |
| power of two | lũy thừa của 2 | |
| 99th percentile | phân vị thứ 99 | như ddia |
| interviewer / interviewee / candidate | người phỏng vấn / ứng viên | |
| high-level design | thiết kế tổng quan (high-level design) | |
| deep dive | đào sâu (deep dive) | |
| wrap up | tổng kết | |
| requirements clarification | làm rõ yêu cầu | |
| trade-off | đánh đổi (trade-off) | |
| back-end / front-end | back-end / front-end | giữ nguyên |
