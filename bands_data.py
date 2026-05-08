"""J-rock band database with genre tags for recommendations (~100 bands)."""

import re
from difflib import get_close_matches

BANDS = [
    # ============================================================
    # Shoegaze / Dream Pop
    # ============================================================
    {
        "name": "SUPERCAR",
        "aliases": ["supercar", "super car", "スーパーカー", "supaca"],
        "tags": ["shoegaze", "indie", "electronic", "dream-pop", "alternative"],
        "desc": "90年代日本盯鞋/电子摇滚传奇。石渡淳治+中村弘二，从吉他噪音墙到电子实验的进化，日本独立摇滚的里程碑。",
        "similar": ["COALTAR OF THE DEEPERS", "Number Girl", "きのこ帝国 (Kinoko Teikoku)", "cruyff in the bedroom", "Syrup16g (シロップ)"],
    },
    {
        "name": "きのこ帝国 (Kinoko Teikoku)",
        "aliases": ["kinoko teikoku", "kinokoteikoku", "きのこていこく", "kinoko", "mushroom empire"],
        "tags": ["shoegaze", "dream-pop", "indie", "female-vocal"],
        "desc": "梦幻感极强的盯鞋乐队，女主唱佐藤千亜妃的声线空灵飘渺。《渦になる》是入坑神曲。",
        "similar": ["My Dead Girlfriend", "溶けない名前 (Tokenai Namae)", "COALTAR OF THE DEEPERS", "SUPERCAR", "yuragi"],
    },
    {
        "name": "My Dead Girlfriend",
        "aliases": ["my dead girlfriend", "mydg", "dead girlfriend"],
        "tags": ["shoegaze", "noise-pop", "electronic", "indie"],
        "desc": "电子噪响与盯鞋美学的完美融合，甜腻旋律下藏着噪音墙。",
        "similar": ["きのこ帝国 (Kinoko Teikoku)", "COALTAR OF THE DEEPERS", "cruyff in the bedroom", "pasteboard"],
    },
    {
        "name": "COALTAR OF THE DEEPERS",
        "aliases": ["coaltar", "coal tar of the deepers", "cotd", "coaltar of the deepers"],
        "tags": ["shoegaze", "alternative", "heavy", "indie"],
        "desc": "日本盯鞋鼻祖级乐队，将重型吉他与梦幻旋律结合，影响了一代日本独立音乐人。",
        "similar": ["My Dead Girlfriend", "cruyff in the bedroom", "Number Girl", "SUPERCAR", "dive"],
    },
    {
        "name": "cruyff in the bedroom",
        "aliases": ["cruyff", "cruyff in bedroom", "citb"],
        "tags": ["shoegaze", "dream-pop", "indie"],
        "desc": "经典的日系盯鞋之声，名字向 The Velvet Underground 和 My Bloody Valentine 双重致敬。",
        "similar": ["COALTAR OF THE DEEPERS", "きのこ帝国 (Kinoko Teikoku)", "溶けない名前 (Tokenai Namae)", "Hartfield"],
    },
    {
        "name": "dive",
        "aliases": ["dive", "ダイブ"],
        "tags": ["shoegaze", "noise-pop", "indie"],
        "desc": "90年代日本盯鞋场景的核心乐队之一，厚重的吉他噪音墙与 MBV 影响明显。",
        "similar": ["COALTAR OF THE DEEPERS", "cruyff in the bedroom", "Honeydip", "SUPERCAR"],
    },
    {
        "name": "Honeydip",
        "aliases": ["honeydip", "honey dip", "ハニーディップ"],
        "tags": ["shoegaze", "dream-pop", "indie", "female-vocal"],
        "desc": "早期日本盯鞋代表，女主唱的甜美声线与层叠吉他音墙的交织。",
        "similar": ["dive", "cruyff in the bedroom", "My Dead Girlfriend", "Luminous Orange"],
    },
    {
        "name": "Luminous Orange",
        "aliases": ["luminous orange", "ルミナスオレンジ"],
        "tags": ["shoegaze", "dream-pop", "indie", "female-vocal"],
        "desc": "横滨发祥的长寿盯鞋乐队，从 90 年代活跃至今，国际合作经验丰富。",
        "similar": ["Honeydip", "dive", "My Dead Girlfriend", "Oeil"],
    },
    {
        "name": "Oeil",
        "aliases": ["oeil", "オエイユ"],
        "tags": ["shoegaze", "dream-pop", "indie", "female-vocal"],
        "desc": "东京的梦幻盯鞋二人组，Lo-Fi 质感 + 飘渺女声，Bandcamp 世代日系盯鞋的代表。",
        "similar": ["yuragi", "溶けない名前 (Tokenai Namae)", "For Tracy Hyde", "Luminous Orange"],
    },
    {
        "name": "yuragi",
        "aliases": ["yuragi", "ゆらぎ", "yuragu"],
        "tags": ["shoegaze", "dream-pop", "indie"],
        "desc": "新一代日系盯鞋/梦泡的代表，《nightlife》EP 在国际盯鞋圈引起广泛关注。",
        "similar": ["Oeil", "きのこ帝国 (Kinoko Teikoku)", "For Tracy Hyde", "Moon in June"],
    },
    {
        "name": "pasteboard",
        "aliases": ["pasteboard", "ペーストボード"],
        "tags": ["shoegaze", "dream-pop", "indie"],
        "desc": "日本盯鞋名盘《glitter》的创作者，甜美旋律与厚实音墙的完美平衡。",
        "similar": ["My Dead Girlfriend", "SUPERCAR", "COALTAR OF THE DEEPERS", "CQ"],
    },
    {
        "name": "溶けない名前 (Tokenai Namae)",
        "aliases": ["tokenai namae", "tokenainamae", "とけないなまえ", "tokenai", "unmelting name"],
        "tags": ["shoegaze", "dream-pop", "female-vocal", "indie"],
        "desc": "温柔的女声盯鞋，像不会融化的名字一样留下持久的余韵。",
        "similar": ["きのこ帝国 (Kinoko Teikoku)", "My Dead Girlfriend", "For Tracy Hyde", "CQ"],
    },
    {
        "name": "For Tracy Hyde",
        "aliases": ["for tracy hyde", "forth", "tracy hyde", "for tracy"],
        "tags": ["shoegaze", "dream-pop", "indie", "female-vocal"],
        "desc": "青春感满溢的盯鞋/梦泡乐队，旋律甜美而富有层次。",
        "similar": ["溶けない名前 (Tokenai Namae)", "きのこ帝国 (Kinoko Teikoku)", "Moon in June", "yuragi"],
    },
    {
        "name": "Moon in June",
        "aliases": ["moon in june", "mij"],
        "tags": ["shoegaze", "dream-pop", "indie", "female-vocal"],
        "desc": "台湾×日本的跨国梦泡计划，充满迷离感的人声与吉他音墙。",
        "similar": ["For Tracy Hyde", "溶けない名前 (Tokenai Namae)", "きのこ帝国 (Kinoko Teikoku)", "yuragi"],
    },
    {
        "name": "CQ",
        "aliases": ["cq", "c.q.", "seekyou"],
        "tags": ["shoegaze", "dream-pop", "indie", "female-vocal"],
        "desc": "东京发的地下盯鞋新星，Lo-Fi 质感 + 甜美旋律。",
        "similar": ["For Tracy Hyde", "溶けない名前 (Tokenai Namae)", "きのこ帝国 (Kinoko Teikoku)", "pasteboard"],
    },
    {
        "name": "RAY",
        "aliases": ["ray", "レイ"],
        "tags": ["shoegaze", "dream-pop", "indie"],
        "desc": "大阪的盯鞋/梦泡乐队，细腻的吉他编曲和温暖的旋律线条。",
        "similar": ["CRUYFF IN THE BEDROOM", "Hartfield", "yuragi", "Oeil"],
    },
    {
        "name": "Hartfield",
        "aliases": ["hartfield", "ハートフィールド"],
        "tags": ["shoegaze", "dream-pop", "indie"],
        "desc": "日本盯鞋场景的中坚力量，干净的吉他音色与内省式旋律。",
        "similar": ["cruyff in the bedroom", "RAY", "dive", "COALTAR OF THE DEEPERS"],
    },
    {
        "name": "sphere",
        "aliases": ["sphere", "スフィア"],
        "tags": ["shoegaze", "dream-pop", "electronic", "indie"],
        "desc": "电子元素与盯鞋吉他的融合，太空感的音景设计。",
        "similar": ["SUPERCAR", "pasteboard", "COALTAR OF THE DEEPERS", "World's End Girlfriend"],
    },
    {
        "name": "揺籠 (Yurikago)",
        "aliases": ["yurikago", "ゆりかご", "cradle"],
        "tags": ["shoegaze", "dream-pop", "female-vocal", "indie"],
        "desc": "东京女子盯鞋新锐，甜美而忧伤的旋律包裹在朦胧的吉他噪音中。",
        "similar": ["CQ", "Oeil", "溶けない名前 (Tokenai Namae)", "For Tracy Hyde"],
    },
    {
        "name": "COLLAPSE",
        "aliases": ["collapse", "コラプス"],
        "tags": ["shoegaze", "noise-pop", "indie"],
        "desc": "地下盯鞋/噪响流行乐队，粗粝的质感和高密度的吉他音墙。",
        "similar": ["My Dead Girlfriend", "dive", "COALTAR OF THE DEEPERS", "pasteboard"],
    },

    # ============================================================
    # Dream Pop / Indie Pop / Shibuya-kei
    # ============================================================
    {
        "name": "The fin.",
        "aliases": ["the fin", "the fin.", "fin", "ザ・フィン"],
        "tags": ["dream-pop", "indie", "electronic", "shoegaze"],
        "desc": "神户发祥的梦幻流行/电子乐队，英文歌词 + 迷幻合成器音色，国际巡演广泛。",
        "similar": ["SUPERCAR", "Mitsume", "Yogee New Waves", "Suchmos"],
    },
    {
        "name": "Mitsume (ミツメ)",
        "aliases": ["mitsume", "ミツメ", "mitsume"],
        "tags": ["indie-pop", "dream-pop", "indie"],
        "desc": "东京 indie pop 代表，简洁清爽的吉他编排和温存的日常感旋律。",
        "similar": ["The fin.", "Yogee New Waves", "advantage Lucy", "Lucky Tapes"],
    },
    {
        "name": "Lamp",
        "aliases": ["lamp", "ランプ"],
        "tags": ["indie-pop", "shibuya-kei", "bossanova", "dream-pop"],
        "desc": "涩谷系/巴西风味的独立流行三人组，精致柔软的城市夜曲。",
        "similar": ["advantage Lucy", "Mitsume", "cero", "The fin."],
    },
    {
        "name": "advantage Lucy",
        "aliases": ["advantage lucy", "advantage lucy", "アドバンテージルーシー", "adlucy"],
        "tags": ["indie-pop", "shibuya-kei", "indie", "dream-pop"],
        "desc": "涩谷系 indie pop 标志性乐队，阳光午后般的吉他流行曲。",
        "similar": ["Lamp", "Mitsume", "the brilliant green", "The fin."],
    },
    {
        "name": "the brilliant green",
        "aliases": ["brilliant green", "the brilliant green", "ブリグリ", "buriguri"],
        "tags": ["indie-pop", "alternative", "j-rock", "indie"],
        "desc": "川瀬智子+奥田俊作的双人组合，英伦吉他流行与日系旋律的完美结合。",
        "similar": ["advantage Lucy", "Asian Kung-Fu Generation", "the pillows", "The fin."],
    },

    # ============================================================
    # City Pop / Neo City Pop
    # ============================================================
    {
        "name": "Yogee New Waves",
        "aliases": ["yogee new waves", "yogee", "ヨギーニューウェイブス"],
        "tags": ["city-pop", "indie-pop", "indie", "alternative"],
        "desc": "东京 neo city-pop 浪潮的旗手，夏天/海滩/敞篷车的青春气息。",
        "similar": ["Suchmos", "Mitsume", "cero", "Never Young Beach"],
    },
    {
        "name": "Suchmos",
        "aliases": ["suchmos", "サチモス"],
        "tags": ["city-pop", "indie", "acid-jazz", "alternative"],
        "desc": "神奈川出身，将 acid jazz / city pop / rock 融为一体的国民级独立乐队。",
        "similar": ["Yogee New Waves", "cero", "Never Young Beach", "The fin."],
    },
    {
        "name": "cero",
        "aliases": ["cero", "セロ"],
        "tags": ["city-pop", "indie", "jazz", "alternative"],
        "desc": "东京 city pop 三人组，精巧的编曲和对都市空间的诗意书写。",
        "similar": ["Suchmos", "Yogee New Waves", "Lamp", "Lucky Tapes"],
    },
    {
        "name": "Never Young Beach (ネバーヤングビーチ)",
        "aliases": ["never young beach", "ネバーヤングビーチ", "nyb", "never young"],
        "tags": ["city-pop", "indie-pop", "indie"],
        "desc": "东京 city pop 乐队，轻松惬意的日常感和复古流行旋律。",
        "similar": ["Yogee New Waves", "Suchmos", "Mitsume", "cero"],
    },
    {
        "name": "Lucky Tapes",
        "aliases": ["lucky tapes", "ラッキーテープス"],
        "tags": ["city-pop", "indie-pop", "jazz", "indie"],
        "desc": "东京 neo city pop 代表，铜管编排和 groovy 节奏带来都会的浮遊感。",
        "similar": ["Suchmos", "cero", "Yogee New Waves", "Lamp"],
    },

    # ============================================================
    # Emo / Post-Hardcore / Screamo
    # ============================================================
    {
        "name": "envy",
        "aliases": ["envy"],
        "tags": ["screamo", "post-rock", "emo", "hardcore"],
        "desc": "日本 screamo 传奇，从硬核嘶吼到后摇长曲，情绪爆发力无人能及。",
        "similar": ["heaven in her arms", "downy", "Mono", "1000 travels of jawah"],
    },
    {
        "name": "heaven in her arms",
        "aliases": ["heaven in her arms", "hiha", "heaven"],
        "tags": ["screamo", "post-rock", "emo", "hardcore"],
        "desc": "继承 envy 衣钵的东京 screamo 乐队，兼具爆裂与唯美。",
        "similar": ["envy", "downy", "Pale", "1000 travels of jawah"],
    },
    {
        "name": "1000 travels of jawah",
        "aliases": ["1000 travels of jawah", "sento", "jawah", "1000 travels"],
        "tags": ["screamo", "emo", "hardcore", "post-rock"],
        "desc": "名古屋 screamo/emo 核心乐队，欧洲巡演经验丰富，情绪爆发的感染力极强。",
        "similar": ["envy", "heaven in her arms", "killie", "Pale"],
    },
    {
        "name": "killie",
        "aliases": ["killie", "キリー"],
        "tags": ["screamo", "emo", "hardcore"],
        "desc": "90s 末-00s 初日本 screamo 场景的重要存在，狂暴与脆弱并存。",
        "similar": ["envy", "1000 travels of jawah", "tetola93", "there is a fox in the flames"],
    },
    {
        "name": "tetola93",
        "aliases": ["tetola93", "tetola", "93"],
        "tags": ["screamo", "emo", "hardcore"],
        "desc": "新生代日系 screamo 的代表之一，继承了 90 年代草根 hardcore 的精神。",
        "similar": ["killie", "1000 travels of jawah", "heaven in her arms", "Pale"],
    },
    {
        "name": "there is a fox in the flames",
        "aliases": ["there is a fox in the flames", "tiafitf", "fox in the flames"],
        "tags": ["screamo", "emo", "post-rock", "hardcore"],
        "desc": "东京 screamo 新锐，长篇情绪铺陈与突然的爆发，受 envy 影响明显。",
        "similar": ["envy", "heaven in her arms", "1000 travels of jawah", "Pale"],
    },
    {
        "name": "FACT",
        "aliases": ["fact", "fact japan", "ファクト"],
        "tags": ["post-hardcore", "emo", "alternative", "indie"],
        "desc": "日本的国际化 post-hardcore 乐队，clean/metal vocal 切换自如，海外知名度极高。",
        "similar": ["Pay money To my Pain", "coldrain", "9mm Parabellum Bullet", "ONE OK ROCK"],
    },
    {
        "name": "Pay money To my Pain (PTP)",
        "aliases": ["pay money to my pain", "ptp", "pay money", "ペイマネ"],
        "tags": ["post-hardcore", "alternative", "emo", "indie"],
        "desc": "东京 post-hardcore/alternative 名团，主唱 K 的英日双语歌词和情绪化演绎令人难忘。",
        "similar": ["FACT", "coldrain", "ONE OK ROCK", "9mm Parabellum Bullet"],
    },
    {
        "name": "coldrain",
        "aliases": ["coldrain", "コールドレイン"],
        "tags": ["post-hardcore", "alternative", "emo", "metalcore"],
        "desc": "名古屋出身、全英文歌词的 post-hardcore / metalcore 乐队，国际知名度极高。",
        "similar": ["FACT", "Pay money To my Pain (PTP)", "ONE OK ROCK", "Crossfaith"],
    },
    {
        "name": "HaKU",
        "aliases": ["haku", "ハク"],
        "tags": ["emo", "indie", "alternative", "post-rock"],
        "desc": "大阪 emo/indie 乐队，高亢的情感化人声和后摇式的音墙铺陈。",
        "similar": ["the cabs", "Ling Tosite Sigure (凛として時雨)", "9mm Parabellum Bullet", "cinema staff"],
    },
    {
        "name": "Ling Tosite Sigure (凛として時雨)",
        "aliases": ["ling tosite sigure", "ling", "sigure", "凛として時雨", "りんとしてしぐれ", "凛時雨"],
        "tags": ["post-hardcore", "emo", "indie", "math-rock"],
        "desc": "男女双主唱的激烈后硬核，TK 的独特假声与复杂的数摇节奏交织。",
        "similar": ["9mm Parabellum Bullet", "the cabs", "tricot", "HaKU"],
    },
    {
        "name": "9mm Parabellum Bullet",
        "aliases": ["9mm", "9mm parabellum", "kyumu", "9mm parabellum bullet"],
        "tags": ["post-hardcore", "alternative", "emo", "indie"],
        "desc": "高速激烈的日系另类摇滚，充满青春反叛的能量感。",
        "similar": ["Ling Tosite Sigure (凛として時雨)", "the cabs", "THE NOVEMBERS", "HaKU"],
    },
    {
        "name": "the cabs",
        "aliases": ["cabs", "thecabs", "the cabs", "cabss"],
        "tags": ["math-rock", "emo", "post-hardcore", "indie"],
        "desc": "短暂的传奇，复杂的数学摇滚结构与情绪化歌词，解散后仍被深深怀念。",
        "similar": ["Ling Tosite Sigure (凛として時雨)", "tricot", "9mm Parabellum Bullet", "HaKU"],
    },
    {
        "name": "downy",
        "aliases": ["downy", "ダウニー"],
        "tags": ["post-rock", "emo", "experimental", "hardcore"],
        "desc": "暗黑氛围的后摇/emo，影像与音乐结合的艺术计划。",
        "similar": ["envy", "heaven in her arms", "Mono", "World's End Girlfriend"],
    },
    {
        "name": "Pale",
        "aliases": ["pale", "ペイル"],
        "tags": ["screamo", "emo", "post-rock", "hardcore"],
        "desc": "新生代 screamo 代表，继承了 envy 和 heaven in her arms 的情绪爆发。",
        "similar": ["heaven in her arms", "envy", "downy", "1000 travels of jawah"],
    },

    # ============================================================
    # Math Rock
    # ============================================================
    {
        "name": "tricot",
        "aliases": ["tricot", "トリコ", "toriko"],
        "tags": ["math-rock", "indie", "female-vocal", "alternative"],
        "desc": "京都出身的三女一男数学摇滚乐队，复杂的拍子变化和 catchy 的旋律并存。",
        "similar": ["the cabs", "Ling Tosite Sigure (凛として時雨)", "Mass of the Fermenting Dregs (マスドレ)", "a picture of her"],
    },
    {
        "name": "toe",
        "aliases": ["toe", "トー", "toe band"],
        "tags": ["math-rock", "post-rock", "instrumental", "indie"],
        "desc": "日本器乐摇滚的代表，干净精准的演奏与温暖的情感表达。",
        "similar": ["LITE", "mouse on the keys", "jizue", "té"],
    },
    {
        "name": "LITE",
        "aliases": ["lite", "ライト", "lite band"],
        "tags": ["math-rock", "instrumental", "indie", "progressive"],
        "desc": "纯器乐数学摇滚，节奏锋利、吉他跳跃，现场表现力极强。",
        "similar": ["toe", "mouse on the keys", "tricot", "a picture of her"],
    },
    {
        "name": "mouse on the keys",
        "aliases": ["mouse on the keys", "motk", "mouse", "motk band"],
        "tags": ["math-rock", "jazz", "instrumental", "indie"],
        "desc": "钢琴+鼓的双人器乐计划，爵士与数学摇滚的跨界融合。",
        "similar": ["toe", "LITE", "jizue", "Fox Capture Plan"],
    },
    {
        "name": "jizue",
        "aliases": ["jizue", "ジズー", "jizue band"],
        "tags": ["math-rock", "jazz", "instrumental", "indie"],
        "desc": "京都器乐乐队，爵士钢琴与数学摇滚节奏的交融。",
        "similar": ["mouse on the keys", "toe", "LITE", "Fox Capture Plan"],
    },
    {
        "name": "a picture of her",
        "aliases": ["a picture of her", "apoh", "picture of her"],
        "tags": ["math-rock", "instrumental", "indie", "post-rock"],
        "desc": "东京器乐数学摇滚三人组，优美的吉他旋律线和复杂的节奏结构。",
        "similar": ["toe", "LITE", "how to count one to ten", "hyakkei (百景)"],
    },
    {
        "name": "how to count one to ten",
        "aliases": ["how to count one to ten", "htcott", "how to count"],
        "tags": ["math-rock", "instrumental", "indie", "post-rock"],
        "desc": "东京器乐数摇，toe 式的温暖旋律 + 更跳跃的节奏变化。",
        "similar": ["a picture of her", "toe", "LITE", "hyakkei (百景)"],
    },
    {
        "name": "hyakkei (百景)",
        "aliases": ["hyakkei", "百景", "ひゃっけい", "hyakkei band"],
        "tags": ["math-rock", "instrumental", "indie", "post-rock"],
        "desc": "东京四人器乐数摇乐队，壮大的音景设计和精密的多声部吉他对话。",
        "similar": ["a picture of her", "how to count one to ten", "toe", "té"],
    },
    {
        "name": "mudy on the 昨晩",
        "aliases": ["mudy on the sakuban", "mudy on the 昨晩", "mots", "mudy", "mudy on the sakuban"],
        "tags": ["math-rock", "instrumental", "indie", "experimental"],
        "desc": "名古屋出身的器乐数学摇滚，复杂的变拍子与舞蹈感的律动并存。",
        "similar": ["LITE", "toe", "a picture of her", "tricot"],
    },
    {
        "name": "ハイスイノナサ (haisuinonasa)",
        "aliases": ["haisuinonasa", "ハイスイノナサ", "haisui", "haisui no nasa"],
        "tags": ["math-rock", "post-rock", "indie", "experimental"],
        "desc": "钢琴主导的数学摇滚/后摇，透明感的音色与复杂的节奏结构。",
        "similar": ["mouse on the keys", "toe", "jizue", "matryoshka"],
    },
    {
        "name": "té (テ)",
        "aliases": ["té", "te", "テ", "te band"],
        "tags": ["math-rock", "post-rock", "instrumental", "indie"],
        "desc": "日本器乐摇滚的重要存在，吉他旋律的情绪张力和精密编排。",
        "similar": ["toe", "LITE", "hyakkei (百景)", "miaou"],
    },

    # ============================================================
    # Post-Rock
    # ============================================================
    {
        "name": "Mono",
        "aliases": ["mono", "mono japan"],
        "tags": ["post-rock", "instrumental", "orchestral", "experimental"],
        "desc": "日本后摇的旗帜，恢弘的交响式吉他音墙，与管弦乐团合作演出。",
        "similar": ["envy", "downy", "World's End Girlfriend", "miaou"],
    },
    {
        "name": "World's End Girlfriend",
        "aliases": ["world's end girlfriend", "world end girlfriend", "weg", "worlds end girlfriend", "worlds end"],
        "tags": ["post-rock", "electronic", "experimental", "orchestral"],
        "desc": "前田胜彦的个人计划，将后摇、电子、古典交织成末世般的宏大叙事。",
        "similar": ["Mono", "downy", "KASHIWA Daisuke", "matryoshka"],
    },
    {
        "name": "miaou",
        "aliases": ["miaou", "ミアオ", "miaou band"],
        "tags": ["post-rock", "instrumental", "indie", "electronic"],
        "desc": "东京三人后摇乐队，温暖的电子纹理和清新的吉他旋律。",
        "similar": ["toe", "Mono", "té", "euphoria"],
    },
    {
        "name": "euphoria",
        "aliases": ["euphoria", "ユーフォリア", "euphoria band"],
        "tags": ["post-rock", "instrumental", "indie"],
        "desc": "日本后摇三人组，情绪饱满的吉他叙事和紧凑的节奏编排。",
        "similar": ["miaou", "toe", "té", "Mono"],
    },
    {
        "name": "matryoshka",
        "aliases": ["matryoshka", "マトリョーシカ", "matryoshka band"],
        "tags": ["post-rock", "electronic", "experimental", "female-vocal"],
        "desc": "东京的电子后摇二人组，破碎的女声采样与精致电子音景。",
        "similar": ["World's End Girlfriend", "KASHIWA Daisuke", "ハイスイノナサ (haisuinonasa)", "Anoice"],
    },
    {
        "name": "Anoice",
        "aliases": ["anoice", "アノイス"],
        "tags": ["post-rock", "ambient", "instrumental", "experimental"],
        "desc": "东京的暗黑后摇/氛围团体，影像与音乐结合的多媒体艺术计划。",
        "similar": ["Mono", "World's End Girlfriend", "matryoshka", "downy"],
    },
    {
        "name": "sgt.",
        "aliases": ["sgt", "sgt.", "sgt band"],
        "tags": ["post-rock", "instrumental", "indie", "progressive"],
        "desc": "东京器乐后摇四人组，精密的三吉他编排和 progressive 结构。",
        "similar": ["toe", "miaou", "té", "euphoria"],
    },
    {
        "name": "December",
        "aliases": ["december", "ディセンバー", "december japan"],
        "tags": ["post-rock", "instrumental", "indie"],
        "desc": "名古屋后摇乐队，暗色调的吉他叙事与空旷的音景。",
        "similar": ["Mono", "euphoria", "miaou", "sgt."],
    },
    {
        "name": "Fox Capture Plan",
        "aliases": ["fox capture plan", "fcp", "fox capture"],
        "tags": ["post-rock", "jazz", "instrumental", "indie"],
        "desc": "钢琴三重奏的爵士后摇，紧凑的律动和电影配乐般的叙事性。",
        "similar": ["mouse on the keys", "jizue", "toe", "LITE"],
    },
    {
        "name": "KASHIWA Daisuke",
        "aliases": ["kashiwa daisuke", "kashiwa", "柏大輔", "daisuke kashiwa"],
        "tags": ["post-rock", "electronic", "experimental", "orchestral"],
        "desc": "广岛出身的电子/后摇作曲家，将极简钢琴与电子噪音编织成宏大叙事。",
        "similar": ["World's End Girlfriend", "Mono", "downy", "matryoshka"],
    },

    # ============================================================
    # Indie / Alternative Rock
    # ============================================================
    {
        "name": "Syrup16g (シロップ)",
        "aliases": ["syrup16g", "syrup 16g", "syrup", "シロップ", "shiroppu", "syrup16"],
        "tags": ["indie", "alternative", "emo", "shoegaze"],
        "desc": "五十岚隆领衔的忧郁系独立摇滚，暗黑诗意的歌词与厚重的吉他音墙。日本 00 年代独立场景的基石。",
        "similar": ["SUPERCAR", "Number Girl", "ART-SCHOOL", "THE NOVEMBERS"],
    },
    {
        "name": "ART-SCHOOL",
        "aliases": ["art-school", "art school", "artschool", "artschool band"],
        "tags": ["indie", "alternative", "emo", "shoegaze"],
        "desc": "木下理树领衔的独立摇滚乐队，忧郁的旋律线与 90s 盯鞋影响，日本 indie 场景的长青树。",
        "similar": ["Syrup16g (シロップ)", "SUPERCAR", "THE NOVEMBERS", "Number Girl"],
    },
    {
        "name": "Asian Kung-Fu Generation",
        "aliases": ["asian kung-fu generation", "ajikan", "akfg", "asian kung fu", "アジカン"],
        "tags": ["indie", "alternative", "punk", "j-rock"],
        "desc": "日本独立摇滚的代表性乐队，影响了整整一代人的青春。",
        "similar": ["Number Girl", "ZAZEN BOYS", "ELLEGARDEN", "the pillows"],
    },
    {
        "name": "Number Girl",
        "aliases": ["number girl", "nangirl", "ナンバーガール", "namba girl", "number girl japan"],
        "tags": ["indie", "alternative", "punk", "noise"],
        "desc": "向井秀德领衔的传奇乐队，90年代日本地下摇滚的基石。",
        "similar": ["ZAZEN BOYS", "Asian Kung-Fu Generation", "COALTAR OF THE DEEPERS", "SUPERCAR"],
    },
    {
        "name": "ZAZEN BOYS",
        "aliases": ["zazen boys", "zazen", "ザゼンボーイズ", "zazen boys band"],
        "tags": ["indie", "alternative", "experimental", "math-rock"],
        "desc": "Number Girl 解散后向井秀德的新计划，更实验、更神经质的数学摇滚。",
        "similar": ["Number Girl", "Ling Tosite Sigure (凛として時雨)", "tricot", "Syrup16g (シロップ)"],
    },
    {
        "name": "Mass of the Fermenting Dregs (マスドレ)",
        "aliases": ["mass of the fermenting dregs", "masudore", "マスドレ", "motfd", "massdregs", "masudore band"],
        "tags": ["indie", "alternative", "female-vocal", "post-rock"],
        "desc": "神户三人组，爆裂的贝斯线与女主唱的力量感，日本独立摇滚的骄傲。",
        "similar": ["tricot", "Number Girl", "ZAZEN BOYS", "Bloodthirsty Butchers"],
    },
    {
        "name": "THE NOVEMBERS",
        "aliases": ["the novembers", "novembers", "nove", "novembers band"],
        "tags": ["indie", "alternative", "shoegaze", "emo"],
        "desc": "暗黑美学的独立摇滚，从盯鞋到另类摇滚均有涉猎。",
        "similar": ["9mm Parabellum Bullet", "COALTAR OF THE DEEPERS", "PLASTIC GIRL IN CLOSET", "ART-SCHOOL"],
    },
    {
        "name": "PLASTIC GIRL IN CLOSET",
        "aliases": ["plastic girl in closet", "plastic girl", "pgic", "プラガ", "plastic girl band"],
        "tags": ["shoegaze", "indie", "dream-pop", "female-vocal"],
        "desc": "仙台出身的独立乐队，甜美噪音与少女心的完美结合。",
        "similar": ["THE NOVEMBERS", "For Tracy Hyde", "きのこ帝国 (Kinoko Teikoku)", "CQ"],
    },
    {
        "name": "くるり (Quruli)",
        "aliases": ["quruli", "くるり", "kururi", "quruli band"],
        "tags": ["indie", "alternative", "folk", "experimental"],
        "desc": "京都发祥的独立摇滚传奇，从 folk/indie 到电子实验的不断进化，日本 indie 的教科书。",
        "similar": ["Number Girl", "Asian Kung-Fu Generation", "Syrup16g (シロップ)", "SUPERCAR"],
    },
    {
        "name": "東京事変 (Tokyo Incidents)",
        "aliases": ["tokyo incidents", "tokyo jihen", "東京事変", "东京事变", "東京事變", "jihen", "tokyojihen"],
        "tags": ["jazz-rock", "alternative", "experimental", "progressive", "indie"],
        "desc": "椎名林檎领衔的五人乐队，爵士/放克/摇滚的知性融合，日本 2000 年代最重要的乐队之一。",
        "similar": ["くるり (Quruli)", "Number Girl", "ZAZEN BOYS", "Syrup16g (シロップ)", "ストレイテナー (STRAIGHTENER)"],
    },
    {
        "name": "銀杏BOYZ (Ging Nang Boyz)",
        "aliases": ["ging nang boyz", "銀杏ボーイズ", "ging nang", "ginnan boyz", "ギンナンボーイズ"],
        "tags": ["punk", "indie", "alternative", "noise"],
        "desc": "峯田和伸领衔的青春朋克乐队，赤裸的情感宣泄与 Lo-Fi 噪音美学。GOING STEADY 的精神继承者。",
        "similar": ["Number Girl", "Bloodthirsty Butchers", "Eastern Youth", "the pillows"],
    },
    {
        "name": "Base Ball Bear",
        "aliases": ["base ball bear", "baseball bear", "ベボベ", "bebobe"],
        "tags": ["indie", "alternative", "j-rock", "indie-pop"],
        "desc": "东京独立摇滚四人组，青春文学式歌词与跳跃的吉他旋律。",
        "similar": ["Asian Kung-Fu Generation", "the pillows", "Chatmonchy", "andymori"],
    },
    {
        "name": "GO!GO!7188",
        "aliases": ["go go 7188", "gogo7188", "go!go!7188", "ゴーゴー7188", "7188"],
        "tags": ["indie", "alternative", "punk", "female-vocal"],
        "desc": "九州出身的两女一男独立摇滚乐队，冲绳音阶 + 朋克态度的独特混搭。",
        "similar": ["Chatmonchy", "Number Girl", "Mass of the Fermenting Dregs (マスドレ)", "tricot"],
    },
    {
        "name": "Chatmonchy (チャットモンチー)",
        "aliases": ["chatmonchy", "チャットモンチー", "chat", "chatmonchy band"],
        "tags": ["indie", "alternative", "female-vocal", "j-rock"],
        "desc": "德岛出身的两女一男 indie rock 乐队，清新而有力的女子和声与摇滚编排。",
        "similar": ["GO!GO!7188", "Base Ball Bear", "tricot", "the pillows"],
    },
    {
        "name": "Bloodthirsty Butchers",
        "aliases": ["bloodthirsty butchers", "butchers", "blood thirsty butchers", "ブッチャーズ", "bloodthirsty"],
        "tags": ["indie", "punk", "alternative", "noise"],
        "desc": "北海道发祥的传奇独立/朋克乐队，田渕ひさ子的吉他音墙影响了无数后继者。",
        "similar": ["Number Girl", "Eastern Youth", "銀杏BOYZ (Ging Nang Boyz)", "COALTAR OF THE DEEPERS"],
    },
    {
        "name": "Eastern Youth",
        "aliases": ["eastern youth", "eastern", "イースタンユース"],
        "tags": ["indie", "punk", "alternative", "emo"],
        "desc": "东京三人朋克/独立乐队，吉野寿的怒吼和对社会议题的直面。90年代至今的日本 indies 支柱。",
        "similar": ["Bloodthirsty Butchers", "Number Girl", "銀杏BOYZ (Ging Nang Boyz)", "envy"],
    },
    {
        "name": "cinema staff",
        "aliases": ["cinema staff", "cinema", "シネマスタッフ", "cinestaff"],
        "tags": ["indie", "alternative", "emo", "post-rock"],
        "desc": "岐阜出身的独立摇滚四人组，锐利的吉他 riff 和后摇式的情绪爆发。",
        "similar": ["9mm Parabellum Bullet", "HaKU", "THE NOVEMBERS", "the cabs"],
    },
    {
        "name": "ストレイテナー (STRAIGHTENER)",
        "aliases": ["straightener", "ストレイテナー", "streitena", "テナー", "tena"],
        "tags": ["indie", "alternative", "emo", "j-rock"],
        "desc": "东京独立摇滚的中坚力量，流畅的旋律线与 emo/post-hardcore 影响。",
        "similar": ["Asian Kung-Fu Generation", "9mm Parabellum Bullet", "ELLEGARDEN", "cinema staff"],
    },
    {
        "name": "ACIDMAN",
        "aliases": ["acidman", "アシッドマン", "acid man"],
        "tags": ["indie", "alternative", "post-rock", "j-rock"],
        "desc": "埼玉出身三人组，自然/宇宙主题的歌词与宏大的器乐铺陈。日本 arena 级独立摇滚。",
        "similar": ["ストレイテナー (STRAIGHTENER)", "Asian Kung-Fu Generation", "Mono", "BUMP OF CHICKEN"],
    },
    {
        "name": "BUMP OF CHICKEN",
        "aliases": ["bump of chicken", "bump", "バンプ", "バンプオブチキン", "boc"],
        "tags": ["alternative", "j-rock", "indie", "emo"],
        "desc": "日本国民级摇滚乐队，藤原基央的诗意歌词和细腻的旋律叙事。",
        "similar": ["RADWIMPS", "ACIDMAN", "Asian Kung-Fu Generation", "ストレイテナー (STRAIGHTENER)"],
    },
    {
        "name": "RADWIMPS",
        "aliases": ["radwimps", "ラッドウインプス", "rad", "ラッド"],
        "tags": ["alternative", "j-rock", "indie", "emo"],
        "desc": "野田洋次郎领衔的另类摇滚乐队，《你的名字。》原声带让他们享誉全球。哲学思辨式歌词。",
        "similar": ["BUMP OF CHICKEN", "ONE OK ROCK", "Asian Kung-Fu Generation", "ACIDMAN"],
    },
    {
        "name": "andymori",
        "aliases": ["andymori", "アンディモリ", "andy mori"],
        "tags": ["indie", "alternative", "punk", "j-rock"],
        "desc": "小山田壮平领衔的青春 indie rock 三人组，热血与感伤并存的东京青春赞歌。",
        "similar": ["Base Ball Bear", "Asian Kung-Fu Generation", "the pillows", "銀杏BOYZ (Ging Nang Boyz)"],
    },
    {
        "name": "the pillows",
        "aliases": ["pillows", "the pillows", "ピロウズ", "the pillows band"],
        "tags": ["indie", "alternative", "punk", "j-rock"],
        "desc": "日本另类摇滚的常青树，《FLCL》原声带让他们在全球范围内广为人知。爽朗的吉他流行曲与不老的少年心气。",
        "similar": ["Asian Kung-Fu Generation", "Number Girl", "ELLEGARDEN", "Base Ball Bear"],
    },
    {
        "name": "Sparta Locals",
        "aliases": ["sparta locals", "sparta", "スパルタローカルズ"],
        "tags": ["indie", "alternative", "math-rock", "experimental"],
        "desc": "福冈出身的独立/数学摇滚乐队，尖锐的吉他切分和独特的日式 vocal 旋律。",
        "similar": ["ZAZEN BOYS", "Number Girl", "tricot", "Syrup16g (シロップ)"],
    },
    {
        "name": "people in the box",
        "aliases": ["people in the box", "pitb", "people box", "ピープルインザボックス"],
        "tags": ["indie", "alternative", "emo", "experimental"],
        "desc": "暗黑文学系独立摇滚三人组，内省式歌词和沉重而精致的吉他编曲。",
        "similar": ["Syrup16g (シロップ)", "THE NOVEMBERS", "ART-SCHOOL", "downy"],
    },
    {
        "name": "NICO Touches the Walls",
        "aliases": ["nico touches the walls", "nico", "ニコタッチズザウォールズ", "nicotachi"],
        "tags": ["indie", "alternative", "j-rock", "indie-pop"],
        "desc": "东京独立摇滚四人组，耳熟能详的动画主题曲和明快的吉他旋律。",
        "similar": ["Base Ball Bear", "Asian Kung-Fu Generation", "ストレイテナー (STRAIGHTENER)", "the pillows"],
    },

    # ============================================================
    # J-Rock / Punk
    # ============================================================
    {
        "name": "ELLEGARDEN",
        "aliases": ["ellegarden", "elle", "エルレガーデン", "エルレ", "ellegarden band"],
        "tags": ["punk", "j-rock", "indie", "alternative"],
        "desc": "细美武士领衔的日系旋律朋克，英文歌词 + 热血旋律。",
        "similar": ["Asian Kung-Fu Generation", "ONE OK ROCK", "the HIATUS", "ストレイテナー (STRAIGHTENER)"],
    },
    {
        "name": "the HIATUS",
        "aliases": ["hiatus", "the hiatus", "ザ・ハイエイタス", "the hiatus band"],
        "tags": ["indie", "alternative", "piano-rock", "emo"],
        "desc": "ELLEGARDEN 解散后细美武士的新方向，更成熟内敛的独立摇滚。",
        "similar": ["ELLEGARDEN", "THE NOVEMBERS", "9mm Parabellum Bullet", "ストレイテナー (STRAIGHTENER)"],
    },
    {
        "name": "ONE OK ROCK",
        "aliases": ["one ok rock", "oneokrock", "oor", "ワンオク", "oneok"],
        "tags": ["j-rock", "alternative", "punk", "emo"],
        "desc": "日本最具国际影响力的摇滚乐队之一，从 emo/punk 发端到 arena rock 巨团。",
        "similar": ["ELLEGARDEN", "Asian Kung-Fu Generation", "9mm Parabellum Bullet", "RADWIMPS"],
    },
    {
        "name": "Maximum the Hormone (マキシマムザホルモン)",
        "aliases": ["maximum the hormone", "ホルモン", "mth", "maximam the hormone", "マキシマムザホルモン"],
        "tags": ["alternative-metal", "punk", "funk", "experimental"],
        "desc": "日本最疯狂的混种摇滚乐队之一，metal/punk/funk 的无缝切换，现场爆发力爆表。",
        "similar": ["Boris", "Melt-Banana", "9mm Parabellum Bullet", "coldrain"],
    },
    {
        "name": "Crossfaith",
        "aliases": ["crossfaith", "クロスフェイス"],
        "tags": ["metalcore", "electronic", "post-hardcore", "alternative"],
        "desc": "大阪出身，将 metalcore 与 electronic/EDM 融合，国际音乐节常客。",
        "similar": ["coldrain", "FACT", "ONE OK ROCK", "Maximum the Hormone (マキシマムザホルモン)"],
    },

    # ============================================================
    # Experimental / Noise
    # ============================================================
    {
        "name": "Boris",
        "aliases": ["boris", "ボリス"],
        "tags": ["drone", "noise", "experimental", "heavy"],
        "desc": "日本实验摇滚的巨人，从 drone/doom 到 noise rock 到迷幻，无所不能。",
        "similar": ["Melt-Banana", "COALTAR OF THE DEEPERS", "downy", "Maximum the Hormone (マキシマムザホルモン)"],
    },
    {
        "name": "Melt-Banana",
        "aliases": ["melt-banana", "melt banana", "meltbanana", "メルトバナナ"],
        "tags": ["noise", "punk", "experimental", "indie"],
        "desc": "疯狂的噪音朋克二人组，超高速吉他与尖锐人声的极限体验。",
        "similar": ["Boris", "Number Girl", "Otoboke Beaver (おとぼけビ～バ～)"],
    },
    {
        "name": "Otoboke Beaver (おとぼけビ～バ～)",
        "aliases": ["otoboke beaver", "otoboke", "おとぼけビーバー", "otoboke beaver band", "otoboke beaver"],
        "tags": ["punk", "noise", "female-vocal", "indie"],
        "desc": "京都女子朋克乐队，狂野、幽默、充满爆发力的现场。",
        "similar": ["Melt-Banana", "Number Girl", "Mass of the Fermenting Dregs (マスドレ)", "GO!GO!7188"],
    },
    {
        "name": "八十八ヶ所巡礼 (88kasyo junrei)",
        "aliases": ["88kasyo junrei", "八十八ヶ所巡礼", "88", "hachijuuhachi kasho", "88 junrei"],
        "tags": ["math-rock", "progressive", "experimental", "indie"],
        "desc": "东京技术系器乐摇滚，超高难度的演奏和神秘主义的世界观。",
        "similar": ["ZAZEN BOYS", "LITE", "mudy on the 昨晩", "tricot"],
    },
    {
        "name": "piana",
        "aliases": ["piana", "ピアナ"],
        "tags": ["electronic", "dream-pop", "ambient", "experimental"],
        "desc": "佐佐木直美的个人电子计划，脆弱而精致的电子梦境。",
        "similar": ["matryoshka", "World's End Girlfriend", "KASHIWA Daisuke", "Honeydip"],
    },

    # ============================================================
    # J-Pop / Electronic (crossover)
    # ============================================================
    {
        "name": "Perfume",
        "aliases": ["perfume", "パフューム", "perfume japan"],
        "tags": ["j-pop", "electronic", "techno-pop", "experimental"],
        "desc": "中田ヤスタカ制作的电音女团，Techno-pop 的极致，与实验电子和独立场景有深层联系。",
        "similar": ["CAPSULE", "きゃりーぱみゅぱみゅ (Kyary Pamyu Pamyu)", "World's End Girlfriend"],
    },
    {
        "name": "CAPSULE",
        "aliases": ["capsule", "カプセル"],
        "tags": ["electronic", "j-pop", "experimental", "techno-pop"],
        "desc": "中田ヤスタカ+越岛敏子的电音二人组，从 neo-Shibuya-kei 到 EDM 的进化，日本电子音乐的标杆。",
        "similar": ["Perfume", "きゃりーぱみゅぱみゅ (Kyary Pamyu Pamyu)", "World's End Girlfriend"],
    },
    {
        "name": "きゃりーぱみゅぱみゅ (Kyary Pamyu Pamyu)",
        "aliases": ["kyary pamyu pamyu", "kyary", "きゃりー", "kpp", "kyary pamyu"],
        "tags": ["j-pop", "electronic", "experimental"],
        "desc": "虽然主打 J-Pop，但中田ヤスタカ的制作充满了实验电子元素，与独立音乐场景有千丝万缕的联系。",
        "similar": ["Perfume", "CAPSULE", "World's End Girlfriend"],
    },

    # ============================================================
    # Shoegaze / Dream Pop (continued)
    # ============================================================
    {
        "name": "Burrrn",
        "aliases": ["burrrn", "burn", "バーン"],
        "tags": ["shoegaze", "noise-pop", "indie", "dream-pop"],
        "desc": "东京单人盯鞋计划，甜美而粗粝的噪音墙包裹着朦胧的人声。",
        "similar": ["My Dead Girlfriend", "pasteboard", "COALTAR OF THE DEEPERS", "dive"],
    },
    {
        "name": "Seventeen Years Old and Berlin Wall",
        "aliases": ["seventeen years old and berlin wall", "17 years old and berlin wall", "syoabw", "17才とベルリンの壁"],
        "tags": ["shoegaze", "dream-pop", "indie", "female-vocal"],
        "desc": "名古屋的梦幻盯鞋二人组，如同青春期的朦胧记忆般温柔而忧伤的音景。",
        "similar": ["きのこ帝国 (Kinoko Teikoku)", "Oeil", "For Tracy Hyde", "溶けない名前 (Tokenai Namae)"],
    },
    {
        "name": "Softsurf",
        "aliases": ["softsurf", "soft surf", "ソフトサーフ"],
        "tags": ["shoegaze", "dream-pop", "indie"],
        "desc": "东京盯鞋新锐，清澈的吉他音色和梦幻的旋律线。",
        "similar": ["yuragi", "Oeil", "RAY", "Hartfield"],
    },
    {
        "name": "Texas Pandaa",
        "aliases": ["texas pandaa", "texas panda", "テキサスパンダ"],
        "tags": ["shoegaze", "post-rock", "indie"],
        "desc": "北海道出身的盯鞋/后摇乐队，厚重的吉他音墙与壮大的音景设计。",
        "similar": ["COALTAR OF THE DEEPERS", "cruyff in the bedroom", "dive", "Mono"],
    },
    {
        "name": "Caucus",
        "aliases": ["caucus", "コーカス"],
        "tags": ["shoegaze", "dream-pop", "indie"],
        "desc": "东京盯鞋/梦泡乐队，绵密的吉他音墙和浮游感的人声。",
        "similar": ["dive", "Honeydip", "cruyff in the bedroom", "Luminous Orange"],
    },

    # ============================================================
    # Math Rock (continued)
    # ============================================================
    {
        "name": "宇宙コンビニ (uchu konbini)",
        "aliases": ["uchu konbini", "uchu konbini", "宇宙コンビニ", "uchu combini", "space convenience store"],
        "tags": ["math-rock", "emo", "indie", "progressive"],
        "desc": "京都数学摇滚/emo三人组，复杂拍子与青春情绪的完美融合，可惜已解散。",
        "similar": ["tricot", "the cabs", "JYOCHO", "a picture of her"],
    },
    {
        "name": "JYOCHO",
        "aliases": ["jyocho", "じょうちょ", "jyoucho"],
        "tags": ["math-rock", "progressive", "indie", "female-vocal"],
        "desc": "宇宙コンビニ吉他手的新计划，木吉他+长笛的独特编制的数学摇滚。",
        "similar": ["宇宙コンビニ (uchu konbini)", "tricot", "a picture of her", "toe"],
    },
    {
        "name": "paranoid void",
        "aliases": ["paranoid void", "paranoid", "パラノイドヴォイド"],
        "tags": ["math-rock", "instrumental", "indie", "female-vocal"],
        "desc": "大阪全女子器乐数学摇滚三人组，跳跃的节奏与精致的吉他对话。",
        "similar": ["tricot", "toe", "LITE", "a picture of her"],
    },
    {
        "name": "chouchou merged syrups",
        "aliases": ["chouchou merged syrups", "chouchou", "シュシュ", "cms"],
        "tags": ["math-rock", "emo", "indie", "female-vocal"],
        "desc": "东京 math rock/emo 三人组，复杂的节奏编排与 fragile 的人声交织。",
        "similar": ["tricot", "宇宙コンビニ (uchu konbini)", "the cabs", "a picture of her"],
    },
    {
        "name": "3nd (sand)",
        "aliases": ["3nd", "sand", "サンド", "three n d"],
        "tags": ["math-rock", "emo", "indie", "post-rock"],
        "desc": "东京器乐数学摇滚/emo四人组，细腻的吉他旋律与紧凑的节奏变化。",
        "similar": ["toe", "a picture of her", "how to count one to ten", "LITE"],
    },

    # ============================================================
    # Post-Rock (continued)
    # ============================================================
    {
        "name": "saisa",
        "aliases": ["saisa", "サイサ"],
        "tags": ["post-rock", "instrumental", "ambient", "indie"],
        "desc": "东京后摇乐队，暗色调的吉他叙事与空旷的都市音景。",
        "similar": ["Mono", "euphoria", "December", "miaou"],
    },
    {
        "name": "yodaka",
        "aliases": ["yodaka", "ヨダカ", "nightjar"],
        "tags": ["post-rock", "instrumental", "indie"],
        "desc": "福冈后摇四人组，温暖而内省的旋律铺陈与精密的三吉他编排。",
        "similar": ["toe", "sgt.", "miaou", "euphoria"],
    },
    {
        "name": "SHISHAMO",
        "aliases": ["shishamo", "シシャモ", "shishamo band"],
        "tags": ["indie", "alternative", "female-vocal", "j-rock"],
        "desc": "神奈川出身全女子 indie rock 三人组，从高中生乐队到全国巡演，青春的真实写照。",
        "similar": ["Chatmonchy (チャットモンチー)", "tricot", "GO!GO!7188", "ポルカドットスティングレイ (Polkadot Stingray)"],
    },
    {
        "name": "フレデリック (Frederic)",
        "aliases": ["frederic", "フレデリック", "frederic band", "furederikku"],
        "tags": ["indie", "alternative", "dance-rock", "indie-pop"],
        "desc": "神户出身的 indie/dance-rock 三人组，中毒性的节奏和独特的舞蹈律动。",
        "similar": ["Base Ball Bear", "sumika", "KEYTALK", "サカナクション (sakanaction)"],
    },
    {
        "name": "カネコアヤノ (Kaneko Ayano)",
        "aliases": ["kaneko ayano", "カネコアヤノ", "ayano kaneko", "kaneko"],
        "tags": ["indie-folk", "singer-songwriter", "indie", "female-vocal"],
        "desc": "横滨出身的创作歌手，从 Lo-Fi 卧室民谣到 full band 编制，真实而锋利的日常诗学。",
        "similar": ["青葉市子 (Ichiko Aoba)", "クリープハイプ (CreepHyp)", "andymori", "優河 (Yuga)"],
    },

    # ============================================================
    # Punk / Melodic Punk / Ska Punk
    # ============================================================
    {
        "name": "Hi-STANDARD",
        "aliases": ["hi-standard", "hi standard", "high standard", "ハイスタ", "haista"],
        "tags": ["punk", "melodic-punk", "hardcore", "ska-punk"],
        "desc": "日本旋律朋克的开山鼻祖，英文歌词+高速三和弦，影响了整整一代朋克乐队。",
        "similar": ["Ken Yokohama", "10-FEET", "ELLEGARDEN", "locofrank"],
    },
    {
        "name": "Ken Yokohama",
        "aliases": ["ken yokohama", "ken band", "横山健", "yokohama ken"],
        "tags": ["punk", "melodic-punk", "indie"],
        "desc": "Hi-STANDARD吉他手的个人计划，延续了热血旋律朋克的传统。",
        "similar": ["Hi-STANDARD", "10-FEET", "ELLEGARDEN", "locofrank"],
    },
    {
        "name": "10-FEET",
        "aliases": ["10-feet", "10 feet", "ten feet", "テンフィート"],
        "tags": ["punk", "melodic-punk", "alternative", "hardcore"],
        "desc": "京都三人朋克乐队，关西腔歌词+硬核爆发力，日本朋克场景的支柱。",
        "similar": ["Hi-STANDARD", "WANIMA", "ELLEGARDEN", "04 Limited Sazabys"],
    },
    {
        "name": "HEY-SMITH",
        "aliases": ["hey-smith", "hey smith", "ヘイスミス", "heysmith"],
        "tags": ["ska-punk", "punk", "melodic-punk", "indie"],
        "desc": "大阪 ska-punk 乐队，铜管齐鸣的狂欢派对，现场感染力极强。",
        "similar": ["10-FEET", "SHANK", "Hi-STANDARD", "ROTTENGRAFFTY"],
    },
    {
        "name": "WANIMA",
        "aliases": ["wanima", "ワニマ"],
        "tags": ["punk", "melodic-punk", "indie"],
        "desc": "熊本出身的高速旋律朋克三人组，超快节奏+热血合唱，arena 级人气。",
        "similar": ["10-FEET", "04 Limited Sazabys", "ELLEGARDEN", "Hi-STANDARD"],
    },
    {
        "name": "04 Limited Sazabys",
        "aliases": ["04 limited sazabys", "04", "フォーリミテッドサザビーズ", "four limited sazabys"],
        "tags": ["punk", "melodic-punk", "indie"],
        "desc": "名古屋旋律朋克三人组，高音主唱+跳跃感的节奏，新一代朋克场景的代表。",
        "similar": ["WANIMA", "10-FEET", "ELLEGARDEN", "SHANK"],
    },
    {
        "name": "SiM",
        "aliases": ["sim", "シム"],
        "tags": ["punk", "reggae-punk", "alternative", "metalcore"],
        "desc": "湘南出身的混种朋克乐队，reggae/punk/metal 的自由切换。",
        "similar": ["ROTTENGRAFFTY", "coldrain", "10-FEET", "Crossfaith"],
    },
    {
        "name": "ROTTENGRAFFTY",
        "aliases": ["rottengraffty", "rotten", "ロットングラフティー"],
        "tags": ["punk", "mixture", "alternative", "hardcore"],
        "desc": "京都发祥的混种摇滚五人组，punk/hip-hop/metal 的爆炸性融合。",
        "similar": ["SiM", "10-FEET", "HEY-SMITH", "MAN WITH A MISSION"],
    },
    {
        "name": "locofrank",
        "aliases": ["locofrank", "loco frank", "ロコフランク"],
        "tags": ["punk", "melodic-punk", "indie"],
        "desc": "东京旋律朋克三人组，英文歌词+爽快的吉他旋律。",
        "similar": ["Hi-STANDARD", "SHANK", "Ken Yokohama", "ELLEGARDEN"],
    },
    {
        "name": "SHANK",
        "aliases": ["shank", "シャンク"],
        "tags": ["punk", "ska-punk", "melodic-punk", "indie"],
        "desc": "长野出身的 ska-punk 四人组，高速双声轨轮流爆发的热血现场。",
        "similar": ["HEY-SMITH", "locofrank", "10-FEET", "04 Limited Sazabys"],
    },
    {
        "name": "NAMBA69",
        "aliases": ["namba69", "namba", "ナンバ69", "難波69"],
        "tags": ["punk", "melodic-punk", "hardcore"],
        "desc": "Hi-STANDARD 难波章浩的个人朋克计划，更加直接的 hardcore 态度。",
        "similar": ["Hi-STANDARD", "Ken Yokohama", "10-FEET", "locofrank"],
    },
    {
        "name": "MAN WITH A MISSION",
        "aliases": ["man with a mission", "man with a mission", "mwam", "マンウィズアミッション", "man with"],
        "tags": ["alternative", "punk", "electronic", "indie"],
        "desc": "狼头人身的谜之五人组，将 punk/electronic/dance 融为一体的国际化乐队。",
        "similar": ["ROTTENGRAFFTY", "ONE OK ROCK", "coldrain", "Crossfaith"],
    },

    # ============================================================
    # Metal / Visual Kei / Alternative Metal
    # ============================================================
    {
        "name": "DIR EN GREY",
        "aliases": ["dir en grey", "dir", "dir en grey", "ディルアングレイ"],
        "tags": ["alternative-metal", "visual-kei", "experimental", "heavy"],
        "desc": "日本最具国际影响力的 heavy rock 乐队之一，从视觉系到前卫金属的惊人进化。",
        "similar": ["the GazettE", "X JAPAN", "coldrain", "Boris"],
    },
    {
        "name": "X JAPAN",
        "aliases": ["x japan", "x", "エックスジャパン", "x-japan"],
        "tags": ["heavy-metal", "visual-kei", "orchestral", "alternative"],
        "desc": "日本视觉系的创始者和传奇，将古典乐与重金属融合为壮大的摇滚叙事。",
        "similar": ["LUNA SEA", "DIR EN GREY", "the GazettE", "ONE OK ROCK"],
    },
    {
        "name": "LUNA SEA",
        "aliases": ["luna sea", "ルナシー", "lunasea", "luna"],
        "tags": ["alternative-rock", "visual-kei", "indie"],
        "desc": "日本视觉系黄金时代的代表，暗黑美学与另类摇滚的完美融合。",
        "similar": ["X JAPAN", "DIR EN GREY", "the GazettE", "ACIDMAN"],
    },
    {
        "name": "the GazettE",
        "aliases": ["gazette", "the gazette", "the gazette", "ガゼット"],
        "tags": ["alternative-metal", "visual-kei", "hardcore"],
        "desc": "名古屋出身视觉系代表，重型吉他 riffs 与暗黑美学的视觉冲击。",
        "similar": ["DIR EN GREY", "X JAPAN", "coldrain", "FACT"],
    },
    {
        "name": "Crystal Lake",
        "aliases": ["crystal lake", "クリスタルレイク"],
        "tags": ["metalcore", "heavy", "alternative"],
        "desc": "东京 metalcore 代表，国际 metalcore 场景中日本的声音，重型 breakdown 和英语歌词。",
        "similar": ["coldrain", "Crossfaith", "FACT", "Fear, and Loathing in Las Vegas"],
    },
    {
        "name": "Fear, and Loathing in Las Vegas",
        "aliases": ["fear and loathing in las vegas", "fear loathing", "las vegas", "fear loathing las vegas", "ファーアンドロージングインラスベガス"],
        "tags": ["electronic", "post-hardcore", "alternative", "metalcore"],
        "desc": "神户出身的 electronicore 六人组，Auto-Tune 人声+EDM+金属核的无厘头爆炸。",
        "similar": ["Crossfaith", "coldrain", "FACT", "SiM"],
    },
    {
        "name": "Girugamesh (ギルガメッシュ)",
        "aliases": ["girugamesh", "girugamesshu", "ギルガメッシュ", "gilgamesh"],
        "tags": ["alternative-metal", "visual-kei", "indie"],
        "desc": "东京视觉系/alternative metal 四人组，重型 groove 与日系旋律的交错。",
        "similar": ["the GazettE", "DIR EN GREY", "FACT", "coldrain"],
    },

    # ============================================================
    # Folk / Neo-folk / Singer-songwriter
    # ============================================================
    {
        "name": "青葉市子 (Ichiko Aoba)",
        "aliases": ["ichiko aoba", "aoba ichiko", "青葉市子", "ichiko", "aoba"],
        "tags": ["folk", "ambient", "neo-folk", "female-vocal"],
        "desc": "日本 neo-folk 的代表，空灵的歌声与精致的古典吉他编织出梦幻般的音景。",
        "similar": ["YeYe", "ハンバート ハンバート (Humbert Humbert)", "優河 (Yuga)", "matryoshka"],
    },
    {
        "name": "ハンバート ハンバート (Humbert Humbert)",
        "aliases": ["humbert humbert", "ハンバートハンバート", "humbert", "hanba"],
        "tags": ["folk", "indie-folk", "duo"],
        "desc": "男女双声道的温暖民谣二人组，日常生活的细腻观察与轻快的吉他旋律。",
        "similar": ["青葉市子 (Ichiko Aoba)", "YeYe", "advantage Lucy", "Lamp"],
    },
    {
        "name": "YeYe",
        "aliases": ["yeye", "イエイエ", "yeye singer"],
        "tags": ["indie-folk", "dream-pop", "female-vocal"],
        "desc": "东京 indie-folk 创作歌手，温柔的呢喃与 dream-pop 质感的吉他。",
        "similar": ["青葉市子 (Ichiko Aoba)", "ハンバート ハンバート (Humbert Humbert)", "advantage Lucy", "CQ"],
    },
    {
        "name": "優河 (Yuga)",
        "aliases": ["yuga", "優河", "yuuga"],
        "tags": ["folk", "neo-folk", "female-vocal", "soul"],
        "desc": "东京 neo-folk/灵魂乐创作歌手，醇厚的嗓音与 minimal 的器乐编排。",
        "similar": ["青葉市子 (Ichiko Aoba)", "YeYe", "ハンバート ハンバート (Humbert Humbert)", "Lamp"],
    },
    {
        "name": "七尾旅人 (Nanao Tabito)",
        "aliases": ["nanao tabito", "nanao", "七尾旅人", "tabito"],
        "tags": ["folk", "singer-songwriter", "indie"],
        "desc": "日本 folk/singer-songwriter 的异色存在，实验性的声音探索与社会议题的直面。",
        "similar": ["青葉市子 (Ichiko Aoba)", "World's End Girlfriend", "くるり (Quruli)", "KASHIWA Daisuke"],
    },

    # ============================================================
    # Post-punk / New Wave / Garage
    # ============================================================
    {
        "name": "ゆらゆら帝国 (Yura Yura Teikoku)",
        "aliases": ["yura yura teikoku", "yurayura teikoku", "ゆらゆら帝国", "yurayura", "yyteikoku"],
        "tags": ["post-punk", "psychedelic", "indie", "garage-rock"],
        "desc": "坂本慎太郎领衔的迷幻/车库传奇，90年代日本地下摇滚的基石，解散后被恒久怀念。",
        "similar": ["Number Girl", "ZAZEN BOYS", "Bloodthirsty Butchers", "Boris"],
    },
    {
        "name": "The Birthday",
        "aliases": ["birthday", "the birthday", "ザ・バースデイ"],
        "tags": ["punk", "garage-rock", "indie", "alternative"],
        "desc": "チバユウスケ (thee michelle gun elephant) 领衔的 garage punk 乐队，粗粝且浪漫的蓝领摇滚。",
        "similar": ["ゆらゆら帝国 (Yura Yura Teikoku)", "Number Girl", "Bloodthirsty Butchers", "銀杏BOYZ (Ging Nang Boyz)"],
    },
    {
        "name": "戸川純 (Jun Togawa)",
        "aliases": ["jun togawa", "togawa jun", "戸川純", "togawa"],
        "tags": ["new-wave", "experimental", "female-vocal", "post-punk"],
        "desc": "日本 new wave / 实验音乐的 cult icon，从ゲルニカ到ソロ，病态美学与尖锐创意。",
        "similar": ["P-MODEL", "Melt-Banana", "Boris", "Buffalo Daughter"],
    },
    {
        "name": "P-MODEL",
        "aliases": ["p-model", "p model", "pmodel", "ピーモデル"],
        "tags": ["new-wave", "techno-pop", "experimental", "post-punk"],
        "desc": "平沢進领衔的传说级 techno-pop/新浪潮乐队，日本 80 年代地下音乐的先驱。",
        "similar": ["戸川純 (Jun Togawa)", "ヒカシュー", "Boredoms", "World's End Girlfriend"],
    },
    {
        "name": "突然段ボール (Totsuzen Danball)",
        "aliases": ["totsuzen danball", "totsuzendanball", "突然段ボール", "sudden cardboard"],
        "tags": ["post-punk", "new-wave", "experimental", "indie"],
        "desc": "80年代日本 post-punk / new wave 的代表，奇抜的创意与 Lo-Fi 美学的先驱。",
        "similar": ["P-MODEL", "戸川純 (Jun Togawa)", "Boredoms", "ゆらゆら帝国 (Yura Yura Teikoku)"],
    },

    # ============================================================
    # Indie / Alternative Rock (continued)
    # ============================================================
    {
        "name": "サカナクション (sakanaction)",
        "aliases": ["sakanaction", "sakana", "サカナクション", "sakanaction band"],
        "tags": ["electronic", "indie", "alternative", "experimental"],
        "desc": "北海道出身的电子/另类摇滚五人组，将 dance music 与 indie rock 无缝融合的国民级乐队。",
        "similar": ["くるり (Quruli)", "King Gnu", "cero", "Suchmos"],
    },
    {
        "name": "フジファブリック (Fujifabric)",
        "aliases": ["fujifabric", "fuji fabric", "フジファブリック", "fujifabric band"],
        "tags": ["indie", "alternative", "j-rock"],
        "desc": "山梨县出身的 indie rock 乐队，纤细的旋律线与青春感满溢的歌词。",
        "similar": ["Asian Kung-Fu Generation", "くるり (Quruli)", "Base Ball Bear", "ストレイテナー (STRAIGHTENER)"],
    },
    {
        "name": "indigo la End",
        "aliases": ["indigo la end", "indigo", "インディゴ・ラ・エンド", "indigo la"],
        "tags": ["indie", "alternative", "city-pop", "indie-pop"],
        "desc": "川谷絵音领衔的 indie 四人组，都会的感伤与精致的流行旋律。",
        "similar": ["ゲスの極み乙女 (Gesu no Kiwami Otome)", "Lucky Tapes", "cero", "Suchmos"],
    },
    {
        "name": "ゲスの極み乙女 (Gesu no Kiwami Otome)",
        "aliases": ["gesu no kiwami otome", "gesu", "ゲスの極み乙女", "gesu otome", "gesu no kiwami"],
        "tags": ["indie", "progressive", "jazz", "experimental"],
        "desc": "川谷絵音的另一乐队，更 experimental 的编曲+爵士和声+hip-hop 律动。",
        "similar": ["indigo la End", "King Gnu", "ZAZEN BOYS", "cero"],
    },
    {
        "name": "King Gnu",
        "aliases": ["king gnu", "kinggnu", "キングヌー"],
        "tags": ["alternative", "indie", "experimental", "mixture"],
        "desc": "东京四人组，将摇滚/jazz/classical/hip-hop 融为一体的次世代国民乐队。",
        "similar": ["ゲスの極み乙女 (Gesu no Kiwami Otome)", "Suchmos", "サカナクション (sakanaction)", "cero"],
    },
    {
        "name": "[Alexandros]",
        "aliases": ["alexandros", "[alexandros]", "アレキサンドロス", "[champagne]", "champagne"],
        "tags": ["alternative", "indie", "j-rock"],
        "desc": "东京发祥的另类摇滚四人组，英文歌词+arena rock 的爆发力。",
        "similar": ["ONE OK ROCK", "ELLEGARDEN", "ストレイテナー (STRAIGHTENER)", "Asian Kung-Fu Generation"],
    },
    {
        "name": "ポルカドットスティングレイ (Polkadot Stingray)",
        "aliases": ["polkadot stingray", "polkadot", "ポルカドットスティングレイ", "polca"],
        "tags": ["indie", "alternative", "female-vocal", "j-rock"],
        "desc": "福冈出身的 indie rock 四人组，雫的酷帅女主唱和跳跃的吉他 riff。",
        "similar": ["tricot", "Base Ball Bear", "Asian Kung-Fu Generation", "GO!GO!7188"],
    },
    {
        "name": "sumika",
        "aliases": ["sumika", "スミカ"],
        "tags": ["indie-pop", "indie", "alternative"],
        "desc": "神奈川出身的 indie pop 四人组，阳光感满溢的青春旋律和温暖的合唱。",
        "similar": ["Base Ball Bear", "フジファブリック (Fujifabric)", "Official髭男dism", "andymori"],
    },
    {
        "name": "KEYTALK",
        "aliases": ["keytalk", "キートーク"],
        "tags": ["indie", "alternative", "j-rock"],
        "desc": "东京 indie rock 四人组，双吉他+合成器的舞蹈感摇滚。",
        "similar": ["Base Ball Bear", "sumika", "the pillows", "フジファブリック (Fujifabric)"],
    },
    {
        "name": "the band apart",
        "aliases": ["band apart", "the band apart", "バンドアパート", "banapa"],
        "tags": ["indie", "alternative", "math-rock", "jazz"],
        "desc": "东京 indie/数学摇滚四人组，精致的三吉他编排与黑人音乐律动的融合。",
        "similar": ["tricot", "ZAZEN BOYS", "くるり (Quruli)", "mouse on the keys"],
    },
    {
        "name": "SHE'S",
        "aliases": ["she's", "shes", "シーズ"],
        "tags": ["indie-pop", "indie", "alternative", "piano-rock"],
        "desc": "大阪 piano-rock/indie pop 四人组，钢琴主导的清爽青春旋律。",
        "similar": ["sumika", "Base Ball Bear", "Official髭男dism", "フジファブリック (Fujifabric)"],
    },
    {
        "name": "クリープハイプ (CreepHyp)",
        "aliases": ["creephyp", "creep hyp", "クリープハイプ", "kuripu"],
        "tags": ["indie", "alternative", "emo"],
        "desc": "尾崎世界観领衔的三人组，文学性极强的歌词和内省式的 indie rock。",
        "similar": ["マカロニえんぴつ (Macaroni Enpitsu)", "indigo la End", "andymori", "Syrup16g (シロップ)"],
    },
    {
        "name": "マカロニえんぴつ (Macaroni Enpitsu)",
        "aliases": ["macaroni enpitsu", "macaroni", "マカロニえんぴつ", "makaronienpitsu", "macaroni pencil"],
        "tags": ["indie", "alternative", "emo"],
        "desc": "关西出身的新世代 indie rock 三人组，感伤的旋律和直击内心的日常歌词。",
        "similar": ["クリープハイプ (CreepHyp)", "Saucy Dog", "indigo la End", "andymori"],
    },
    {
        "name": "Saucy Dog",
        "aliases": ["saucy dog", "サウシードッグ"],
        "tags": ["indie", "alternative", "emo"],
        "desc": "大阪 indie rock 三人组，恋爱与失恋的切ない歌词+耳熟能详的旋律。",
        "similar": ["マカロニえんぴつ (Macaroni Enpitsu)", "クリープハイプ (CreepHyp)", "indigo la End", "andymori"],
    },
    {
        "name": "Official髭男dism (Official HIGE DANDism)",
        "aliases": ["official hige dandism", "hige dandism", "hige dandism", "official髭男dism", "ヒゲダン", "higedan"],
        "tags": ["j-pop", "indie-pop", "alternative", "indie"],
        "desc": "岛根县出身的钢琴 pop 四人组，从 indie 到国民级的跃升，藤原聡的旋律天赋令人惊叹。",
        "similar": ["sumika", "Base Ball Bear", "SHE'S", "King Gnu"],
    },
    {
        "name": "羊文学 (Hitsujibungaku)",
        "aliases": ["hitsujibungaku", "hitsuji bungaku", "羊文学", "sheep literature"],
        "tags": ["indie", "alternative", "dream-pop", "female-vocal"],
        "desc": "东京三人 indie rock 乐队，盐塚モエカ的透明感嗓音和 dream-pop 质感的吉他。",
        "similar": ["きのこ帝国 (Kinoko Teikoku)", "For Tracy Hyde", "CQ", "溶けない名前 (Tokenai Namae)"],
    },
    {
        "name": "ドミコ (domico)",
        "aliases": ["domico", "ドミコ"],
        "tags": ["indie", "alternative", "noise", "experimental"],
        "desc": "新潟出身两人组，Lo-Fi 噪音+电子节拍+后朋克态度，独特的地下美学。",
        "similar": ["ZAZEN BOYS", "Syrup16g (シロップ)", "THE NOVEMBERS", "ゆらゆら帝国 (Yura Yura Teikoku)"],
    },

    # ============================================================
    # Electronic / Experimental (continued)
    # ============================================================
    {
        "name": "Cornelius",
        "aliases": ["cornelius", "コーネリアス", "keigo oyamada", "小山田圭吾"],
        "tags": ["electronic", "experimental", "shibuya-kei", "indie"],
        "desc": "小山田圭吾的个人计划，涩谷系的核心人物，极简电子与视觉艺术的完美融合。",
        "similar": ["CAPSULE", "Buffalo Daughter", "P-MODEL", "World's End Girlfriend"],
    },
    {
        "name": "fishmans",
        "aliases": ["fishmans", "fishmans band", "フィッシュマンズ"],
        "tags": ["dub", "dream-pop", "electronic", "indie"],
        "desc": "90年代传奇三人组，佐藤伸治的透明感假声+dub/dream-pop的独特融合。《LONG SEASON》是不朽名盘。",
        "similar": ["Cornelius", "Lamp", "World's End Girlfriend", "Lucky Tapes"],
    },
    {
        "name": "Buffalo Daughter",
        "aliases": ["buffalo daughter", "buffalo", "バッファロードーター"],
        "tags": ["electronic", "experimental", "indie", "female-vocal"],
        "desc": "东京电子/实验三人组，将 turntable/guitar/电子节拍编织成独特的跨界音乐。",
        "similar": ["Cornelius", "Boredoms", "matryoshka", "CAPSULE"],
    },
    {
        "name": "Boredoms",
        "aliases": ["boredoms", "ボアダムス", "bore"],
        "tags": ["noise", "experimental", "psychedelic", "drone"],
        "desc": "山塚アイ(EYE)领衔的噪音/实验传奇，从 hardcore 到 tribal drum circle 的疯狂进化。",
        "similar": ["Melt-Banana", "Boris", "P-MODEL", "戸川純 (Jun Togawa)"],
    },
    {
        "name": "OOIOO",
        "aliases": ["ooioo", "オーアイオー"],
        "tags": ["experimental", "noise", "female-vocal", "psychedelic"],
        "desc": "Boredoms 鼓手 Yoshimi 的全女子实验摇滚计划，tribal rhythm 与噪音的迷幻之旅。",
        "similar": ["Boredoms", "Melt-Banana", "Buffalo Daughter", "Boris"],
    },
]


