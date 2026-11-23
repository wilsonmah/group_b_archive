# Wilson's Group B Archive

An archive of Group B rally cars (1982–1986) as exploded 3D studies. Each car's body and livery are calibrated line by line against period photographs, and its engine, gearbox and suspension are rebuilt so you can take them apart, turn them over and run them in the browser.

[Open the archive](https://wilsonmah.github.io/group_b_archive/)

## Catalogue

| # | Car | Contents | View |
|---|---|---|---|
| 01 | Lancia Rally 037 · Martini Racing Nº 5 | Full teardown, engine, transaxle, suspension and steering, motion study | [3D viewer](https://wilsonmah.github.io/group_b_archive/cars/lancia-037/) · [Notes](cars/lancia-037/README.md) |
| 02 | Audi Sport quattro S1 E2 · HB Audi Team Nº 2 | Full teardown, turbocharged inline-five, quattro drivetrain, MacPherson suspension, rear-mounted cooling, motion study | [3D viewer](https://wilsonmah.github.io/group_b_archive/cars/audi-quattro-s1/) · [Notes](cars/audi-quattro-s1/README.md) |
| 03 | Lancia Delta S4 · Martini Racing Nº 1 | Full teardown, twin-charged inline-four, spaceframe, 4WD drivetrain, double-wishbone suspension, motion study | [3D viewer](https://wilsonmah.github.io/group_b_archive/cars/lancia-delta-s4/) · [Notes](cars/lancia-delta-s4/README.md) |

More Group B cars are on the way.

## Viewer controls

- **Drag:** orbit.
- **Scroll or pinch:** zoom towards the point under the cursor or between your fingers. You can zoom in far enough to inspect individual parts.
- **Double-click any point on the model:** that point glides to the centre and becomes the orbit centre, zooming in. Double-click empty space to reset.
- **Right-drag, Shift-drag or two-finger drag:** pan.
- **Click a part:** select it. The home, side and top buttons reset the view.

## Layout

```
index.html              Homepage (catalogue)
assets/covers/          Homepage cover and card images
cars/<slug>/            One self-contained folder per car
  index.html            Offline 3D viewer with the model embedded
  models/               Exported GLB models
  images/               Images used in the car's notes
  src/                  Generator scripts and viewer source
```

Every page opens straight from disk in a browser; no server is needed.

## Adding a car

1. Create `cars/<slug>/` with the car's viewer and models (use any existing car folder as a template).
2. Append an entry to the `CARS` list in the homepage `index.html`: link, card image, name, year, part count and three specs.
3. To change the cover, put the photo in `assets/covers/` and update the image path at the top of the homepage.

The site interface is bilingual (Chinese and English); switch languages from the header or with `?lang=en` / `?lang=zh`.
