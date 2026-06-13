# Bảng thuật ngữ (Glossary) — Anh → Việt

Bảng này giữ cho cách dịch thuật ngữ **nhất quán xuyên suốt cả cuốn sách**. Khi gặp thuật ngữ mới, thêm vào đây trước. Quy ước: lần đầu xuất hiện trong mỗi chương ghi `tiếng Việt (english term)`, các lần sau dùng cột "Tiếng Việt". Kế thừa thuật ngữ chung từ `books/ddia/glossary.md` và `books/system-design/glossary.md` (cache, throughput, latency, scalability, load balancer, sharding, quorum…). Sách này về **mẫu thiết kế cho hệ phân tán dựa trên container/Kubernetes** nên giữ nguyên phần lớn thuật ngữ container.

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| distributed system | hệ phân tán | |
| design pattern | mẫu thiết kế (design pattern) | |
| container | container | giữ nguyên |
| containerized application | ứng dụng đóng gói container | |
| container image | image container | giữ "image" |
| container orchestrator | bộ điều phối container (orchestrator) | |
| Kubernetes | Kubernetes | giữ nguyên |
| Pod | Pod | giữ nguyên (đơn vị triển khai của Kubernetes) |
| node | nút (node) | |
| single-node pattern | mẫu đơn nút (single-node) | |
| multi-node pattern | mẫu đa nút (multi-node) | |
| sidecar | sidecar | giữ nguyên (mẫu sidecar) |
| ambassador | ambassador | giữ nguyên (mẫu ambassador) |
| adapter | adapter | giữ nguyên (mẫu adapter) |
| reusable component | thành phần tái sử dụng | |
| microservice | microservice | giữ nguyên |
| service | dịch vụ | |
| legacy service | dịch vụ kế thừa (legacy) | |
| API | API | giữ nguyên |
| SSL/TLS termination | kết thúc SSL/TLS (termination) | |
| reverse proxy | reverse proxy | giữ nguyên |
| service mesh | service mesh | giữ nguyên |
| replicated service | dịch vụ nhân bản | |
| replica | bản sao (replica) | |
| load balancing | cân bằng tải | |
| load balancer | bộ cân bằng tải | |
| stateless | không trạng thái | |
| stateful | có trạng thái | |
| readiness probe | đầu dò sẵn sàng (readiness probe) | |
| liveness probe | đầu dò sự sống (liveness probe) | |
| health check / health monitoring | kiểm tra sức khỏe / giám sát sức khỏe | |
| caching layer | tầng đệm (cache) | |
| cache hit / miss | trúng / trượt cache | |
| rate limiting | giới hạn tốc độ | |
| denial-of-service (DoS) | tấn công từ chối dịch vụ (DoS) | |
| session tracking | theo dõi phiên | |
| sticky session | phiên dính (sticky session) | |
| sharded service | dịch vụ phân mảnh (sharded) | |
| shard | mảnh (shard) | |
| sharding function | hàm phân mảnh | |
| sharding key | khóa phân mảnh | |
| consistent hashing | băm nhất quán (consistent hashing) | |
| hot shard / hot sharding | mảnh nóng (hot shard) | |
| shard router / shard routing service | dịch vụ định tuyến mảnh (shard router) | |
| re-sharding | tái phân mảnh (re-sharding) | |
| hit rate | tỷ lệ trúng (hit rate) | |
| memcache / Memcached | Memcached | giữ nguyên |
| scatter/gather | scatter/gather | giữ nguyên (mẫu phát tán/thu gom) |
| root distribution | phân phối tại gốc (root) | |
| leaf sharding | phân mảnh tại lá (leaf) | |
| fan-out / fan-in | fan-out / fan-in | giữ nguyên |
| tail latency | độ trễ đuôi (tail latency) | như ddia |
| function (FaaS) | hàm (function) | |
| Functions as a Service (FaaS) | Hàm-như-Dịch-vụ (FaaS) | giữ "FaaS" |
| serverless | serverless | giữ nguyên |
| event-driven | hướng sự kiện (event-driven) | |
| event | sự kiện | |
| trigger | trình kích hoạt (trigger) | |
| pipeline | pipeline | giữ nguyên |
| ownership | quyền sở hữu (ownership) | |
| leader election | bầu chọn leader (election) | |
| master election | bầu chọn master | |
| mutual exclusion lock | khóa loại trừ tương hỗ (mutex lock) | |
| distributed lock | khóa phân tán | |
| lease | hợp đồng thuê (lease) | |
| renewable lock | khóa gia hạn được (renewable lock) | |
| handoff | bàn giao (handoff) | |
| work queue | hàng đợi công việc (work queue) | |
| worker | worker | giữ nguyên |
| multi-worker pattern | mẫu đa worker (multi-worker) | đặc biệt hóa của mẫu adapter |
| source container interface | giao diện container nguồn (source) | cung cấp luồng đơn vị công việc |
| worker container interface | giao diện container worker | thực sự xử lý đơn vị công việc |
| work item | đơn vị công việc (work item) | |
| Job (Kubernetes) | đối tượng Job | giữ nguyên tên đối tượng |
| thumbnail | thumbnail | giữ nguyên |
| transcode | chuyển mã (transcode) | |
| interarrival time | thời gian giữa các lần đến (interarrival time) | tốc độ công việc mới đến |
| autoscaler | bộ tự co giãn (autoscaler) | |
| feast or famine | no dồn đói góp | tải lúc dồn dập lúc rỗng |
| batch processing | xử lý theo lô (batch) | |
| batch computational pattern | mẫu tính toán theo lô | |
| MapReduce | MapReduce | giữ nguyên |
| map / reduce / shuffle | map / reduce / shuffle | giữ nguyên |
| copier pattern | mẫu sao chép (copier) | |
| filter pattern | mẫu lọc (filter) | |
| splitter / merger | bộ tách (splitter) / bộ gộp (merger) | |
| join | join | giữ nguyên |
| coordinator | bộ điều phối (coordinator) | |
| idempotent | bất biến theo lần gọi (idempotent) | |
| retry | thử lại (retry) | |
| at-least-once / exactly-once | ít nhất một lần / đúng một lần | ngữ nghĩa giao hàng |
| throughput | thông lượng | |
| latency | độ trễ | |
| availability | tính sẵn sàng | |
| reliability | độ tin cậy | |
| scalability | khả năng mở rộng | |
| extensibility | khả năng mở rộng (extensibility) | khác scalability; ghi kèm tiếng Anh khi cần phân biệt |
| object-oriented programming | lập trình hướng đối tượng | |
| interface | interface | giữ nguyên |
| open source | mã nguồn mở | |
| client-server | client-server | giữ nguyên |
| mainframe | máy chủ lớn (mainframe) | |
| time-sharing | chia sẻ thời gian (time-sharing) | |
| deployment | triển khai (deployment) | |
| rollout / rollback | tung ra / hoàn tác (rollout/rollback) | |
| canary | canary | giữ nguyên (triển khai canary) |
| configuration | cấu hình | |
| parameterized container | container tham số hóa | |
| YAML manifest | tệp khai báo YAML (manifest) | |
| Docker | Docker | giữ nguyên |
| Prometheus / Fluentd / nginx / Redis | Prometheus / Fluentd / nginx / Redis | giữ nguyên |
| Hands On | Thực hành (Hands On) | tiêu đề mục thực hành |
| service discovery | phát hiện dịch vụ (service discovery) | |
| service broker | bộ trung gian dịch vụ (service broker) | ambassador làm trung gian dịch vụ |
| portable / portability | di động (portable) | ứng dụng chạy được qua nhiều môi trường |
| introspect | xem xét nội tại (introspect) | |
| request splitting | tách yêu cầu (request splitting) | |
| tee / teeing traffic | rẽ nhánh lưu lượng (tee) | nhân đôi lưu lượng để thử nghiệm |
| proxy | proxy | giữ nguyên |
| IP hashing | băm theo IP (IP hashing) | |
| StatefulSet / Service / ConfigMap | StatefulSet / Service / ConfigMap | giữ nguyên (đối tượng Kubernetes) |
| twemproxy | twemproxy | giữ nguyên (proxy cho Redis/Memcached) |
| key-value store | kho key-value | |
| decorator pattern | mẫu decorator | giữ "decorator" (mẫu trang trí) |
| two-factor authentication | xác thực hai yếu tố (two-factor authentication) | |
| webhook | webhook | giữ nguyên |
| event-based pipeline | pipeline dựa trên sự kiện | |
| event sink | điểm tiếp nhận sự kiện (event sink) | |
| background processing | xử lý nền (background processing) | |
| amortize | phân bổ (amortize) | |
| pay-per-request / pay-per-consumption | trả-theo-yêu-cầu / trả-theo-mức-tiêu-thụ | mô hình định giá |
| artifact | sản phẩm tạo tác (artifact) | |
| kubeless | kubeless | giữ nguyên (framework FaaS trên Kubernetes) |
| kubectl | kubectl | giữ nguyên (công cụ dòng lệnh Kubernetes) |
| affinity (IP/session) | tính tương thuộc (affinity) | ch05: ái lực địa chỉ IP/phiên |
| edge layer | tầng biên (edge layer) | ch05: tầng ngoài cùng (nginx) |
| Varnish | Varnish | giữ nguyên (web cache mã nguồn mở) |
| caching proxy / caching web proxy | proxy đệm (caching proxy) | ch05 |
| Deployment | Deployment | giữ nguyên (đối tượng Kubernetes) |
| secret | secret | giữ nguyên (đối tượng Kubernetes) |
| Let's Encrypt / openssl | Let's Encrypt / openssl | giữ nguyên |
| two pizza team | nhóm "hai chiếc pizza" | ch05: nhóm nhỏ vừa đủ ăn hai chiếc pizza |
| three-nines / 99.9% | ba số chín (99.9%) | ch05: mức tính sẵn sàng |
| SLA (service level agreement) | thỏa thuận mức dịch vụ (SLA) | |
| continuous delivery | phân phối liên tục (continuous delivery) | |
| horizontal scaling | mở rộng theo chiều ngang | |
| hit rate | tỷ lệ trúng cache (hit rate) | |