def _normalize(s: str) -> str:
    """Lowercase, collapse whitespace, for fuzzy matching."""
    s = s.lower().strip()
    s = re.sub(r'\s+', ' ', s)
    return s


def _search_terms(b):
    """Yield all searchable terms for a band: aliases + name."""
    seen = set()
    for alias in b.get("aliases", []):
        norm = _normalize(alias)
        if norm and norm not in seen:
            seen.add(norm)
            yield norm, alias
    name_norm = _normalize(b["name"])
    if name_norm and name_norm not in seen:
        seen.add(name_norm)
        yield name_norm, b["name"]


def find_band(query: str):
    """Multi-strategy band lookup. Returns (matched_band, match_quality_str) or (None, None)."""

    q = _normalize(query)
    if not q:
        return None, None

    # Strategy 1: exact match
    for b in BANDS:
        for norm, _raw in _search_terms(b):
            if norm == q:
                return b, "exact"

    # Strategy 2: query is a substring of search term
    for b in BANDS:
        for norm, _raw in _search_terms(b):
            if q in norm:
                return b, "partial"

    # Strategy 3: search term is a substring of query (user typed extra words)
    for b in BANDS:
        for norm, _raw in _search_terms(b):
            if len(norm) >= 2 and norm in q:
                return b, "partial"

    # Strategy 4: fuzzy match via edit distance
    all_terms = []
    mapping = {}
    for b in BANDS:
        for norm, _raw in _search_terms(b):
            all_terms.append(norm)
            mapping[norm] = b

    cutoff = 0.6 if len(q) <= 3 else 0.7
    matches = get_close_matches(q, all_terms, n=1, cutoff=cutoff)
    if matches:
        return mapping[matches[0]], "fuzzy"

    return None, None


