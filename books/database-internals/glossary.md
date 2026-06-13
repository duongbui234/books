# Bảng thuật ngữ (Glossary) — Anh → Việt

Bảng này giữ cho cách dịch thuật ngữ **nhất quán xuyên suốt cả cuốn sách**. Khi gặp thuật ngữ mới, thêm vào đây trước. Quy ước: lần đầu xuất hiện trong mỗi chương ghi `tiếng Việt (english term)`, các lần sau dùng cột "Tiếng Việt". Kế thừa toàn bộ thuật ngữ chung từ `books/ddia/glossary.md` (database, cache, throughput, latency, replication, partitioning, consistency, CAP, quorum, leader/follower…) và `books/system-design/glossary.md`. Bảng dưới chỉ ghi thêm các thuật ngữ **riêng/đặc thù cuốn Database Internals** (cốt lõi về storage engine + hệ phân tán).

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| storage engine | bộ máy lưu trữ (storage engine) | giữ kèm tiếng Anh lần đầu |
| DBMS (database management system) | hệ quản trị cơ sở dữ liệu (DBMS) | giữ "DBMS" |
| query processor / query optimizer | bộ xử lý truy vấn / bộ tối ưu truy vấn | |
| execution engine / execution plan | bộ thực thi / kế hoạch thực thi | |
| transport subsystem | phân hệ truyền vận | |
| OLTP / OLAP / HTAP | OLTP / OLAP / HTAP | giữ nguyên |
| row-oriented / column-oriented | hướng hàng / hướng cột | |
| wide column store | kho lưu cột rộng (wide column store) | |
| data file / index file | tệp dữ liệu / tệp chỉ mục | |
| primary index / secondary index | chỉ mục chính / chỉ mục phụ | |
| clustered / nonclustered index | chỉ mục gom cụm / không gom cụm | |
| index-organized table (IOT) | bảng tổ chức theo chỉ mục (IOT) | |
| heap file | tệp heap (heap file) | giữ kèm tiếng Anh |
| page / block | trang (page) / khối (block) | |
| slotted page | trang có khe (slotted page) | giữ kèm tiếng Anh |
| cell (key cell / key-value cell) | ô (cell) | giữ kèm tiếng Anh lần đầu |
| offset | độ dời (offset) | |
| B-Tree / B+Tree | B-Tree / B+Tree | giữ nguyên |
| binary search tree (BST) | cây tìm kiếm nhị phân (BST) | |
| tree balancing | cân bằng cây | |
| fanout | độ phân nhánh (fanout) | giữ kèm tiếng Anh |
| occupancy | độ lấp đầy (occupancy) | |
| separator key | khóa phân tách (separator key) | |
| high key | khóa biên (high key) | |
| sibling pointer / link | con trỏ/liên kết anh em (sibling) | |
| rightmost pointer | con trỏ cực phải | |
| overflow page | trang tràn (overflow page) | |
| node split / merge | tách / gộp nút | |
| rebalancing | tái cân bằng | |
| bulk loading | nạp hàng loạt (bulk loading) | |
| breadcrumb | dấu vết đường đi (breadcrumb) | giữ kèm tiếng Anh |
| HDD / SSD | HDD / SSD | giữ nguyên |
| sector / track / cylinder | cung từ / rãnh / trụ | đĩa cứng |
| seek / rotational latency | thời gian tìm kiếm / trễ quay | |
| sequential / random I/O | I/O tuần tự / ngẫu nhiên | |
| write amplification | khuếch đại ghi (write amplification) | |
| read amplification | khuếch đại đọc (read amplification) | |
| space amplification | khuếch đại không gian | |
| garbage collection | thu gom rác (garbage collection) | |
| compaction | nén-gộp (compaction) | giữ kèm tiếng Anh; LSM |
| fragmentation / defragmentation | phân mảnh / chống phân mảnh | |
| vacuum | dọn dẹp (vacuum) | |
| WAL (write-ahead log) | nhật ký ghi-trước (WAL) | giữ "WAL" |
| log-structured storage | lưu trữ dạng nhật ký (log-structured) | |
| LSM Tree | LSM Tree | giữ nguyên |
| memtable / SSTable | memtable / SSTable | giữ nguyên |
| immutability / immutable | tính bất biến / bất biến | |
| buffering | đệm (buffering) | |
| buffer pool / page cache | vùng đệm trang (buffer pool) / page cache | |
| checksum / checksumming | tổng kiểm (checksum) | |
| binary encoding | mã hóa nhị phân | |
| variable-size data | dữ liệu kích thước thay đổi | |
| bit-packing | đóng gói bit (bit-packing) | |
| transaction processing | xử lý giao dịch | |
| recovery | phục hồi (recovery) | |
| ACID | ACID | giữ nguyên |
| atomicity / isolation / durability | tính nguyên tử / cô lập / bền vững | |
| isolation level | mức cô lập | |
| concurrency control | điều khiển tương tranh | |
| pessimistic / optimistic concurrency control | điều khiển tương tranh bi quan / lạc quan | |
| lock / latch | khóa (lock) / chốt (latch) | latch giữ kèm tiếng Anh |
| deadlock | bế tắc (deadlock) | |
| MVCC (multiversion concurrency control) | điều khiển tương tranh đa phiên bản (MVCC) | giữ "MVCC" |
| serializability | tính khả tuần tự (serializability) | |
| read/write anomaly | dị thường đọc/ghi | |
| dirty read / phantom read | đọc bẩn / đọc bóng ma | |
| ARIES | ARIES | giữ nguyên (thuật toán recovery) |
| steal / no-steal, force / no-force | steal/no-steal, force/no-force | giữ nguyên |
| undo / redo | undo / redo | giữ nguyên |
| Bw-Tree / Cache-oblivious B-Tree | Bw-Tree / Cache-oblivious B-Tree | giữ nguyên |
| FD-Tree / lazy B-Tree | FD-Tree / lazy B-Tree | giữ nguyên |
| copy-on-write | sao-khi-ghi (copy-on-write) | |
| distributed system | hệ phân tán | |
| node / process / participant | nút / tiến trình / bên tham gia | |
| message passing | truyền thông điệp | |
| link (fair-loss / stubborn / perfect) | kênh (fair-loss/stubborn/perfect link) | giữ nguyên phân loại |
| network partition | phân vùng mạng (network partition) | |
| partial failure | lỗi cục bộ (partial failure) | |
| asynchronous / synchronous system | hệ bất đồng bộ / đồng bộ | |
| failure detector | bộ phát hiện lỗi (failure detector) | |
| heartbeat | nhịp tim (heartbeat) | giữ kèm tiếng Anh |
| gossip protocol | giao thức gossip | giữ "gossip" |
| phi-accrual failure detector | bộ phát hiện lỗi phi-accrual | giữ nguyên |
| leader election | bầu chọn leader | giữ "leader" |
| bully algorithm | thuật toán bully | giữ nguyên |
| anti-entropy | anti-entropy | giữ nguyên |
| dissemination | lan truyền (dissemination) | |
| read repair / hinted handoff | sửa-khi-đọc (read repair) / hinted handoff | giữ nguyên |
| Merkle tree | cây Merkle | |
| Bitmap / Bloom filter | Bitmap / bộ lọc Bloom | |
| consistency model | mô hình nhất quán | |
| linearizability | tính tuyến tính hóa (linearizability) | |
| sequential / causal consistency | nhất quán tuần tự / nhân quả | |
| eventual consistency | nhất quán cuối cùng (eventual consistency) | |
| tunable consistency | nhất quán điều chỉnh được | |
| session guarantees | bảo đảm phiên | |
| CRDT | CRDT | giữ nguyên |
| distributed transaction | giao dịch phân tán | |
| two-phase commit (2PC) / 3PC | commit hai pha (2PC) / ba pha (3PC) | |
| coordinator / cohort | bên điều phối (coordinator) / bên tham gia (cohort) | |
| Calvin / Spanner / Percolator | Calvin / Spanner / Percolator | giữ nguyên tên hệ thống |
| consensus | đồng thuận (consensus) | |
| Paxos / Multi-Paxos / Fast Paxos | Paxos / Multi-Paxos / Fast Paxos | giữ nguyên |
| proposer / acceptor / learner | bên đề xuất / bên chấp nhận / bên học | Paxos |
| Raft / leader / term | Raft / leader / nhiệm kỳ (term) | giữ nguyên Raft |
| ZAB (Zookeeper Atomic Broadcast) | ZAB | giữ nguyên |
| atomic broadcast / total order broadcast | quảng bá nguyên tử / quảng bá thứ tự toàn cục | |
| virtual synchrony | đồng bộ ảo (virtual synchrony) | |
| quorum | quorum | giữ nguyên |
| split brain | split brain | giữ nguyên, chú thích "não phân liệt" lần đầu |
| FLP impossibility | bất khả thi FLP | |
| Byzantine fault tolerance (BFT) | dung lỗi Byzantine (BFT) | |
| logical clock / Lamport clock | đồng hồ logic / đồng hồ Lamport | |
| vector clock | đồng hồ vector | |
| happens-before | xảy-ra-trước (happens-before) | |
