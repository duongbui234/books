# Bảng thuật ngữ (Glossary) — Anh → Việt

Bảng này giữ cho cách dịch thuật ngữ **nhất quán xuyên suốt cả cuốn sách**. Khi gặp thuật ngữ mới, thêm vào đây trước. Quy ước: lần đầu xuất hiện trong mỗi chương ghi `tiếng Việt (english term)`, các lần sau dùng cột "Tiếng Việt". Kế thừa thuật ngữ từ `books/clean-code/glossary.md` (cùng tác giả, nhiều khái niệm trùng) và `books/building-microservices/glossary.md`.

**Nguyên tắc cho sách này:** *Clean Architecture* bàn về **cấu trúc phần mềm ở mức hệ thống**. Giữ NGUYÊN tiếng Anh mọi tên nguyên tắc (SOLID, SRP, OCP, LSP, ISP, DIP, REP, CCP, CRP, ADP, SDP, SAP), tên mẫu kiến trúc, tên ngôn ngữ/công nghệ, và mọi định danh mã. Chỉ dịch văn xuôi giải thích. **Không dịch nội dung trong khối code.** Tên hình (`Figure N.M`) giữ nguyên số hiệu.

## Khái niệm cốt lõi

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| architecture | kiến trúc (architecture) | |
| design | thiết kế (design) | tác giả khẳng định hai từ này là một |
| clean architecture | Clean Architecture | giữ nguyên — tên sách |
| software structure | cấu trúc phần mềm | |
| the two values of software | hai giá trị của phần mềm | behavior & structure |
| behavior | hành vi (behavior) | |
| structure | cấu trúc (structure) | |
| urgent / important | khẩn cấp / quan trọng | ma trận Eisenhower |
| Eisenhower's matrix | ma trận Eisenhower | |
| craftsman / craftsmanship | người thợ lành nghề / tay nghề | |
| effort | công sức | |
| human resources | nhân lực | |
| mess | mớ hỗn độn | |
| rot | mục ruỗng | |
| technical debt | nợ kỹ thuật (technical debt) | |
| the Boy Scout Rule | Quy tắc Hướng đạo sinh | |

## Ba mô thức lập trình

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| paradigm | mô thức (paradigm) | |
| structured programming | lập trình có cấu trúc (structured programming) | |
| object-oriented programming (OO) | lập trình hướng đối tượng (OO) | giữ viết tắt OO |
| functional programming | lập trình hàm (functional programming) | |
| direct transfer of control | chuyển điều khiển trực tiếp | |
| indirect transfer of control | chuyển điều khiển gián tiếp | |
| assignment | phép gán (assignment) | |
| immutability | tính bất biến (immutability) | |
| mutable / immutable | khả biến / bất biến | |
| encapsulation | đóng gói (encapsulation) | |
| inheritance | kế thừa (inheritance) | |
| polymorphism | đa hình (polymorphism) | |
| dependency inversion | đảo ngược phụ thuộc (dependency inversion) | |
| plugin architecture | kiến trúc plugin | |
| event sourcing | event sourcing | giữ nguyên |
| functional decomposition | phân rã theo hàm | |
| formal proof | chứng minh hình thức | |
| falsifiable | khả bác bỏ (falsifiable) | |

## Nguyên tắc SOLID

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| the SOLID principles | các nguyên tắc SOLID | giữ viết tắt |
| SRP: Single Responsibility Principle | SRP — Nguyên tắc Trách nhiệm Đơn nhất | giữ viết tắt EN |
| OCP: Open-Closed Principle | OCP — Nguyên tắc Đóng–Mở | |
| LSP: Liskov Substitution Principle | LSP — Nguyên tắc Thay thế Liskov | |
| ISP: Interface Segregation Principle | ISP — Nguyên tắc Phân tách Interface | |
| DIP: Dependency Inversion Principle | DIP — Nguyên tắc Đảo ngược Phụ thuộc | |
| actor | actor | giữ nguyên — "một module chỉ chịu trách nhiệm trước một actor" |
| stakeholder | bên liên quan (stakeholder) | |
| abstract class / interface | abstract class / interface | giữ nguyên |
| concrete class | class cụ thể (concrete class) | |
| volatile | dễ biến động (volatile) | |
| source code dependency | phụ thuộc mã nguồn | |
| flow of control | luồng điều khiển | |
| substitutability | khả năng thay thế (substitutability) | |

