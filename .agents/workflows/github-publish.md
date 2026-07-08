
---
description: Khởi tạo và đưa dự án lên GitHub ở chế độ công khai kèm theo logo, tài liệu README chuyên nghiệp
---
<!--
File: .agents/workflows/github-publish.md
Description: Workflow hướng dẫn quy chuẩn đưa dự án lên GitHub công khai (Logo, README, gitignore, CLI push).
CHANGELOG:
- 15:35:00 02/07/2026: [NEW] Khởi tạo workflow publish-github chuẩn hóa (Lê Thanh Vân/Antigravity)
-->

# Workflow Đưa Dự Án Lên GitHub (GitHub Publish & Branding Workflow)

Workflow này chuẩn hóa quy trình khởi tạo Git, xây dựng thương hiệu (Logo, Name, README) và đẩy mã nguồn sạch của dự án lên GitHub bằng dòng lệnh CLI.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_GITHUB_PUBLISH",
    "workflow_name": "Publish Project to GitHub",
    "workflow_goal": "Initialize Git, setup strict gitignore, design logo & README, and push to GitHub using CLI.",
    "expected_inputs": [
      {"name": "repo_name", "type": "string", "description": "Tên repository trên GitHub (Ví dụ: MarkDocx)"},
      {"name": "app_description", "type": "string", "description": "Mô tả ngắn gọn về ứng dụng"},
      {"name": "is_public", "type": "boolean", "description": "Chế độ công khai (True) hoặc Riêng tư (False)"}
    ],
    "constraints": [
      "Strict Ignore: Bắt buộc loại trừ các thư mục nhạy cảm (.env, .gemini, docs, scripts, caches) khỏi Git.",
      "Branding First: Đề xuất tên ứng dụng hay và tạo logo chuyên nghiệp trước khi push.",
      "CLI First: Sử dụng GitHub CLI (gh) để tạo repo và push, không dùng trình duyệt tự động.",
      "Readme Standards: README.md phải có logo, badges động, sơ đồ Mermaid và kiến trúc module."
    ],
    "entry_scene_id": "S_GIT_INIT"
  },
  "scenes": [
    {
      "scene_id": "S_GIT_INIT",
      "scene_type": "ACT",
      "scene_goal": "Khởi tạo Git repository và cấu hình file .gitignore nghiêm ngặt.",
      "next_scene_rules": [{"condition": "success", "target": "S_BRANDING_DESIGN"}]
    },
    {
      "scene_id": "S_BRANDING_DESIGN",
      "scene_type": "ACQUIRE",
      "scene_goal": "Thiết kế logo qua generate_image, chọn tên và soạn README.md tiêu chuẩn.",
      "next_scene_rules": [{"condition": "success", "target": "S_COMMIT_LOCAL"}]
    },
    {
      "scene_id": "S_COMMIT_LOCAL",
      "scene_type": "ACT",
      "scene_goal": "Lưu nhật ký phát triển cục bộ và thực hiện Initial Commit trong Git.",
      "next_scene_rules": [{"condition": "success", "target": "S_GITHUB_PUSH"}]
    },
    {
      "scene_id": "S_GITHUB_PUSH",
      "scene_type": "ACT",
      "scene_goal": "Tạo repository trên GitHub bằng GitHub CLI (gh) và đẩy mã nguồn lên.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE_REPORT"}]
    },
    {
      "scene_id": "S_FINALIZE_REPORT",
      "scene_type": "FINALIZE",
      "scene_goal": "Kiểm tra liên kết hoạt động và hiển thị URL repository cho người dùng.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 📁 Scene 1: GIT_INIT (Khởi tạo Git & Cấu hình Bỏ qua)

- [ ] Chạy lệnh `git init` để khởi tạo repository cục bộ.
- [ ] Tạo file `.gitignore` ở thư mục gốc của dự án. File này bắt buộc phải loại trừ:
  - Cache: `__pycache__/`, `*.pyc`
  - Biến môi trường: `.env`
  - Thư mục làm việc của Agent/IDE: `.gemini/`, `.agents/`, `scratch/`
  - Thư mục tài liệu & script nội bộ: `docs/`, `scripts/` (nếu dự án yêu cầu giữ private)
  - Thư mục kết quả render tạm: `temp_render/`, `_mermaid_temp/`

### 🎨 Scene 2: BRANDING_DESIGN (Thương hiệu & Soạn thảo README)

- [ ] **Gợi ý tên ứng dụng**: Đề xuất 2-3 cái tên ngắn gọn, dễ nhớ, liên quan đến nghiệp vụ (ví dụ: *MarkDocx* cho trình xem/xuất Word).
- [ ] **Tạo Logo**: Sử dụng công cụ `generate_image` để tạo logo ứng dụng chuyên nghiệp. Copy logo đã sinh về thư mục gốc làm `logo.png`.
- [ ] **Viết README.md**: Soạn thảo file `README.md` bao gồm:
  - Header chứa logo căn giữa và các badges động (Python version, UI framework, license, v.v.).
  - Phần giới thiệu làm rõ **các điểm độc đáo vượt trội** của sản phẩm so với các công cụ trên thị trường.
  - Sơ đồ Mermaid mô tả kiến trúc module hệ thống.
  - Hướng dẫn cài đặt và sử dụng nhanh.

### 💾 Scene 3: COMMIT_LOCAL (Lưu Nhật ký & Commit cục bộ)

- [ ] Chạy kiểm toán ruff linter (`ruff check .`) để đảm bảo code sạch.
- [ ] Ghi lại nhật ký công việc ngày hôm nay vào `docs/work_logs/` hoặc chạy script `update_work_log.py` (nếu có).
- [ ] Thêm tất cả file codebase vào staging: `git add .` (do đã có `.gitignore` chặn file rác).
- [ ] Thực hiện commit đầu tiên: `git commit -m "initial commit: import codebase, logos, and readme documentation"`.

### 🚀 Scene 4: GITHUB_PUSH (Tạo repo & Đẩy lên GitHub)

- [ ] Kiểm tra trạng thái đăng nhập của GitHub CLI: `gh auth status`
- [ ] Nếu chưa đăng nhập, hướng dẫn người dùng chạy lệnh `gh auth login`.
- [ ] Tạo và đẩy repository lên GitHub bằng một lệnh duy nhất:

  ```bash
  gh repo create <repo_name> --public --source=. --remote=origin --push
  ```

  *(Thay thế `--public` bằng `--private` nếu người dùng muốn để chế độ riêng tư)*.

### 🏁 Scene 5: FINALIZE (Kiểm chứng & Báo cáo)

- [ ] Xác nhận lệnh push thành công.
- [ ] Trích xuất commit hash mới nhất bằng `git log -n 1`.
- [ ] Trả về đường link URL chính thức của repository trên GitHub để Anh Lưu click kiểm tra trực tiếp.
