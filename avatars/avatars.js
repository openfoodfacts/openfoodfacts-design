// avatars.js

// Sample UI to create an avatar by selecting parts and colors

function createAvatarSVG () {
    // For each part, we will extract the content of the selected part type SVG
    // and create a new SVG element with the selected parts and re"turn the SVG element

    const avatarSVG = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    avatarSVG.setAttribute("width", avatars_config.width);
    avatarSVG.setAttribute("height", avatars_config.height);
    avatarSVG.setAttribute("viewBox", `0 0 ${avatars_config.width} ${avatars_config.height}`);
    avatarSVG.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    avatarSVG.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
    avatarSVG.setAttribute("id", "avatar-svg");
    avatarSVG.style.position = 'relative';
    avatarSVG.style.width = `${avatars_config.width}px`;
    avatarSVG.style.height = `${avatars_config.height}px`;

    // For each part in the order defined in avatars_config.parts_order
    avatars_config.parts_order.forEach(partComponent => {
        const [part, component] = partComponent.split('.');
        const partElement = document.getElementById(`avatar-${part}`);
        // Get the index of the selected colors, for all parts
        // (as some parts use colors from other parts, e.g. face-expression uses hair colors)
        let selectedColorsIndexes = {};
        for (const colorPart in avatars_config.colors) {
            const selectedColorElement = document.querySelector(`#avatar-colors-${colorPart} .selected`);
            if (selectedColorElement) {
                const colorIdParts = selectedColorElement.id.split('-');
                // Get the index of the color from the id, which is in the format avatar-color-part-index
                const colorIndex = parseInt(colorIdParts[colorIdParts.length - 1], 10);
                selectedColorsIndexes[colorPart] = colorIndex; // Store the index of the selected color
            } else {
                selectedColorsIndexes[colorPart] = 0; // Default to the first color if none is selected
            }
        }

        if (partElement) {
            // Find the selected type element
            console.log(`Processing part: ${part}, component: ${component}`);
            const selectedTypeElement = Array.from(partElement.children).find(child => child.classList.contains('selected'));
            if (selectedTypeElement) {
                // Get the SVG for the selected type and component
                console.log(`Selected type element for ${part}:`, selectedTypeElement);
                const svgElement = selectedTypeElement.querySelector(`object[data*="${component}"]`);
                // We need to extract the SVG content inside the img element and add it to the avatarSVG
                if (svgElement) {
                    console.log(`Adding ${part}.${component} to avatar`);
                    // Add all the top level elements except the <svg> tag itself
                    // Note: contentDocument only works if the SVG is loaded from the same origin (on a web server)
                    // it does not work locally
                    const svgContent = svgElement.contentDocument;
                    const svgChildren = Array.from(svgContent.children);
                    svgChildren.forEach(child => {
                        // Get the SVG code as a string, so that we can find and replace colors easily
                        let svgCode = new XMLSerializer().serializeToString(child);

                        // Replace colors in the SVG code for parts that have colors defined
                        // when the selected color is not the first one (index 0)
                        for (const colorPart in avatars_config.colors) {
                            if (selectedColorsIndexes[colorPart] > 0) {
                                const originalColors = avatars_config.colors[colorPart][0];
                                const selectedColors = avatars_config.colors[colorPart][selectedColorsIndexes[colorPart]];
                                // Replace all instances of the original colors with the selected colors
                                console.log(`Replacing colors for ${part}:`, originalColors, 'with', selectedColors);
                                for (let j = 0; j < originalColors.length; j++) {
                                    // Replace the color in the SVG code
                                    svgCode = svgCode.replace(new RegExp(originalColors[j], 'g'), selectedColors[j]);
                                }
                            }
                        }

                        // Create a new SVG element from the modified SVG code and append it
                        newSvgElement = document.createElementNS("http://www.w3.org/2000/svg", "g");
                        newSvgElement.innerHTML = svgCode;
                        // Set the id of the new SVG element to the part and component
                        newSvgElement.id = `${part}-${component}`;
                        // Add the new SVG element to the avatarSVG
                        avatarSVG.appendChild(newSvgElement);
                    });
                }

            }
        }
    });

    return avatarSVG;
}

