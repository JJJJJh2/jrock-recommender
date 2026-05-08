# J-Rock Reco

Japanese rock band recommendation engine. Input a band name, get similar shoegaze / emo / math rock / indie recommendations.

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
