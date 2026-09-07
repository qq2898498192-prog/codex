# Microduck 参考资料导航

来源：[atrl/microduck_rl](https://github.com/atrl/microduck_rl/tree/57280a07b06f7356500b796c8ddcda66008908d2)，固定提交 `57280a07b06f7356500b796c8ddcda66008908d2`。
整理日期：2026-09-07。官方上游：https://github.com/pollen-robotics/microduck_rl

## 已复制到本仓库
- [硬件总览与 BOM](upstream/docs/hardware/)：总表、打印件、采购件、参考件、装配接线、工作计划及调试说明。
- [结构资产说明](upstream/docs/robot_assets.md)：47 个机器人 STL 的分类与使用范围。
- [IMU 电路设计参考](upstream/docs/hardware/imu_to_dxl_v0_design.md)：已删去私人项目标识和历史订单信息，并注明删节。
- [IMU 协议固件及测试](upstream/firmware/imu_to_dxl_v0_2/)。
- [上游代码许可证](upstream/LICENSE)。

上述共 18 份参考文件；中文导航另计。部分上游文档的相对链接指向尚未复制的资产，可使用下面的固定版本入口查看。

## 尚未复制：来源入口
- [机器人 STL、MJCF 和 Onshape 导出配置](https://github.com/atrl/microduck_rl/tree/57280a07b06f7356500b796c8ddcda66008908d2/src/mjlab_microduck/robot/microduck)
- [IMU 原理图图片与制造资料所在目录](https://github.com/atrl/microduck_rl/tree/57280a07b06f7356500b796c8ddcda66008908d2/docs/hardware)
- [上游 README 与模型许可声明](https://github.com/atrl/microduck_rl/tree/57280a07b06f7356500b796c8ddcda66008908d2/README.md)

模型、图片、Gerber 和贴片文件尚未上传。当前插件文件接口仅支持 UTF-8 文本，普通 Git 推送缺少独立认证。自动导入工作流因涉及仓库写权限和自动提交被审批拒绝；制造说明也因包含被判定为私人项目的元数据被审批拒绝。本目录不表示这些文件已完整归档。

## 使用边界
- 不包含完整 RK3566、DDR、eMMC 主控板原理图与可编辑 PCB 工程。
- IMU 小板为独立传感器节点，不是主控板或整机电源板；上游可编辑立创工程未包含在公开文件内。
- STL 是简化仿真资产，制作前需核对原始 CAD、孔位、公差、材料与安装条件。
- 模型中的树莓派与 Robot HAT 为外形参考，不直接代表新 RK3566 主板尺寸。
- IMU 固件仍需 STM32 启动、DMA、中断与传感器采集集成。上游验证记录不等于本仓库独立实物验证。

## 许可与归属
保留来源与原作者归属。上游声明代码 Apache-2.0，3D 模型 Creative Commons BY-SA-NC，含非商业使用限制，具体许可版本以作者说明为准；不要把代码许可证套用于模型。除注明删节的 IMU 设计文档外，已复制文件保持原文。
