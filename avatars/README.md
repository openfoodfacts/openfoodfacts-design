# Avatars

This directory contains SVG avatar designs for use in the Open Food Facts project.

The avatars can be used in marketing materials (e.g. to create illustrations for social media), and in the future, we could also offer Open Food Facts to create avatars for themselves
that could be used in their profiles (similarly to popular apps like Duolingo).

## Avatars structure

Avatars are composed of several body parts (e.g. hair, body, top clothes, bottom clothes, shoes etc.) that are stacked on each other.
For each part, it's possible to choose between different types (e.g. short hair, long hair).
Some parts / types combinations will also allow users to choose a color (e.g. tshirt color).

## Avatars SVG files

### Software

Please use Inkscape to create or edit the SVG files, as other software (e.g. Adobe Illustrator) use different features of SVG files to set colors,
which will not work with our avatars creation code that combines multiple SVG files into one.

### Naming: [part].[type].[component].svg

* part: the body part (e.g. hair, body, top-clothes, bottom-clothes)
* type: a type for the body part that users will be able to choose (e.g. "tshirt" and "sweatshirt" for the "top-clothes" part).
* component: some parts require different layers that must be displayed in a specific order. For instance hair can have a bottom layer under the face, and a top layer on top of the face. We can define different components (like "top" or "bottom") for some parts.

### Size and component placements

All SVG files must be 250x300px.

We use full width and height files for all components to place all components.
For instance, a shoes component will be placed at the center bottom of the image.

### Colors

For parts where users can choose colors (e.g. hair color, clothes color), all types of the same type must use the same colors. e.g. all types of hair must use the same 2 bottom and top hair colors.

Colors need to be applied directly on the SVG elements (using the fill: and stroke: attributes, or the style attribute).
They must not be applied indirectly through a class, as we will combine SVG elements for each body part, and classes will conflict.
If you use Inkscape to create or edit existing SVG files, it will be the case.
