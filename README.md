# J-Rock Reco

一个帮你继续深挖日摇的小网站（｡•̀ᴗ-)✧

输入喜欢的乐队，
继续发现 shoegaze / emo / math rock / post-rock 宝藏 ✨

适合：
- 半夜挖团
- Spotify 推不出来的时候
- 想找冷门日摇的时候
- “听完 SUPERCAR 不知道下一步听什么” 的时候
## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>.

## Project Structure

```
jrock_reco/
├── app.py              # Flask application
├── bands_data.py       # Band database + recommendation logic
├── requirements.txt    # Python dependencies
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── index.html      # Search page
    └── history.html    # Search history page
```

## Data

`bands_data.py` contains ~30 Japanese rock bands with genre tags (shoegaze, emo, math rock, post-rock, indie, etc.). Recommendations are computed by tag overlap with a boost for explicitly listed similar bands.

Search history is stored in SQLite (`history.db`, auto-created on first run).
