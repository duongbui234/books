# Bảng thuật ngữ (Glossary) — Anh → Việt

Bảng này giữ cho cách dịch thuật ngữ **nhất quán xuyên suốt cả cuốn sách**. Khi gặp thuật ngữ mới, thêm vào đây trước. Quy ước: lần đầu xuất hiện trong mỗi chương ghi `tiếng Việt (english term)`, các lần sau dùng cột "Tiếng Việt". Kế thừa thuật ngữ chung từ `books/nodejs-design-patterns/glossary.md` và `books/pragmatic-programmer/glossary.md`.

**Nguyên tắc cho sách này:** *Clean Code* là sách về **thủ công viết mã**, nên giữ NGUYÊN tiếng Anh mọi từ khoá ngôn ngữ, tên API, tên nguyên tắc/mẫu thiết kế và thuật ngữ đã quá phổ biến trong giới lập trình Việt (`refactor`, `TDD`, `SOLID`, `mock`…). Chỉ dịch phần văn xuôi giải thích. **Tuyệt đối không dịch nội dung bên trong khối code, kể cả comment trong code** — vì bản thân tên biến/hàm chính là đối tượng bàn luận của cuốn sách.

## Khái niệm cốt lõi

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| clean code | clean code | giữ nguyên — tên sách, khái niệm trung tâm |
| bad code / messy code | mã tệ / mã bầy hầy | |
| mess | mớ hỗn độn | |
| craft / craftsmanship | tay nghề / tinh thần thợ lành nghề (craftsmanship) | |
| discipline | kỷ luật (discipline) | |
| code smell | code smell | giữ nguyên, chú thích "mùi mã" lần đầu |
| heuristic | kinh nghiệm thực hành (heuristic) | |
| the Boy Scout Rule | Quy tắc Hướng đạo sinh (the Boy Scout Rule) | |
| wading / slogging | lội bì bõm / lê lết | ẩn dụ của tác giả, giữ sắc thái |
| technical debt | nợ kỹ thuật (technical debt) | |
| rot | mục ruỗng | code rot → mã mục ruỗng |
| productivity | năng suất | |
| LeBlanc's law | định luật LeBlanc | "later equals never" |

