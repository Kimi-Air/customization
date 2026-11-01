# 碧瑶花园水电点位方案

基于平面图的交互式水电点位清单，使用 React、TypeScript 和 Ant Design。当前维护版本为 2D 页面，支持强电、弱电、控制、水路筛选，区域聚焦、点位详情、附件对照及 CSV 导出。

在线分享：https://kimi-air.github.io/customization/

点位详情包括设计原因、数量、安装位置、参考高度和待核定条件。图上坐标用于方案讨论；安装尺寸与设备接口需结合施工现场、柜体和最终机型复核。

## 运行

仓库包含已构建的页面，无需安装依赖即可预览（需要 Python 3）：

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory work/plan2d/dist
```

访问 http://localhost:8765/ 。也可以直接打开 `outputs/碧瑶花园-水电点位图-2D.html` 离线查看。

保留原有 `/2d/` 和 `/three.html` 地址的启动方式（macOS/Linux）：

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory work/home-site/dist
```

`work/home-site/dist/2d` 是指向当前 2D 构建目录的相对符号链接。早期 3D 页面仅作为历史参考，未同步后续全部点位调整；当前方案以 2D 页面为准。

## 修改与构建

需要 Node.js/npm 和 Python 3。Python 点位修订和导出脚本只使用标准库。

```sh
cd work/plan2d
npm ci
python3 review_points.py
npm run check
npm run build
python3 deliver.py
```

`review_points.py` 读取初始数据及各修订模块生成 `src/data.json`；不要直接修改生成文件。新增、删除和移动点位时，应同步维护 `point_specs.py` 中的数量、高度及核量口径，并遵守该目录的 `AGENTS.md`。

## GitHub Pages 发布

发布源为 `main` 分支的 `/docs`。`npm run build` 会同步当前 2D 静态资源到该目录。修改方案后运行上面的完整构建流程，将源码、构建产物及 `docs/` 一并提交并推送到 `main`，GitHub Pages 即会发布更新。分享地址保持不变。

发布内容仅为 2D 页面及其平面图、附件对照资源，不依赖本地服务器或登录。

## 目录

- `work/plan2d/`：当前 2D 应用、点位修订脚本、数据和构建资源。
- `work/home-site/`：早期 3D 方案源码及静态页面。
- `outputs/`：最新离线 2D 页面和点位 CSV 清单。

依赖、截图、原始视频及本地分析缓存不纳入版本控制。早期初始化和一次性迁移脚本为历史工具，日常修改使用上述构建流程。

## 全屋三维空间定位

在线地址：https://kimi-air.github.io/customization/model.html

2D 页顶栏的「3D 空间定位」进入新模型。支持全屋/房间筛选、旋转缩放、俯视、四面正视、墙体剖切及柜体家具透视；点位详情保留数量、安装高度、设计原因与待核条件。全屋默认隐藏编号以减少重叠，可开启编号或聚焦房间。

- `src/ModelApp.tsx`：三维界面，Ant Design 控件。
- `src/modelScene.ts`：Three.js 几何、相机、剖切与标注。
- `src/modelData.ts`：从当前2D数据生成三维标记；不读取已过期的早期3D点位。
- 厨房柜体以「厨房方案-V9-四视角渲染与正面剖面」为依据，参考「厨房水电深化-M1-平面与透视剖面」。厨房移门不建模，墙垛保留。
- 室内净高2700、厨房吊顶净高2400 mm仅为模型示意。未定标高以虚线编号表示；M1中650/450等值为协调建议，不替代安装图。
- K01保留冰箱背后。K04/K05/K06及W01/W02在三维中展示M1的柜内适配建议，2D仍保留原需求区域，详情明确区分。
- `npm run build` 同时构建2D与3D并同步Pages；`python3 deliver.py` 同时导出两个可相互跳转的离线HTML。
