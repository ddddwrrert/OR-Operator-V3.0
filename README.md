# OR-Operator V3.0

## Python 框架

本目录自带完整 Python 源码、YAML 配置、安装入口和测试。Python 3.11+。建议每个版本使用自己的虚拟环境。

```powershell
python -m pip install -r requirements.txt
python -B run.py --work python-demo
python -B -m unittest discover -s tests -t .
```

可使用 `python -m pip install .` 安装对应版本的命令，或直接运行 `main.py` / `run.py`。添加 `--config config-overrides.yaml` 覆盖配置。相同配置和任务可在同一工作目录读取状态和预算。候选、接受和拒绝源码在工作目录的 `storage/`，逐项实验与最终记忆在 `reports/`，分阶段事件在 `logs/`。

默认数据来自可重复的数值 Solver。尝试包括生成可执行 Python 代码、语法检查、真实求解进程、配对评分和接受或回滚决策。原版接入有两条路径：

- DSH 内注册 JavaScript 插件。保留原版循环，用原版 worker 和 evaluator。
- Python 独立 runner 使用 `--organon <原版路径> --task <任务路径> --config <覆盖配置>`。设置 `OR_OPERATOR_LLM_URL`（完整兼容请求地址）、模型名与可选密钥。该入口在工作目录复制 task 和原版 evaluator。设置 `solver.sandbox_prefix` 为部署环境提供的隔离启动参数。如果任务确实从环境变量接受种子，配置 `solver.organon_seed_env`；否则报告单次匹配评分。原版任务夹具、C++ 编译和本地配对已经验证。

V2 层支持 UCB 和 Thompson 两种实际调度策略、2 到 3 步组合、同父代组件和顺序消融，并输出协同图。调度报告的策略回放只比较决策。将 `scheduler.algorithm` 分别设为 `UCB` 和 `Thompson` 并使用独立工作目录，可执行两次真实对照。

V3 层在固定数值任务上对策略做配对评估，隔离运行使用有界数据策略、独立工作目录、独立 Solver 与保留种子。外部 Organon 任务没有绑定固定验证套件时跳过 Python 策略晋升。


本目录包含自己的源码、入口和测试。进入目录后运行 npm test。移到其他位置时，可将 ORGANON_ROOT 设为原版 Organon 的绝对路径，以运行集成测试。

## Offline standalone run

```powershell
npm start -- --work demo-run
npm run test:offline
```

The output directory must be new. The bundled demo uses only Node.js, executes an evolving numerical solver and evaluates it on distinct paired instances. It writes source candidates, scores, population and operator memory under the output directory. The demo backend is deterministic. Use the Organon adapter and its workers for unrestricted model-based discovery. Override demo defaults with --config path-to-json. Run npm test to include the Organon integration suite.

Accepted demo combinations are evaluated on the same parent using an untreated control, each component alone and both orders. A dedicated evaluation cap limits these ablations. Production tasks can supply the inspectComposition callback with task-specific rebuilding and evaluation.

A successor mechanism can propose evidence selection and discovery instructions, a seed count, a sequence length and whether to try compositions. Operator validation and run budgets remain under the original hard caps. Promotion currently uses same-phase search trials.

## 运行测试

在 PowerShell 中运行：

```powershell
Set-Location -LiteralPath 'D:\RSI\OR-Operator\V3.0'
npm test
```

需要 Node.js 22+、Python 和OR-Operator 同级目录中的 Organon（原）。也可以用环境变量 ORGANON_ROOT 指向另一份原版源码。测试复制原版任务夹具到临时目录，通过原版 Evolve 服务、候选分配、循环、Python 评估脚本及种群文件执行三个版本。测试替身为 worker 和本地进程接口。

## 加载到 Organon

先使用原版文档建立 DSH Evolve Mode。把 OR-Operator 放在可加载的宿主路径，在独立的 DSH 配置层为已有 evolve 服务插入一个插件。例中模块路径相对于配置文件，按部署目录调整：

```yaml
- insert:
    - id: or-operator
      name: ./OR-Operator/V3.0/index.js
```

也可以由宿主插件导入任一版本的 createPlugin(options)，在具备 ctx.evolve 的上下文中调用 apply(ctx)。同一服务只装一个 OR-Operator 版本。注册后仍调用原版 evolve_run。保持原版循环入口的参数和响应格式；插件包装原版循环并复用原版 select、evaluate、survive 和常规 mutate。动态切换 loop 时，OR-Operator 需要作为当前 loop 提供者。卸载插件会把调用交回原先的 loop，已有种群和日志仍可继续使用。

### 配置接口

| 参数 | 默认 | 作用 |
| --- | --- | --- |
| stagnation | 3 | 全局最优连续未改进多少候选才触发算子探索 |
| window | 8 | 诊断读取的最近记录数 |
| fraction | 0.3 | 某一版本可使用的全局候选预算比例，向下取整 |
| maxAttempts | 12 | 某一版本的探索候选绝对上限 |
| minimumConfidence | 0.6 | M2 报告的最低置信度 |
| maxPairs | 24 | 某一版本可运行的额外配对次数，每对最多调用评估适配器两次 |
| seeds | [11, 29, 47] | 开启 trial 后使用的独立 seed，每对共享用于控制和处理 |
| trial | 未配置 | 异步函数 (candidate, seed, signal) → number，返回与原版相同方向和零值约定的 fitness |

一次探索分配一个候选槽，至多启动两次 worker。常规变异使用剩余候选额度。配对额度在调用适配器前写入日志，跨 evolve_run 调用累计。适配器负责真实的 seed 注入、任务隔离、超时和取消。默认官方 evaluator 接口未承诺可配置 seed，因此默认使用同一任务下的新候选官方分数与父代历史分数归因。启用 trial 后，首对筛选要求正收益，最终要求平均收益为正且多数配对改善。

日志写在任务的 run/or-operator/v版本.json。每条记录包括候选与父代 ID、画像、证据、假设、计划、分数、阶段、耗时及配对结果。拒绝的候选保留工件和原始评估，种群以 fitness=0、survival=no 记录。中断后的已分配额度继续遵循原版候选计数，未完成试验可从日志辨识。

### 当前验证边界

静态画像使用轻量源码扫描。运行数据来自原版可取得的候选谱系和评估指标，逐算子执行时序需由任务提供可读指标。贡献是相对同一父代的整次修改效果，组合内各组件的独立边际效应需要专门消融。M6 比较的是有限预算下的同阶段通过率，结论会受父代和实例差异影响。实际 DSH 部署、真实模型调用及 AHC 基准尚未验证。

