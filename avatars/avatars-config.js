var avatars_config = {
    "width": 300,
    "height": 400,
    "select_width": 75,
    "select_height": 100,
    "parts": {
        "body" : {
            "types" : [
                "default"
            ],
            "components" : [ "top" ]
        },
        "hair" : {
            "types" : [
                "short", "long"
            ],
            "components" : [ "bottom", "top" ]
        },
        "face-expression" : {
            "types" : [
                "basic", "smile"
            ],
            "components" : [ "top" ]
        },
        "top-clothes" : {
            "types" : [
                "tshirt", "sweatshirt"
            ],
            "components" : [ "top" ]
        },
        "bottom-clothes" : {
            "types" : [
                "pants"
            ],
            "components" : [ "top" ]
        },
        "shoes" : {
            "types" : [
                "basic"
            ],
            "components" : [ "top" ]
        }
    },
    "parts_order": [
        "hair.bottom",
        "body.top",
        "face-expression.top",
        "bottom-clothes.top",        
        "top-clothes.top",
        "hair.top",
        "shoes.top"
    ],
    "colors": {
        "hair": [
            ['#eac37d', '#d6ac69'],
            ['#663300', '#4d2600']
        ],
        "top-clothes": [
            ['#337ab7', '#2b6c9e'],
            ['#b73333', '#9e2b2b'],
            ['#5bb733', '#4d9e2b']
        ],
        "bottom-clothes": [
            ['#50728c'],
            ['#8c507a'],
        ],
    }
}

// Export the avatars_config object
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = avatars_config;
}