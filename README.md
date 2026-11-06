# progressbar-static

![Progress](https://progress-bar.demolab.com/img/25.svg)
![Progress](https://progress-bar.demolab.com/img/50.svg)
![Progress](https://progress-bar.demolab.com/img/100.svg)


Static SVG progress bars for every whole percentage from **0% to 100%**, hosted on GitHub Pages.

These images are generated from the design in [guibranco/progressbar](https://github.com/guibranco/progressbar). That project also supported dynamic links (where the percentage was computed on request), but the dynamic service is down as of writing this. This repository pre-generates every value as a plain static file, so it doesn't rely on Vercel's usage limits.

## Usage

Each image is available at:

```
https://progress-bar.demolab.com/img/<percentage>.svg
```

where `<percentage>` is a number from `0` to `100`. For example:

| Percentage | URL                                          |
| ---------: | -------------------------------------------- |
|         1% | https://progress-bar.demolab.com/img/1.svg   |
|        50% | https://progress-bar.demolab.com/img/50.svg  |
|       100% | https://progress-bar.demolab.com/img/100.svg |

### Markdown

```markdown
![Progress](https://progress-bar.demolab.com/img/75.svg)
```

### HTML

```html
<img src="https://progress-bar.demolab.com/img/75.svg" alt="75%" />
```

## Colors

The fill color depends on the percentage:

| Range      | Color  | Hex       |
| ---------- | ------ | --------- |
| 1% – 29%   | Red    | `#d9534f` |
| 30% – 69%  | Orange | `#f0ad4e` |
| 70% – 100% | Green  | `#5cb85c` |

## Migrating from the dynamic service

If you were using a dynamic link from the original project, replace it with the static URL for the same percentage:

```
https://progress-bar.demolab.com/img/<percentage>.svg
```

Only whole percentages from 0 to 100 are available. Values with decimals are not supported.

## Regenerating the images

The SVGs are produced by `generate_svgs.py`:

```bash
python3 generate_svgs.py img
```

This writes `1.svg` through `100.svg` into the given directory (the current directory if none is given). The fill width is `percentage × 0.9` pixels on a 90 × 20 px bar.

## Credits

Based on the work of [guibranco/progressbar](https://github.com/guibranco/progressbar).
