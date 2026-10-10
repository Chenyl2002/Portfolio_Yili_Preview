# 陈宜理 · 中文作品集独立预览

基于 Bruno Simon 作品改编的可驾驶中文作品集。保留可见作者署名、MIT、中文字体 OFL 及第三方许可证。原作品集与原域名保持独立。

## 当前内容

- 四个作品各有一块现场 3D 木展板，共 20 页项目资料。每页打开对应项目原始 PDF 或 DOCX，保留原图与作品来源，明确草稿、模拟与尚未完成部分；全站简历另有入口。
- 地图日夜底图按当前静态场景对齐。白菱形代表安全停车点，文字独立偏移；建筑与关卡方向的两组真实经历拥有独立入口，原经历台保留。
- 默认车辆更换为矿车，保留六种皮肤、轮胎、灯光、boost、悬挂等绑定与驾驶流程。
- 展板观看时局部减轻草和车辆视觉遮挡；退出恢复。车辆处理只影响视觉根，不修改驾驶物理、碰撞、相机或停车位置。
- 转场遮罩在长帧间隔下继续按墙钟推进，保留原色彩、图案和渐变。原输入取消、点击边沿与展板着色修复继续保留。
- 界面、导航和场景说明以中文为主，中文字体覆盖 1,323 个字码。项目原名、作者、技术名和原版权文字保留。

破碎之家主展板位于原庭院黑色小牌的位置，正面对入口；原小牌的三处实体、三处碰撞和标签已撤下。保留原安全停车入口，并有近牌入口；两处入口打开同一块主板，板框、碰撞体、分页命中和观看镜头使用同一位置。其他三块展板保持原处，没有新建铺地或改变草mask。靠近按 Enter、触控交互或手柄 A/× 打开，选择“近看资料”继续靠近；Esc、返回驾驶或相应手柄操作退出。PDF、视频、高清图仅在点击资料入口后打开。

地面草的着色表达式已补充显式共享变量，修复局部遮挡分支未启用时可能读取未赋值临时量的问题。草的生成、密度、位置、风动和原美术参数不变；WGSL/GLSL代码生成回归检查通过，实际设备画面仍需单独核实。

两处通用节点改为工业风“机关试验场”和“迭代影像终端”，原触发玩法、碰撞、屏幕UV、计数和成就保留。对应名称、说明与日夜地图一起更新；本次移除旧小牌后已重新导出并重烘地图。地图增强了可见标签与目标的对应和命中可靠性，安全停靠点与原坐标不变。地图不绘制程序草blades、主展板、车辆、天气、动态屏幕或粒子。

## 技术预览限制

新增模型和场景用于作品展示，不是从原游戏工程直接导出的可玩关卡，也不表示未完成系统或现实改善成果已经实现。道路及其他部分内容仍保留通用素材。未连接多人服务或分析追踪，声音默认关闭。

本版本通过 19 项本地源码、CPU 几何及生产构建命令，并验证两节点保护合同、新主牌位置与正面、低框覆盖、地图来源和生产产物变更范围。涵盖真实矿车 GLB/Draco 解码与轮胎极端姿态净空、双车型展板遮挡、遮罩墙钟、项目原稿链接、地图空间与中文字体。板脚和前方约0.7米范围的既有硬地通过采样，1米处仍可能遇到原草边界。阅读时的草遮挡保护经过32种拟合姿态检查，不承诺任意驾驶视角或前方大片区域无草。离线几何、示意图和方法夹具不等于GPU、真实驾驶、触屏、手柄或移动端性能验收，也不能证明特定设备的误点已经修复。

历史地图审查仍有一项 P3 边界：全局关闭回调内同步重开经历面板可能丢失新面板输入归属，当前 UI 没有使用该订阅方式。静态相对 URL、依赖 eval 和大 chunk 构建提示仍保留。设备端画面、素材读取、帧率和资料可读性仍需验证；高清原图可用于补充阅读。资料运行贴图为 960×540，离线 2K 校样不能证明手机清晰度。

## 离线还原公开网站

九个 preview.zip.partNN 分卷与 manifest.json 保留提交 93b16facda9ed4abc903ba749b4e88e4f8ab7afd 的原始基底。preview-delta.zip.partNN 为每卷不超过 8 MiB 的增量。release-manifest.json 记录顺序、大小、SHA-256、精确删除清单及最终文件校验。

在没有 dist 目录的干净仓库副本中运行：

```sh
python3 extract_preview.py
```

无需安装依赖或联网。提取器先验证路径、类型、分卷和合并压缩包、增删集合、许可证及全部最终文件，再生成 dist；拒绝覆盖已有 dist。保留的 GitHub Actions 工作流发布验证后的静态网站，也可用静态服务器在本地打开。

公开发布包仅含构建资源、许可证及还原工具，不含开发源码、私有配置、凭据或自定义域名设置。

