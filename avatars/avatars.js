// Open Food Facts Avatar Generator (Fixed & Modernized)

let currentAvatarState = {
    selectedTypes: {},
    selectedColors: {}
};

// Helper: parse raw SVG string and return inner elements
function parseSvgInner(svgString) {
    if (!svgString) return "";
    // Remove xml prolog and doctype
    let cleaned = svgString.replace(/<\?xml[^>]*\?>/gi, '').replace(/<!DOCTYPE[^>]*>/gi, '');
    // Match content between <svg ...> and </svg>
    const match = cleaned.match(/<svg[^>]*>([\s\S]*)<\/svg>/i);
    return match ? match[1] : cleaned;
}

// Get SVG content for a given part, type, and component
function getPartSvgString(part, type, component) {
    const filename = `${part}.${type}.${component}.svg`;
    if (typeof AVATAR_SVGS !== 'undefined' && AVATAR_SVGS[filename]) {
        return AVATAR_SVGS[filename];
    }
    return null;
}

// Build the composed Avatar SVG
function createAvatarSVG() {
    const width = avatars_config.width || 250;
    const height = avatars_config.height || 300;

    const avatarSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    avatarSvg.setAttribute("width", "100%");
    avatarSvg.setAttribute("height", "100%");
    avatarSvg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    avatarSvg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    avatarSvg.setAttribute("id", "avatar-svg");

    // Defs wrapper for any gradients/clipPaths
    const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    avatarSvg.appendChild(defs);

    // Render layers in parts_order
    avatars_config.parts_order.forEach(partComponent => {
        const [part, component] = partComponent.split('.');
        const selectedType = currentAvatarState.selectedTypes[part];

        if (!selectedType) return;

        let rawSvg = getPartSvgString(part, selectedType, component);
        if (!rawSvg) return;

        let innerContent = parseSvgInner(rawSvg);

        // Extract <defs> content if any and put into top defs
        const defsMatch = innerContent.match(/<defs[^>]*>([\s\S]*?)<\/defs>/gi);
        if (defsMatch) {
            defsMatch.forEach(d => {
                const defInner = d.replace(/<\/?defs[^>]*>/gi, '');
                defs.innerHTML += defInner;
            });
            innerContent = innerContent.replace(/<defs[^>]*>[\s\S]*?<\/defs>/gi, '');
        }

        // Apply color replacements across defined palettes
        for (const colorPart in avatars_config.colors) {
            const selectedColorIdx = currentAvatarState.selectedColors[colorPart] || 0;
            if (selectedColorIdx > 0 && avatars_config.colors[colorPart][selectedColorIdx]) {
                const originalColors = avatars_config.colors[colorPart][0];
                const newColors = avatars_config.colors[colorPart][selectedColorIdx];

                for (let i = 0; i < originalColors.length; i++) {
                    const orig = originalColors[i];
                    const repl = newColors[i] || newColors[0];
                    if (orig && repl) {
                        innerContent = innerContent.replace(new RegExp(orig, 'gi'), repl);
                    }
                }
            }
        }

        // Create a grouping element for the component
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("id", `avatar-${part}-${component}`);
        g.innerHTML = innerContent;
        avatarSvg.appendChild(g);
    });

    return avatarSvg;
}

// Update the avatar in the DOM preview
function updateAvatar() {
    const container = document.getElementById('avatar-container');
    if (!container) return;

    const newSvg = createAvatarSVG();
    container.innerHTML = '';
    container.appendChild(newSvg);
}

// Randomize all avatar parts and colors
function randomizeAvatar() {
    for (const part in avatars_config.parts) {
        const types = avatars_config.parts[part].types;
        currentAvatarState.selectedTypes[part] = types[Math.floor(Math.random() * types.length)];
    }
    for (const colorPart in avatars_config.colors) {
        const colors = avatars_config.colors[colorPart];
        currentAvatarState.selectedColors[colorPart] = Math.floor(Math.random() * colors.length);
    }
    syncUiSelections();
    updateAvatar();
}

// Sync UI active states with current state
function syncUiSelections() {
    for (const part in currentAvatarState.selectedTypes) {
        const selectedType = currentAvatarState.selectedTypes[part];
        const container = document.getElementById(`avatar-types-${part}`);
        if (container) {
            Array.from(container.children).forEach(child => {
                if (child.dataset.type === selectedType) {
                    child.classList.add('selected');
                } else {
                    child.classList.remove('selected');
                }
            });
        }
    }

    for (const colorPart in currentAvatarState.selectedColors) {
        const selectedIdx = currentAvatarState.selectedColors[colorPart];
        const container = document.getElementById(`avatar-colors-${colorPart}`);
        if (container) {
            Array.from(container.children).forEach((child, idx) => {
                if (idx === selectedIdx) {
                    child.classList.add('selected');
                } else {
                    child.classList.remove('selected');
                }
            });
        }
    }
}

