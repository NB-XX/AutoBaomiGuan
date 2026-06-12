# 终端二维码登录与 2026 课程配置说明

## 背景

原项目只支持账号密码登录，并且课程入口仍混用了旧课程详情 ID。保密观当前流程支持通过 App 扫码登录，参考项目 `/Users/eyeseas/Documents/bmg-vue` 已验证二维码登录接口可用。本次改动将该能力移植到 Python CLI，并同步 2026 年课程包与考试 ID。

## 用户使用流程

运行 `main.py` 后，程序仍会优先检查本地 `credentials.json` 中保存的 token。

如果没有可用 token，程序会展示登录方式：

```text
1. 扫码登录
2. 账号密码登录
```

选择扫码登录后，终端会打印二维码。用户使用保密观 App 扫码并确认后，CLI 会拿到 `qrToken`，保存为本地登录 token，然后进入原有课程菜单。

账号密码登录路径仍保留，适合作为扫码失败或用户不方便扫码时的兜底方式。

## 二维码登录实现

二维码登录逻辑集中在 `login.py`：

- `get_qr_code()`
  - 请求 `https://www.baomi.org.cn/portal/main-api/v2/spc/getQrToken.do`
  - 从返回数据中取出二维码内容字符串。
  - 调用 `parse_qr_token()` 解析其中的 `params.qrToken`。

- `print_terminal_qr(qr_content)`
  - 使用 `qrcode` 依赖在终端输出二维码。
  - 不生成本地图片文件。

- `check_qr_login(qr_token)`
  - 请求 `https://www.baomi.org.cn/portal/api/v2/spc/checkQrToken.do`
  - 通过 `qrToken` 查询扫码状态。

- `qr_login(poll_interval=3)`
  - 显示二维码。
  - 每 3 秒轮询扫码状态。
  - 状态 `1` 表示扫码确认成功，返回当前 `qrToken`。
  - 状态 `-1` 表示二维码失效，自动刷新二维码。
  - 网络或状态接口异常会记录日志，并继续下一轮轮询。

新增依赖：

```text
qrcode>=7.4.0
```

## 凭证保存兼容性

扫码登录没有用户名和密码，因此 `main.py` 保存扫码凭证时使用：

```json
{
  "loginName": "扫码登录用户",
  "passWord": "",
  "token": "<qrToken>",
  "timestamp": 0
}
```

读取历史凭证时改用 `.get()`，避免旧文件或扫码凭证缺少字段时抛出异常。

## 2026 课程与考试配置

当前课程包 ID 统一配置在 `main.py`：

```python
CURRENT_COURSE_PACKET_ID = "312bc914-8e11-421b-b9bc-e900fe1a4e50"
```

课程目录、课程进度、自动学习、自动考试都会使用该课程包 ID。

当前考试 ID 统一配置在 `course.py`：

```python
DEFAULT_EXAM_ID = "8ad5bd4d9d483dde019e3e1066f60035"
```

`complete_exam()` 直接使用该考试 ID 获取试卷、提交答案和查询成绩，不再依赖 `getCourseRelateExam` 动态返回的考试 ID。

## 测试覆盖

新增 `unittest` 用例覆盖以下行为：

- 二维码 payload 能正确解析出 `qrToken`。
- 缺少 `qrToken` 的二维码 payload 会抛出明确异常。
- 获取二维码接口会返回二维码内容和 token。
- 扫码状态接口会解析嵌套状态码。
- `qr_login()` 在状态为 `1` 时返回 token。
- `qr_login()` 在状态为 `-1` 时刷新二维码。
- 主登录流程选择扫码登录时调用 `login.qr_login()`。
- 扫码登录凭证可保存空密码。
- `complete_exam()` 使用当前考试 ID。
- 课程菜单的自动考试入口使用当前课程包 ID。

验证命令：

```bash
python -m unittest discover -v
python -m py_compile login.py main.py course.py tests/__init__.py tests/test_login_qr.py tests/test_main_qr_login.py tests/test_course_exam_config.py tests/test_main_course_config.py
```

## 已知边界

- 本次改动不改变刷课和答题算法，只更新登录方式和 2026 年课程/考试配置。
- 二维码登录依赖保密观 App 扫码确认，无法在纯单元测试中端到端验证真实扫码。
- 若保密观后续变更二维码接口返回结构，需要同步更新 `parse_qr_token()` 和相关测试。
