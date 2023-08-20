# rgb-gradient

A Python package to create gradients.

## Installation

```shell
pip install rgb-gradient
```

## Usage

```python
from rgb_gradient import get_linear_gradient

intermediate_colors = [(255, 0, 0), '#c86496', (160, 150, 80), '#14f0b4', '#0000ff'] # colors format rgb or hex

gradient = get_linear_gradient(colors=intermediate_colors, nb_colors=10, return_format='hex')

print(gradient)
```

Output:

```
['#ff0000', '#dc4161', '#c86496', '#b1816e', '#a09650', '#65bc7a', '#14f0b4', '#13e7b7', '#0a74db', '#0000ff']
```

## Specification

| Parameters      | Type/Format                                                                                                                                                                                                                                                                                     |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `colors`        | A `list` containing:<br/>&emsp;• `tuples` (3 `int` elements from `0` to `255`)<br/>or/and<br/>&emsp;• `string` (representing the hexadecimal color value under the format `'#rrggbb'`<br/>&emsp;e.g. red = `'#ff0000'`).<br/><br/>Requirements: `len(colors) <= nb_colors and len(colors) >= 2` |
| `nb_colors`     | An `int` indicating how many colors will compose the gradient (including the colors already given).<br/><br/>Requirements: `nb_colors >= 3 and nb_colors >= len(colors)`                                                                                                                        |
| `return_format` | A `string` to indicate in which format the colors composing the gradient are returned.<br/>It can take the value `'rgb'` (decimal format) or `'hex'` (hexadecimal format).<br/><br/>Default value: `'rgb'`<br/>Requirements: `return_format == 'rgb' or return_format == 'hex'`                 |

## How it works

The RGB color model is composed of 3 values (red, green, blue) from 0 to 255. With that in mind, we can easily represent a color as a point on a 3D plan.\
With the input of the previous example, it looks like that:

![All input colors of the previous example placed as points on a 3D plan](https://raw.githubusercontent.com/Xeway/rgb-gradient/main/images/input_colors.png)

The `get_linear_gradient` function first determine the global distance from the first point to the last one, passing through the other colors given (if any).

> See on the image above, the global distance is all black lines added together.

With that distance, we can figure out how far from the starting point to place each missing point (simply place a point every `global_distance`/`(nb_points_to_add+1)`).

Here's the colors we got by calling the function `get_linear_gradient` with the arguments of the previous example:

![All output colors of the previous example placed as points on a 3D plan](https://raw.githubusercontent.com/Xeway/rgb-gradient/main/images/output_10_colors.png)

We can see a total of 10 colors, including 5 colors given and 5 new colors.

## Tips

Ok, that doesn't look like a real gradient for now. Let's call `get_linear_gradient` again with a total of 1000 colors (`nb_colors=1000`).

![1000 colors placed as points on a 3D plan, forming a real gradient](https://raw.githubusercontent.com/Xeway/rgb-gradient/main/images/output_1000_colors.png)

Yeah, this is better ;) Of course, the more you ask for colors, the better your gradient will be.

## Support

If you need help or found a bug, consider opening an issue on the project.

## License

The source code for this project is licensed under the GPLv3 license, which you can find in the [LICENSE](https://raw.githubusercontent.com/Xeway/rgb-gradient/main/LICENSE) file.
