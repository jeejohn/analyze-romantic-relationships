# 案例数据规范

## 目录

1. 使用边界
2. 最小结构
3. 字段规则
4. 发布门槛
5. 校验方法

## 1. 使用边界

结构化案例用于复现分析、回归测试和在获得授权后积累案例库。它不能提高材料本身的真实性，也不能把单方报告变成已证实事实。

普通用户不必先填写 JSON。只在用户提供结构化文件、要求建立案例库、提交公开案例或执行回归测试时使用本规范。

严禁把姓名、电话、邮箱、账号、住址、单位、证件、未成年人身份或可反向识别当事人的独特细节提交到公开仓库。真实材料只有“允许分析”而没有“允许公开”时，不得进入公开案例库。

## 2. 最小结构

```json
{
  "schema_version": "1.0",
  "case_id": "synthetic-conflict-001",
  "title": "忙碌与陪伴冲突的合成案例",
  "source": {
    "type": "synthetic",
    "deidentified": true
  },
  "consent": {
    "allow_analysis": true,
    "allow_publication": true
  },
  "relationship": {
    "stage": "dating",
    "participants": [
      {"id": "A", "role": "partner"},
      {"id": "B", "role": "partner"}
    ],
    "agreements": ["每周至少一次固定约会"]
  },
  "events": [
    {
      "id": "E1",
      "time": "2026-01",
      "source_type": "self-report",
      "reporter": "A",
      "summary": "A 报告双方连续三周取消固定约会。",
      "observable_actions": [
        {"actor": "B", "action": "三次在约会前取消安排"},
        {"actor": "A", "action": "提出改为每周一次视频通话"}
      ]
    }
  ],
  "questions": ["现有材料是否支持稳定失约模式？"],
  "risk_flags": []
}
```

## 3. 字段规则

| 字段 | 规则 |
|---|---|
| `schema_version` | 当前固定为 `1.0`。 |
| `case_id` | 使用不含身份信息的稳定标识，只含字母、数字、点、下划线或连字符。 |
| `source.type` | 只用 `synthetic`、`user-submitted-anonymized` 或 `public-with-permission`。 |
| `source.deidentified` | 进入共享或公开流程前必须为 `true`。 |
| `consent.allow_analysis` | 必须明确为 `true` 才能进行案例库分析。 |
| `consent.allow_publication` | 只有明确为 `true` 才能公开；不得从分析授权推定。 |
| `participants` | 使用 `A`、`B` 等代号。不得存储姓名、账号或可识别标签。 |
| `agreements` | 只记录材料明确覆盖的关系约定；未知时使用空数组。 |
| `events` | 按事件而非消息条数切分。每个事件保留来源与报告者。 |
| `observable_actions` | 只写可观察言行；推测的动机放在分析输出，不写成原始事实。 |
| `risk_flags` | 可用 `violence`、`sexual-coercion`、`stalking`、`threats`、`coercive-control`、`self-harm`、`harm-to-others`。 |
| `safety_context` | 出现任一风险标记时必填，记录报告来源、是否迫近及现实支持情况；不得包含身份信息。 |

事件来源 `source_type` 只用：`chat`、`screenshot`、`self-report`、`behavior-record`、`third-party`。

## 4. 发布门槛

公开提交必须同时满足：

1. `source.deidentified` 为 `true`；
2. `consent.allow_analysis` 为 `true`；
3. `consent.allow_publication` 为 `true`；
4. 自动隐私扫描没有未解决警告；
5. 人工检查无法凭细节合理识别当事人；
6. 未包含原始私密截图、联系方式、定位信息或未成年人身份；
7. 风险案例不会因公开而增加报复、跟踪或二次伤害风险。

不满足时只能保留在私有环境，或改写为不对应特定个人的合成案例。

## 5. 校验方法

对单个案例运行：

```bash
python3 scripts/validate_case.py path/to/case.json
```

公开提交使用严格模式；警告也会导致失败：

```bash
python3 scripts/validate_case.py --strict path/to/case.json
```

校验只检查结构、授权字段、明显隐私模式和内部一致性，不验证叙述真实性、法律授权效力或关系结论是否正确。分析仍按《分析协议》执行。