## Personal portfolio guidance update

The constant technical-preview banner has been removed. Home, map, and fallback copy now introduce Chen Yili's level/gameplay design focus and the four projects. Credits and licenses remain available under the existing credits section. Only HTML and its primary stylesheet changed; gameplay JavaScript, models, coordinates, environment and licenses are unchanged.

This release uses a reproducible Vite HTML/CSS-only incremental build. The same pipeline reproduces the previously deployed baseline HTML/CSS byte-for-byte before building changed inputs; unchanged runtime outputs are reused exactly. The attempted full build was memory-limited (exit 137), not passed. No browser, device or GPU acceptance is claimed.

## Optional project design views

Adds optional design details inside the Ancient Temple, Moston, and Broken Home project boards. Original project documents remain the evidence source; interactive mechanism explanations are illustrative and do not claim to reproduce the original games. Navigation, placements, grass fix, project/experience separation and licenses are retained. This candidate passed its full production build and static/focused checks. Device acceptance is recorded separately before publication.

## Project source links and board initialization

Source links now open the intended project document pages (2 and 9), and board media initializes only once. Full production build and focused interaction/geometry/projection/placement checks passed. Existing font-coverage and grass source-regex test failures were reproduced on the prior baseline and are not represented as passing. No device/browser acceptance is claimed.

## Font coverage and lossless project images

The consolidated cloud update also adds 14 missing Chinese glyphs while preserving all prior glyph outlines/metrics, and uses pixel-equivalent lossless WebP for two design-view images. Original PNGs and font license remain included. The final candidate passed all 16 offline suites and full production build. Offline checks do not constitute browser/device acceptance; no user computer was used.

## Ancient Temple static composition

The temple diorama now includes a source-backed static sword, three seal markers and upper window composition. These 18 non-solid decorative parts illustrate the document's three-seal mechanism; they are not an interactive reconstruction. Focused geometry, composition and full production build checks passed. Visibility varies with camera position: the parking framing crops the top window and the whole-board framing places much of the sword outside the frame. No device/browser acceptance is claimed.

## In-site resource reader and recovery update

Resources open inside the portfolio, including a lazy-loaded 84-page PDF preview reader, source text, explicit unavailable-video panels, and contact copying. Career begins at 2023 and lists the owner-confirmed ByteDance internship first. Loader recovery and the bounded sword-clearance correction are included. Original source files and licenses are retained. Offline aggregates and production build passed; browser/device focus, touch, history and rendered layout acceptance remain unverified. The selected light timeline and project-board visual treatments are integrated in the production candidate. Browser-rendered fidelity acceptance remains incomplete.

## Fourteen reference-style boards

All fourteen added scene boards now use the selected magenta panel, dark-purple supports and block-button visual language. The light career timeline and in-site resource functionality are retained; static assets and configuration are unchanged. Production build, board/geometry/crop checks and source-texture completeness passed. Blender text rendering remains incomplete and is not accepted as visual proof; browser-rendered 3D acceptance has not been performed. No user computer was used.

## Source-backed world details and achievements

Adds 24 event-backed achievements and bounded decorative details (+1,872 triangles, one draw, no new materials or colliders). Render-only Broken Home coplanarity and a shared normal-space alias were corrected while preserving collision and input behavior. Main aggregates and build passed. The extra historical map provenance check still fails on an unchanged career-data hash and reproduces on the prior published baseline. Actual device material appearance remains unaccepted; no reproduced flicker or flicker cure is claimed. Static files and existing licenses remain unchanged.

## Terminal arrival and explicit career reading

Moves the terminal landing to a verified dry point and associates its prompt with that arrival. Career records now have an explicit marked-read control. Bounded production-method and build checks passed; the inherited final map source-provenance hash exception remains disclosed. Cloud deployment and byte verification do not establish live browser or device acceptance.

## Board surface and readability repair

Increases the twenty-page board texture resolution with bounded lifecycle handling, adjusts local text sampling and the E2 internship label, removes overlapping paving surfaces while linking coverage to actual floor visibility, and relocates one Ancient Temple bench. Nine offline check groups and production build passed. Actual GPU readability and driving still require separate acceptance; the historical aligned-map provenance exception remains disclosed.

## Reference UI and TV camera integration

Integrates the selected panel and reference-style control treatments, fitted board framing, in-site resource zoom, refined project geometry and 81-glyph board-control font coverage. The frozen production build contains 1,189 files. Independent source and distribution manifest verification passed. Offline production-method checks and full build are separate from actual browser/device visual acceptance, which remains incomplete. The current day/night map was regenerated against the final layout: the new provenance proof covers 82 sources, 27 projected points, 261 checks and 19 actual Map-chain checks. Historical map proofs remain preserved as historical records. Only this independent preview repository is published; the original portfolio repository and custom domain are unchanged.
