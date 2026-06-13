# Bảng thuật ngữ (Glossary) — Anh → Việt

Bảng này giữ cho cách dịch thuật ngữ **nhất quán xuyên suốt cả cuốn sách**. Khi gặp thuật ngữ mới, thêm vào đây trước. Quy ước: lần đầu xuất hiện trong mỗi chương ghi `tiếng Việt (english term)`, các lần sau dùng cột "Tiếng Việt". Kế thừa toàn bộ thuật ngữ chung từ `books/system-design/glossary.md` (Alex Xu) và `books/ddia/glossary.md` (database, cache, throughput, latency, sharding, CAP, consistent hashing, load balancer…). Bảng dưới chỉ ghi thêm các thuật ngữ **riêng của cuốn Grokking** hoặc cần thống nhất lại.

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| Grokking | Grokking | giữ nguyên tên sách |
| functional / non-functional requirements | yêu cầu chức năng / phi chức năng | |
| capacity estimation and constraints | ước lượng dung lượng và ràng buộc | |
| system interface definition | định nghĩa giao diện hệ thống | |
| data model | mô hình dữ liệu | |
| detailed design / component design | thiết kế chi tiết / thiết kế thành phần | |
| identifying and resolving bottlenecks | xác định và xử lý điểm nghẽn | |
| read-heavy / write-heavy | thiên về đọc / thiên về ghi | |
| read:write ratio | tỉ lệ đọc:ghi | |
| key generation service (KGS) | dịch vụ sinh khóa (KGS) | giữ "KGS" — TinyURL |
| encoding actual URL | mã hóa URL gốc | |
| MD5 / SHA256 | MD5 / SHA256 | giữ nguyên |
| purging / DB cleanup | dọn dẹp / làm sạch CSDL | |
| telemetry | đo từ xa (telemetry) | |
| Pastebin | Pastebin | giữ nguyên |
| Instagram / news feed generation | Instagram / tạo bảng tin | |
| metadata | siêu dữ liệu (metadata) | |
| data deduplication | khử trùng lặp dữ liệu (deduplication) | Dropbox |
| chunking | chia khối (chunking) | |
| synchronization service | dịch vụ đồng bộ | |
| message queuing service | dịch vụ hàng đợi thông điệp | |
| cloud/block storage | kho đám mây / kho khối | |
| timeline generation | tạo dòng thời gian (timeline) | Twitter |
| video encoding / transcoding | mã hóa / chuyển mã video | YouTube |
| thumbnail | ảnh thu nhỏ (thumbnail) | |
| typeahead suggestion | gợi ý gõ trước (typeahead) | |
| trie / prefix tree | cây trie (cây tiền tố) | |
| top suggestions | gợi ý hàng đầu | |
| inverted index | chỉ mục ngược (inverted index) | Twitter Search |
| aggregator server | máy chủ tổng hợp (aggregator) | |
| QuadTree | QuadTree | giữ nguyên — Yelp/Uber |
| geohash | geohash | giữ nguyên |
| dynamic segment | phân đoạn động | Yelp |
| pull / push model | mô hình kéo / đẩy | Uber |
| ticket booking / reservation | đặt vé / giữ chỗ | Ticketmaster |
| linearizable / serializable | tuyến tính hóa được / tuần tự hóa được | giữ kèm tiếng Anh |
| ACID transaction | giao dịch ACID | |
| reserved booking / hold | giữ chỗ tạm (hold) | |
| wait list | danh sách chờ | |
| reverse proxy | proxy ngược (reverse proxy) | |
| forward proxy | proxy xuôi (forward proxy) | |
| collapsed forwarding | gộp chuyển tiếp (collapsed forwarding) | |
| cache eviction policy | chính sách loại bỏ cache | |
| LRU (least recently used) | LRU (ít dùng gần đây nhất) | giữ "LRU" |
| write-through / write-back / write-around | ghi xuyên / ghi lại / ghi vòng | chiến lược cache |
| distributed system | hệ thống phân tán | |
| scalability / reliability / availability / efficiency | khả mở rộng / độ tin cậy / tính sẵn sàng / hiệu quả | đặc tính cốt lõi |
| manageability / serviceability | khả năng quản trị / bảo trì | |
| redundancy | dự phòng (redundancy) | |
| Server-Sent Events (SSE) | Sự kiện do máy chủ đẩy (SSE) | giữ "SSE" |
| fanout / fanout-on-write / fanout-on-load | fanout / fanout-on-write / fanout-on-load | giữ nguyên — Facebook Newsfeed |
| newsfeed / feed generation / feed publishing | newsfeed / tạo feed / đăng feed | giữ "newsfeed", "feed" |
| web crawler / spider / bot | web crawler | giữ "web crawler"; lần đầu chú "(trình thu thập dữ liệu web)" — Web Crawler |
| URL frontier | URL frontier | giữ nguyên; lần đầu chú "(biên giới URL)" |
| seed URL / seed set | URL gốc (seed URL) / tập gốc (seed set) | |
| Robots Exclusion Protocol / robot.txt | Robots Exclusion Protocol / robot.txt | giữ nguyên |
| Document Input Stream (DIS) | Document Input Stream (DIS) | giữ "DIS" |
| dedupe test / dedupe | phép kiểm tra khử trùng lặp / dedupe | |
| checksum | checksum | giữ nguyên |
| bloom filter / false positive / false negative | bloom filter / dương tính giả / âm tính giả | giữ "bloom filter" |
| crawler trap | bẫy crawler (crawler trap) | |
| checkpointing | checkpointing (lập điểm kiểm) | |
| path-ascending crawling | path-ascending crawling (thu thập leo đường dẫn) | |
| MIME type | kiểu MIME | giữ "MIME" |
| sharding / shard | phân vùng (sharding) / shard | Grokking giữ "shard" nguyên; "sharding" để cạnh "phân vùng dữ liệu" |
| single point of failure | điểm hỏng đơn lẻ (single point of failure) | thống nhất "đơn lẻ" trong cuốn Grokking |
| horizontal / vertical scaling | mở rộng ngang / mở rộng dọc | dạng rút gọn dùng trong ch17 |
| health check | kiểm tra sức khỏe (health check) | Load Balancing |
| locality of reference | cục bộ tham chiếu (locality of reference) | Caching |
| failover | chuyển dự phòng (failover) | Redundancy and Replication |