## Đặt tên & hàm

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| meaningful name | tên có ý nghĩa | |
| intention-revealing name | tên bộc lộ ý định (intention-revealing name) | |
| disinformation | thông tin sai lệch | |
| encoding | mã hoá tên (encoding) | Hungarian notation… |
| scope | phạm vi (scope) | |
| variable / function / argument | biến / hàm / đối số | |
| class / method / module | class / method / module | giữ nguyên |
| package | package | giữ nguyên |
| function argument | đối số của hàm | |
| side effect | tác dụng phụ (side effect) | |
| command query separation | tách lệnh khỏi truy vấn (command query separation) | |
| the Stepdown Rule | Quy tắc bậc thang (the Stepdown Rule) | |
| switch statement | câu lệnh switch | |
| error code / exception | mã lỗi / exception | exception giữ nguyên |
| structured programming | lập trình có cấu trúc (structured programming) | |
| extract method | extract method | tên refactoring, giữ nguyên |
| refactor / refactoring | refactor / refactoring | giữ nguyên |
| abstraction | trừu tượng hoá (abstraction) | |
| level of abstraction | mức trừu tượng | |
| duplication | trùng lặp (duplication) | |
| DRY (Don't Repeat Yourself) | DRY | giữ nguyên |

## Comment & định dạng

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| comment | comment | giữ nguyên |
| good / bad comment | comment tốt / comment tệ | |
| noise comment | comment nhiễu | |
| formatting | định dạng (formatting) | |
| vertical / horizontal formatting | định dạng theo chiều dọc / chiều ngang | |
| indentation | thụt lề (indentation) | |
| the newspaper metaphor | ẩn dụ tờ báo (the newspaper metaphor) | |

## Đối tượng, class & thiết kế

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| object | đối tượng (object) | |
| data structure | cấu trúc dữ liệu (data structure) | |
| data abstraction | trừu tượng hoá dữ liệu | |
| data/object antisymmetry | tính phản đối xứng dữ liệu/đối tượng | |
| the Law of Demeter | Luật Demeter (the Law of Demeter) | |
| DTO (Data Transfer Object) | DTO | giữ nguyên |
| encapsulation | đóng gói (encapsulation) | |
| polymorphism | đa hình (polymorphism) | |
| inheritance | kế thừa (inheritance) | |
| interface | interface | giữ nguyên |
| implementation | hiện thực (implementation) | |
| coupling | độ kết dính giữa các thành phần (coupling) | |
| cohesion | độ gắn kết nội tại (cohesion) | |
| dependency | phụ thuộc (dependency) | |
| simple design | thiết kế đơn giản (simple design) | |
| YAGNI (You Aren't Gonna Need It) | YAGNI | giữ nguyên |
| continuous design | thiết kế liên tục (continuous design) | |

## SOLID & nguyên tắc thành phần

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| the SOLID principles | các nguyên tắc SOLID | giữ tên viết tắt |
| SRP: Single Responsibility Principle | SRP — Nguyên tắc Trách nhiệm Đơn nhất | giữ viết tắt EN |
| OCP: Open–Closed Principle | OCP — Nguyên tắc Đóng–Mở | |
| LSP: Liskov Substitution Principle | LSP — Nguyên tắc Thay thế Liskov | |
| ISP: Interface Segregation Principle | ISP — Nguyên tắc Phân tách Interface | |
| DIP: Dependency Inversion Principle | DIP — Nguyên tắc Đảo ngược Phụ thuộc | |
| component | component | giữ nguyên |
| component cohesion / coupling | độ gắn kết / kết dính của component | |
| REP, CCP, CRP, ADP, SDP, SAP | giữ nguyên viết tắt | dịch tên đầy đủ lần đầu |

## Kiểm thử

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| test | test | giữ nguyên |
| unit test | unit test | giữ nguyên |
| acceptance test | acceptance test | giữ nguyên, chú thích "kiểm thử chấp nhận" lần đầu |
| TDD (Test-Driven Development) | TDD | giữ nguyên |
| TCR (Test && Commit \|\| Revert) | TCR | giữ nguyên |
| test suite | bộ test (test suite) | |
| test coverage | độ phủ test (test coverage) | |
| mock / stub / spy / fake | mock / stub / spy / fake | giữ nguyên |
| assertion | assertion | giữ nguyên |
| F.I.R.S.T. | F.I.R.S.T. | giữ nguyên |
| domain-specific testing language | ngôn ngữ kiểm thử chuyên biệt miền | |
| the -ilities | các "-ilities" | khả năng bảo trì, mở rộng… |
| red-green-refactor | red-green-refactor | giữ nguyên |
| regression | hồi quy (regression) | |

## Kiến trúc

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| architecture | kiến trúc (architecture) | |
| the Clean Architecture | Clean Architecture | giữ nguyên |
| architectural boundary | ranh giới kiến trúc (architectural boundary) | |
| clean boundary | ranh giới sạch | |
| use case | use case | giữ nguyên |
| entity | entity | giữ nguyên |
| business rule | quy tắc nghiệp vụ (business rule) | |
| plugin architecture | kiến trúc plugin | |
| independence / independently deployable | tính độc lập / triển khai độc lập được | |
| decoupling | tách rời (decoupling) | |
| the two values of software | hai giá trị của phần mềm | behavior & structure |
| behavior / structure | hành vi / cấu trúc | |
| keeping options open | giữ cho các lựa chọn còn ngỏ | |

## Đồng thời (concurrency)

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| concurrency | đồng thời (concurrency) | |
| thread | luồng (thread) | |
| thread-safe | an toàn luồng (thread-safe) | |
| race condition | race condition | giữ nguyên |
| deadlock / livelock | deadlock / livelock | giữ nguyên |
| starvation | starvation | giữ nguyên |
| synchronization | đồng bộ hoá (synchronization) | |
| lock | lock | giữ nguyên |
| shared data | dữ liệu dùng chung | |

## Nghề nghiệp & AI

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| professional / professionalism | chuyên nghiệp / tính chuyên nghiệp | |
| harm | tổn hại (harm) | chương 28 |
| defect | lỗi (defect) | |
| repeatable proof | bằng chứng lặp lại được | |
| small cycles | chu kỳ nhỏ | |
| relentless improvement | cải tiến không ngừng | |
| estimate | ước lượng (estimate) | |
| stakeholder | bên liên quan (stakeholder) | |
| pair programming | pair programming | giữ nguyên |
| continuous integration | tích hợp liên tục (continuous integration) | |
| LLM (large language model) | LLM (mô hình ngôn ngữ lớn) | giữ viết tắt EN |
| AI | AI | giữ nguyên |
| prompt / programming by prompt | prompt / lập trình bằng prompt | |
| generated code | mã do AI sinh ra | |
