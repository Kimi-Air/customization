# 碧瑶花园水电点位方案

基于平面图的交互式水电点位清单，使用 React、TypeScript 和 Ant Design。当前维护版本为 2D 页面，支持强电、弱电、控制、水路筛选，区域聚焦、点位详情、附件对照及 CSV 导出。

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

## 目录

- `work/plan2d/`：当前 2D 应用、点位修订脚本、数据和构建资源。
- `work/home-site/`：早期 3D 方案源码及静态页面。
- `outputs/`：最新离线 2D 页面和点位 CSV 清单。

依赖、截图、原始视频及本地分析缓存不纳入版本控制。早期初始化和一次性迁移脚本为历史工具，日常修改使用上述构建流程。
