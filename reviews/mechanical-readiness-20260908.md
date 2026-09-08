# 结构打样资料检查（2026-09-08）

检查对象：本仓库 microduck_rl/。47 个机器人 STL 的 Git blob SHA 与远端文件逐一一致。另有 11 个 XL330 测试台 STL，不计入机器人零件数。

## 结论
有可供试打印及装配评估的模型，尚不能认定为制造定版。未发现 STEP/STP、3MF、SolidWorks、FreeCAD 或 DXF 工程文件。.part 文件实际是 Onshape 零件标识 JSON，不是实体 CAD。

## 分类
- 刚性打印候选：30 种。
- 柔性打印候选：5 种。
- 采购件外形参考：8 种（舵机、轴承、电子板、电池等，不可作为其功能替代件打印）。
- 当前装配未引用的旧模型：4 种。
- 行走版实际使用：26 种刚性件，共32件；4种柔性件，共4件，合计36件。
- 数量和分类来自 asset_manifest.csv，不代表材料和切片工艺已经验证。

## 网格检查
解析了全部47个二进制STL，核对三角形数与字节长度。按完全相同坐标合并顶点后统计无向边：全部模型均未检出仅使用一次的边或使用超过两次的边。
这只检查边连接情况，未验证自相交、重复面、壁厚、法线一致性、配合公差和结构强度，不能等同于打印合格报告。

## 单位风险
STL 本身不声明单位。抽查原始坐标：neck 为0.002×0.020×0.011；top_head_shell 为0.091759×0.122690×0.046336。结合仿真尺寸判断这些数值采用米；转换为毫米应为2×20×11 mm、约91.759×122.690×46.336 mm。切片软件若直接按毫米解释原坐标，会小1000倍；若软件已自动换算，不要再次缩放。先核对尺寸再打印。

## 资料入口
- [模型目录](../microduck_rl/src/mjlab_microduck/robot/microduck/assets/)
- [分类清单](../microduck_rl/src/mjlab_microduck/robot/microduck/asset_manifest.csv)
- [打印BOM](../microduck_rl/docs/hardware/print_bom.csv)
- [装配说明](../microduck_rl/docs/hardware/assembly_and_wiring.md)
- [Onshape导出配置](../microduck_rl/src/mjlab_microduck/robot/microduck/config_mjcf_allcollisions.json)

## 打样前未完成事项
原始配置明确 simplify_stls=true。应核实Onshape源版本并导出非简化几何；先做舵机安装位、轴承孔和紧固件配合试件，再确认整机材料、打印方向和承载。仓库没有完成上述验证的证据，不能保证一次打印即可装配行走。Onshape链接存在不代表已核实当前访问权限。