// Download generated SVG
function downloadAvatarSvg() {
    const container = document.getElementById('avatar-container');
    const svgEl = container ? container.querySelector('svg') : null;
    if (!svgEl) return;

    const serializer = new XMLSerializer();
    let source = serializer.serializeToString(svgEl);
    if (!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)) {
        source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
    }
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `openfoodfacts-avatar-${Date.now()}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Copy SVG markup to clipboard
function copyAvatarSvg(btnElement) {
    const container = document.getElementById('avatar-container');
    const svgEl = container ? container.querySelector('svg') : null;
    if (!svgEl) return;

    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svgEl);
    navigator.clipboard.writeText(source).then(() => {
        if (btnElement) {
            const origText = btnElement.innerText;
            btnElement.innerText = "✓ Copied!";
            setTimeout(() => { btnElement.innerText = origText; }, 2000);
        }
    });
}

// Initialize the avatar generator UI
function initAvatars() {
    const controlsContainer = document.getElementById('avatars-controls') || document.getElementById('avatars');
    if (!controlsContainer) return;

    controlsContainer.innerHTML = '';

    // Initialize default or random state
    for (const part in avatars_config.parts) {
        const types = avatars_config.parts[part].types;
        currentAvatarState.selectedTypes[part] = types[0];
    }
    for (const colorPart in avatars_config.colors) {
        currentAvatarState.selectedColors[colorPart] = 0;
    }

    // Friendly labels
    const friendlyPartNames = {
        "body": "Skin Tone & Body",
        "hair": "Hairstyle",
        "face-expression": "Expression",
        "top-clothes": "T-Shirts & Tops",
        "bottom-clothes": "Bottom Clothes",
        "shoes": "Shoes"
    };

    // Render part sections
    for (const part in avatars_config.parts) {
        const partSection = document.createElement('div');
        partSection.className = 'avatar-part-section bg-slate-50 dark:bg-stone-900 border border-slate-200 dark:border-stone-800 rounded-2xl p-4 mb-4';

        const titleRow = document.createElement('div');
        titleRow.className = 'flex items-center justify-between mb-3';
        titleRow.innerHTML = `<h3 class="text-sm font-bold text-slate-800 dark:text-stone-200 uppercase tracking-wide">${friendlyPartNames[part] || part}</h3>`;
        partSection.appendChild(titleRow);

        // Color swatches if defined for this part
        if (avatars_config.colors[part]) {
            const colorsWrap = document.createElement('div');
            colorsWrap.className = 'avatar-part-colors flex items-center gap-2 mb-3.5';
            colorsWrap.id = `avatar-colors-${part}`;

            avatars_config.colors[part].forEach((colorPair, idx) => {
                const swatch = document.createElement('button');
                swatch.type = 'button';
                swatch.className = `w-7 h-7 rounded-full transition shadow-xs border-2 border-white dark:border-stone-900 cursor-pointer ${idx === 0 ? 'selected ring-2 ring-orange-500 scale-110' : 'hover:scale-105'}`;
                swatch.style.backgroundColor = colorPair[0];
                swatch.title = `Color option ${idx + 1}`;

                swatch.addEventListener('click', () => {
                    currentAvatarState.selectedColors[part] = idx;
                    syncUiSelections();
                    updateAvatar();
                });

                colorsWrap.appendChild(swatch);
            });

            partSection.appendChild(colorsWrap);
        }

        // Part type options
        const typesWrap = document.createElement('div');
        typesWrap.className = 'avatar-part-types flex flex-wrap gap-2.5';
        typesWrap.id = `avatar-types-${part}`;

        avatars_config.parts[part].types.forEach((type, idx) => {
            const typeBtn = document.createElement('button');
            typeBtn.type = 'button';
            typeBtn.dataset.type = type;
            typeBtn.className = `avatar-type-btn p-2 rounded-xl border border-slate-200 dark:border-stone-700 bg-white dark:bg-stone-800 hover:border-orange-400 transition flex flex-col items-center justify-center cursor-pointer ${idx === 0 ? 'selected border-orange-500 ring-2 ring-orange-500/30' : ''}`;
            typeBtn.style.minWidth = "70px";

            // Thumbnail preview (mini SVG)
            const mainComp = avatars_config.parts[part].components[0] || 'top';
            const miniSvg = getPartSvgString(part, type, mainComp);
            if (miniSvg) {
                const thumb = document.createElement('div');
                thumb.className = 'w-12 h-14 overflow-hidden pointer-events-none flex items-center justify-center';
                thumb.innerHTML = miniSvg;
                const innerSvg = thumb.querySelector('svg');
                if (innerSvg) {
                    innerSvg.setAttribute('width', '100%');
                    innerSvg.setAttribute('height', '100%');
                }
                typeBtn.appendChild(thumb);
            }

            const label = document.createElement('span');
            label.className = 'text-[11px] font-semibold text-slate-600 dark:text-stone-300 mt-1 capitalize';
            label.innerText = type.replace('tshirt-', '').replace('-beige', '');
            typeBtn.appendChild(label);

            typeBtn.addEventListener('click', () => {
                currentAvatarState.selectedTypes[part] = type;
                syncUiSelections();
                updateAvatar();
            });

            typesWrap.appendChild(typeBtn);
        });

        partSection.appendChild(typesWrap);
        controlsContainer.appendChild(partSection);
    }

    // Attach event listeners for buttons if they exist
    const randBtn = document.getElementById('btn-randomize');
    if (randBtn) randBtn.addEventListener('click', randomizeAvatar);

    const dlBtn = document.getElementById('btn-download-svg');
    if (dlBtn) dlBtn.addEventListener('click', downloadAvatarSvg);

    const copyBtn = document.getElementById('btn-copy-svg');
    if (copyBtn) copyBtn.addEventListener('click', () => copyAvatarSvg(copyBtn));

    // Initial render
    syncUiSelections();
    updateAvatar();
}

// Global hook
if (typeof window !== 'undefined') {
    window.initAvatars = initAvatars;
    window.randomizeAvatar = randomizeAvatar;
    window.downloadAvatarSvg = downloadAvatarSvg;
    window.copyAvatarSvg = copyAvatarSvg;
}