def get_suggestions(query: str, limit: int = 3):
    """Return closest band names even when no match is found (lower fuzzy cutoff)."""
    q = _normalize(query)
    if not q or len(q) < 2:
        return []

    all_terms = []
    mapping = {}
    for b in BANDS:
        for norm, _raw in _search_terms(b):
            all_terms.append(norm)
            mapping[norm] = b["name"]

    cutoff = 0.5 if len(q) <= 3 else 0.6
    matches = get_close_matches(q, all_terms, n=limit, cutoff=cutoff)
    seen = set()
    result = []
    for m in matches:
        name = mapping[m]
        if name not in seen:
            seen.add(name)
            result.append(name)
    return result[:limit]


def recommend(query: str, top_n: int = 5):
    """Find bands whose tags most overlap with the queried band."""
    matched, _quality = find_band(query)
    if not matched:
        return None, [], None

    # Build a case-insensitive lookup for similar-name boost
    name_index = {}
    for b in BANDS:
        name_index[_normalize(b["name"])] = b["name"]

    query_tags = set(matched["tags"])
    scored = []
    for b in BANDS:
        if b is matched:
            continue
        overlap = len(query_tags & set(b["tags"]))
        # Boost bands in the explicit similar list (case-insensitive)
        for sim_name in matched.get("similar", []):
            if name_index.get(_normalize(sim_name)) == b["name"]:
                overlap += 3
                break
        if overlap > 0:
            scored.append((b, overlap))

    scored.sort(key=lambda x: -x[1])
    return matched, [b for b, _ in scored[:top_n]], _quality
