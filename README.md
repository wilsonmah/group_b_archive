# Wilson's Group B Archive

B 组拉力赛车（1982–1986）的可拆解 3D 档案。每台车按实车照片逐线校准车身与涂装，并重建发动机、变速箱和悬挂，可在浏览器里拆开、旋转和运转。

An archive of Group B rally cars as exploded 3D studies, calibrated against period photographs.

[打开主页 / Open the archive](https://wilsonmah.github.io/group_b_archive/)

## 车型目录

| # | 车型 | 内容 | 查看 |
|---|---|---|---|
| 01 | Lancia Rally 037 · Martini Racing 5 号 | 整车拆解、发动机、变速箱、悬挂与转向、运转演示 | [3D 查看器](https://wilsonmah.github.io/group_b_archive/cars/lancia-037/) · [说明](cars/lancia-037/README.md) |

更多 B 组赛车陆续加入。

## 目录结构

```
index.html              主页（车型目录）
assets/covers/          主页封面图
cars/<车型>/            每台车一个独立目录
  index.html            内嵌模型的离线 3D 查看器
  models/               导出的 GLB 模型
  images/               说明配图
  src/                  生成脚本与查看器源码
```

所有页面都可以直接用浏览器离线打开，不需要服务器。

## 加入新车

1. 新建 `cars/<车型>/`，放入该车的查看器和模型（可参照 `cars/lancia-037/`）。
2. 在主页 `index.html` 的 `CARS` 列表末尾加一条记录：链接、卡片图、名称、年份和三项规格。
3. 需要换封面时，把照片放进 `assets/covers/` 并改主页顶部的图片路径。