function updateAvatar () {
    // Create the avatar SVG element
    const avatarSVG = createAvatarSVG();
    
    // Get the avatar container and clear it
    const avatarContainer = document.getElementById('avatar-container');
    avatarContainer.innerHTML = ''; // Clear previous content
    
    // Append the new avatar SVG to the container
    avatarContainer.appendChild(avatarSVG);
}

function initAvatars () {

    const avatarsElement = document.getElementById('avatars');
    // For each part, we display the SVGs for each type, on a single row
    for (const part in avatars_config.parts) {
        const partElement = document.createElement('div');
        partElement.className = 'avatar-part';
        partElement.id = `avatar-${part}`;
        partElement.style.display = 'flex';
        partElement.style.flexDirection = 'row';

        // If the part has colors defined, display selectable squares for each color, and automatically select the first color      
        if (avatars_config.colors[part]) {
            const colorsElement = document.createElement('div');
            colorsElement.className = 'avatar-part-colors';
            colorsElement.id = `avatar-colors-${part}`;
            colorsElement.style.display = 'flex';
            colorsElement.style.flexDirection = 'row';

            avatars_config.colors[part].forEach((colorPair, index) => {
                const colorElement = document.createElement('div');
                colorElement.className = `avatar-color`;
                colorElement.style.background = `${colorPair[0]}`;
                // Add an id to identify the part name and the index of the colors
                colorElement.id = `avatar-color-${part}-${index}`;

                // Add click event listener to change the color
                colorElement.addEventListener('click', () => {
                    // Remove "selected" class from all sibling color elements
                    Array.from(colorsElement.children).forEach(child => child.classList.remove('selected'));
                    // Add "selected" class to the clicked color element
                    colorElement.classList.add('selected');
                    // Update the avatar
                    updateAvatar();
                });

                // Add "selected" class to the first color element
                if (index === 0) {
                    colorElement.classList.add('selected');
                }

                colorsElement.appendChild(colorElement);
            });

            partElement.appendChild(colorsElement);
            
        }        

        avatars_config.parts[part].types.forEach((type, index) => {
            
            // Each part can have multiple components, so we iterate over them
            // We create a fixed width and height div for each type of part so that we can display the SVG for all components inside it, one on top of the other
            let svgFilename;
            const typeElement = document.createElement('div');
            typeElement.className = `avatar-part-type`;
            typeElement.style.position = 'relative';
            typeElement.style.width = `${avatars_config.select_width}px`;
            typeElement.style.height = `${avatars_config.select_height}px`;

            // Add "selected" class to the first type element
            if (index === 0) {
                typeElement.classList.add('selected');
            }

            // Add click event listener to make the type selectable
            typeElement.addEventListener('click', () => {
                // Remove "selected" class from all sibling type elements
                Array.from(partElement.children).forEach(child => child.classList.remove('selected'));
                // Add "selected" class to the clicked type element
                typeElement.classList.add('selected');
                // Update the avatar
                updateAvatar();
            });

            partElement.appendChild(typeElement);
            avatars_config.parts[part].components.forEach(component => {
                svgFilename = `svg/${part}.${type}.${component}.svg`;
                // We load the SVG in a HTML object so that we can manipulate its content
                const svgElement = document.createElement('object');
                svgElement.type = 'image/svg+xml';
                svgElement.className = `avatar-svg ${part}-${type}-${component}`;
                // Change the CSS of the SVG element to make it stack on other elements of the same part type
                svgElement.style.position = 'absolute';
                svgElement.style.top = '0';
                svgElement.style.left = '0';
                svgElement.style.width = '100%';
                svgElement.style.height = '100%';
                // We need pointer-events:none; so that the clicks go through to the type element
                svgElement.style.pointerEvents = 'none';
                // Set the source of the SVG
                svgElement.data = svgFilename;

                typeElement.appendChild(svgElement);
            });

            // Hide the body part
            if (part === 'body') {
                //typeElement.style.display = 'none';
            }
        });

        avatarsElement.appendChild(partElement);
    }

}