## Nguyên tắc thành phần

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| component | component | giữ nguyên |
| deployable unit | đơn vị triển khai | |
| relocatability | khả năng tái định vị (relocatability) | |
| linker / loader | linker / loader | giữ nguyên |
| component cohesion | độ gắn kết của component | |
| component coupling | độ kết dính giữa các component | |
| REP: Reuse/Release Equivalence Principle | REP — Nguyên tắc Tương đương Tái dùng/Phát hành | giữ viết tắt |
| CCP: Common Closure Principle | CCP — Nguyên tắc Đóng chung | |
| CRP: Common Reuse Principle | CRP — Nguyên tắc Tái dùng chung | |
| ADP: Acyclic Dependencies Principle | ADP — Nguyên tắc Phụ thuộc Phi chu trình | |
| SDP: Stable Dependencies Principle | SDP — Nguyên tắc Phụ thuộc Ổn định | |
| SAP: Stable Abstractions Principle | SAP — Nguyên tắc Trừu tượng Ổn định | |
| dependency cycle | chu trình phụ thuộc | |
| the morning after syndrome | hội chứng "sáng hôm sau" | |
| weekly build | build hằng tuần | |
| stability | độ ổn định (stability) | |
| stable / unstable | ổn định / bất ổn định | |
| fan-in / fan-out | fan-in / fan-out | giữ nguyên |
| instability (I) | độ bất ổn định (I) | công thức I = Fan-out ÷ (Fan-in + Fan-out) |
| abstractness (A) | độ trừu tượng (A) | |
| the main sequence | đường chính (the main sequence) | |
| zone of pain / zone of uselessness | vùng đau đớn / vùng vô dụng | |
| distance from the main sequence (D) | khoảng cách tới đường chính (D) | |

## Kiến trúc

| English | Tiếng Việt | Ghi chú |
|---------|-----------|---------|
| use case | use case | giữ nguyên |
| entity | entity | giữ nguyên |
| business rule | quy tắc nghiệp vụ (business rule) | |
| critical business rule | quy tắc nghiệp vụ cốt lõi | |
| critical business data | dữ liệu nghiệp vụ cốt lõi | |
| interactor | interactor | giữ nguyên |
| request/response model | mô hình request/response | |
| boundary | ranh giới (boundary) | |
| architectural boundary | ranh giới kiến trúc | |
| boundary crossing | vượt ranh giới (boundary crossing) | |
| partial boundary | ranh giới bán phần (partial boundary) | |
| humble object pattern | Humble Object pattern | giữ nguyên |
| presenter / view model | presenter / view model | giữ nguyên |
| policy / level | chính sách (policy) / cấp (level) | |
| high-level / low-level | mức cao / mức thấp | |
| decoupling | tách rời (decoupling) | |
| decoupling mode | chế độ tách rời | source/deployment/service level |
| independent developability | khả năng phát triển độc lập | |
| independent deployability | khả năng triển khai độc lập | |
| screaming architecture | kiến trúc biết "gào lên" (screaming architecture) | giữ ẩn dụ |
| the dependency rule | Quy tắc Phụ thuộc (the Dependency Rule) | |
| detail | chi tiết (detail) | "database là một chi tiết" |
| framework | framework | giữ nguyên |
| main component | component Main | |
| service | dịch vụ (service) | |
| micro-service | micro-service | giữ nguyên |
| cross-cutting concern | mối quan tâm xuyên suốt (cross-cutting concern) | |
| kitty problem | bài toán "mèo cưng" | ví dụ của tác giả |
| test boundary | ranh giới kiểm thử (test boundary) | |
| fragile test problem | vấn đề test dễ vỡ | |
| testing API | API dành cho kiểm thử | |
| embedded / firmware | nhúng (embedded) / firmware | |
| hardware abstraction layer (HAL) | tầng trừu tượng phần cứng (HAL) | giữ viết tắt |
| operating system abstraction layer (OSAL) | tầng trừu tượng hệ điều hành (OSAL) | |
| target-hardware bottleneck | nút thắt phần cứng đích | |
| package by layer / by feature | đóng gói theo tầng / theo tính năng | |
| ports and adapters | ports and adapters | giữ nguyên |
| package by component | đóng gói theo component | |
