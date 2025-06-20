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
                "short", "bob", "long", "long-wavy"
            ],
            "components" : [ "bottom", "top" ]
        },
        "face-expression" : {
            "types" : [
                "basic", "smile", "sad"
            ],
            "components" : [ "top" ]
        },
        "top-clothes" : {
            "types" : [
                "tshirt", "tshirt-long-sleeves", "sweatshirt", "tshirt-off-beige", "tshirt-obf-beige", "tshirt-opff-beige", "tshirt-opf-beige"
            ],
            "components" : [ "top" ]
        },
        "bottom-clothes" : {
            "types" : [
                "pants", "shorts", "long-skirt"
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
        "body": [
            ['#ffdab9', '#ddbb9f'],
            ['#b2855f', '#9b7053'],
            ['#967357', '#7f5d46'],
            ['#6d4930', '#59351c']


        ],
        "hair": [
            ['#eac37d', '#d6ac69'],
            ['#663300', '#4d2600'],
            ['#bc6a3c', '#ad603a'],
            ['#3d1e09', '#351b09']
        ],
        "top-clothes": [
            ['#337ab7', '#2b6c9e'],
            ['#b73333', '#9e2b2b'],
            ['#5bb733', '#4d9e2b'],
            ['#6d6d6d', '#606060']

        ],
        "bottom-clothes": [
            ['#50728c'],
            ['#8c507a'],
            ['#5a9361'],
            ['#88a2a8'],
            ['#303f56']
        ],
    }
}

// Export the avatars_config object
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = avatars_config;
}